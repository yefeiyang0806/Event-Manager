package com.fitbit.project.service;

import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hibernate.Hibernate;
import org.hibernate.SessionFactory;
import org.hibernate.classic.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import com.fitbit.project.domain.*;
import com.fitbit.project.domain.UserConnection.UserAndProvider;

@Service(value="userManager")
@Transactional
public class UserManager {
	
	@Autowired
	private SessionFactory sessionFactory;
	
	private final Log logger = LogFactory.getLog(getClass());
	
	public void setSessionFactory(SessionFactory sf){
		this.sessionFactory = sf;
	}
	
	public float parseFloat(String string){
		Float f = Float.parseFloat(string);
		return f;
	}
	
	public Boolean validatePassword(String pwd1, String pwd2){
		return (pwd1.equals(pwd2));
	}
	
	public boolean parseGender(String gender){
		return (gender.equals("male"));
	}
	
	public String createDisplayName(String username){
		User user = findByUsername(username);
	    if (user == null){
	    	return null;
	    }
	    String firstName = user.getFirstName();
	    String lastName = user.getLastName();
	    String displayName = username;
	    if ((firstName != null && firstName != "") && (lastName != null && lastName != "")){
	    	displayName = firstName +" "+ lastName;
	    }
	    else if (firstName != null && firstName != ""){
	    	displayName = firstName;
	    }
	    else if (lastName != null && lastName != ""){
	    	displayName = lastName;
	    }
	    return displayName;
	}
	
	public void addUser(User user){
		BCryptPasswordEncoder bcrpt = new BCryptPasswordEncoder();
		String encoded_pwd = bcrpt.encode(user.getPassword());
		user.setPassoword(encoded_pwd);
		this.sessionFactory.getCurrentSession().save(user);
	}
	
	public void updateUser(User user){
		if (user.getPassword() == null || user.getPassword().equals("")){
			User previous_record = findByUsername(user.getUsername());
			user.setPassoword(previous_record.getPassword());
		}
		else {
			BCryptPasswordEncoder bcrpt = new BCryptPasswordEncoder();
			String encoded_pwd = bcrpt.encode(user.getPassword());
			user.setPassoword(encoded_pwd);
		}
		this.sessionFactory.getCurrentSession().merge(user);
	}
	
	@SuppressWarnings("unchecked")
	public Map<String, Object> validateUser(User user, String op){
		Map<String, Object> resultSet = new HashMap<String, Object>();
		Set<String> error_msg = new HashSet<String>();
		
		User temp = findByUsername(user.getUsername());
		Map<String, Object> user_validated = null;
		if (temp == null && op.equals("create")){
			user_validated = validateNewUser(user);
		}
		else if (temp != null && op.equals("update")){
			user_validated = validateUpdateUser(user);
		}
		else if (temp == null && op.equals("update")){
			resultSet.put("result", false);
			error_msg.add("User " + user.getUsername() + " doesn't exist.");
			resultSet.put("error_msg", error_msg);
			return resultSet;
		}
		else if (temp != null && op.equals("create")){
			resultSet.put("result", false);
			error_msg.add("User " + user.getUsername() + " already exists. Please modify your username.");
			resultSet.put("error_msg", error_msg);
			return resultSet;
		}
		resultSet.put("result", user_validated.get("result"));
		error_msg = (Set<String>) user_validated.get("error_msg");
		if (error_msg.size() != 0){
			resultSet.put("error_msg", error_msg);
		}
		return resultSet;
	}
	
	public Map<String, Object> validateNewUser(User user){
		Map<String, Object> resultSet = new HashMap<String, Object>();
		boolean result = true;
		Set<String> error_msg = new HashSet<String>();
		if (user.getUsername().length()>20 || user.getUsername().length()<8){
			result = false;
			error_msg.add("Username Length Error. Username should be within 8-20 characters.");
		}
		if (user.getPassword().length()>20 || user.getPassword().length()<8){
			result = false;
			error_msg.add("Password Length Error. Password should be within 8-20 characters.");
		}
		if ((user.getFirstName()!=null && !user.getFirstName().matches("[a-zA-Z]+")) ||
				(user.getLastName()!=null && !user.getLastName().matches("[a-zA-Z]+"))){
			result = false;
			error_msg.add("Name Format Error. Name should only contains letters.");
		}
		resultSet.put("result", result);
		resultSet.put("error_msg", error_msg);
		return resultSet;
		
	}
	
	public Map<String, Object> validateUpdateUser(User user){
		Map<String, Object> resultSet = new HashMap<String, Object>();
		boolean result = true;
		Set<String> error_msg = new HashSet<String>();
		if ((user.getFirstName()!=null && !user.getFirstName().matches("[a-zA-Z]+")) ||
				(user.getLastName()!=null && !user.getLastName().matches("[a-zA-Z]+"))){
			result = false;
			error_msg.add("Name Format Error. Name should only contains letters.");
		}
		resultSet.put("result", result);
		resultSet.put("error_msg", error_msg);
		return resultSet;
	}
	
	public boolean checkPassword(String username, String password){
		User user = findByUsername(username);
		logger.info("password" + password);
		BCryptPasswordEncoder bcrpt = new BCryptPasswordEncoder();
		return (bcrpt.matches(password, user.getPassword()));
		//String encoded_pwd = bcrpt.encode(password);
		//logger.info("encoded_input" + encoded_pwd);
		//logger.info("Saved PWD: "+user.getPassword());
		//return (encoded_pwd == user.getPassword());
	}
	
	public void addUserConnection(Map<String, Object> hmap){
		UserConnection uc = new UserConnection();
		UserAndProvider uap = uc.new UserAndProvider();
		uap.setUserId((String) hmap.get("userId"));
		uap.setProviderId((String) hmap.get("providerId"));
		uap.setProviderUserId((String) hmap.get("providerUserId"));
		uc.setUserAndProvider(uap);
		logger.info("User manager provider user id: "+uc.getUserAndProvider().getProviderUserId());
		this.sessionFactory.getCurrentSession().save(uc);
		
	}
	
	public void addDailyCalorie(DailyCalorie dc){
		this.sessionFactory.getCurrentSession().save(dc);
	}
	
	public void addFoodCalorie(List<FoodCalorie> fc){
		for (int i=0; i<fc.size(); i++){
			this.sessionFactory.getCurrentSession().save(fc.get(i));
		}
	}
	
	public void addDietTask(DietTask dt){
		this.sessionFactory.getCurrentSession().save(dt);
	}
	
	public void updateDietTask(DietTask dt){
		this.sessionFactory.getCurrentSession().saveOrUpdate(dt);
	}
	
	public void deleteDietTaskById(long gotId){
		this.sessionFactory.getCurrentSession()
		.createQuery("delete from DietTask where Id=?")
		.setParameter(0, gotId).executeUpdate();
	}
	
	public List<FoodCalorie> getFoodListByUserAndDate (String username, String date){
		User user = findByUsername(username);
		DailyCalorie dc = null;
		if (user == null){
			return null;
		}
		List<DailyCalorie> dc_list = user.getDailyCalorie();
		if (dc_list != null){
			logger.info("Passed date is: "+date);
		}
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		
		for (int i=0; i<dc_list.size(); i++){
			DailyCalorie temp = dc_list.get(i);
			logger.info("Date in DB" + sdf.format(temp.getDate()));
			if (sdf.format(temp.getDate()).equals(date)){
				dc = temp;
				logger.info("Temp Date is: "+sdf.format(temp.getDate()));
			}
		}
		if (dc == null){
			logger.info("UserManager not found DC!!!");
			return null;
		}
		Hibernate.initialize(dc.getFoodCalorie());
		return dc.getFoodCalorie();
		
	}
	
	public List<DietTask> getDietTasksByUsername (String username){
		User user = findByUsername(username);
		Hibernate.initialize(user.getDietTasks());
		return user.getDietTasks();
	}
	
	@SuppressWarnings("unchecked")
	public DietTask getDietTaskById (long id){
		List<DietTask> dts = sessionFactory.getCurrentSession()
				.createQuery("from DietTask where Id=?")
				.setParameter(0, id)
				.list();
		if (dts.size() > 0){
			return dts.get(0);
		}
		else {
			//logger.info("Nothing found");
			return null;
		}
		
	}
	
	public Map<String, Integer> getWeeklyCalorieBetween (String username, Date start_date, Date end_date){
		Date temp = start_date;
		Map<String, Integer> results = new LinkedHashMap<String, Integer>();
		for (int i=0; i<100; i++){
			String this_day = formatDateToString(temp);
			DailyCalorie dc = getDailyCalorieByUserAndDate(username,this_day);
			Integer total = 0;
			if (dc != null){
				total = calcDailyCalorie(dc);
			}
			results.put(this_day, total);
			logger.info("Date: " + this_day);
			logger.info(total);
			if (this_day.equals(formatDateToString(end_date))){
				break;
			}
			temp = addOneDay(temp);
		}
		return results;	
	}
	
	public float getTotalCalorieBetween(String username, Date start_date, Date end_date){
		Date temp = start_date;
		float total = 0;
		for (int i=0; i<100; i++){
			String this_day = formatDateToString(temp);
			DailyCalorie dc = getDailyCalorieByUserAndDate(username,this_day);
			if (dc != null){
				total += calcDailyCalorie(dc);
			}
			if (this_day.equals(formatDateToString(end_date))){
				break;
			}
			temp = addOneDay(temp);
		}
		return total;	
	}
	
	public DailyCalorie getDailyCalorieByUserAndDate (String username, String date){
		User user = findByUsername(username);
		List<DailyCalorie> dc_list = user.getDailyCalorie();
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		
		for (int i=0; i<dc_list.size(); i++){
			DailyCalorie temp = dc_list.get(i);
			if (sdf.format(temp.getDate()).equals(date)){
				return temp;
			}
		}
		return null;
	}
	
	@SuppressWarnings("unchecked")
	public User findByUsername (String username){
		List<User> users = new ArrayList<User>();
		users = sessionFactory.getCurrentSession()
				.createQuery("from User where Username=?")
				.setParameter(0, username)
				.list();
		if (users.size() > 0){
			return users.get(0);
		}
		else {
			//logger.info("Nothing found");
			return null;
		}
	}
	
	@SuppressWarnings("unchecked")
	public User findByFbId (String fbId){
		List<User> users = new ArrayList<User>();
		users = sessionFactory.getCurrentSession()
				.createQuery("from User where Id=?")
				.setParameter(0, fbId)
				.list();
		if (users.size() > 0){
			return users.get(0);
		}
		else {
			//logger.info("Nothing found");
			return null;
		}
	}
	
	public String formatDateToString(Date date){
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		return sdf.format(date);
	}
	
	public Date addOneDay(Date date){
		Calendar c = Calendar.getInstance();
		c.setTime(date);
		c.add(Calendar.DATE, 1);
		return c.getTime();
	}
	
	public Integer calcDailyCalorie(DailyCalorie dc){
		List<FoodCalorie> foods = dc.getFoodCalorie();
		int total = 0;
		int food_number = foods.size();
		for (int i=0; i<food_number; i++){
			total += foods.get(i).getCalorie();
		}
		if (food_number == 0){
			return 0;
		}
		else {
			return total;
		}
	}
	
	@SuppressWarnings("unchecked")
	public Integer calcAllAverageCalorie(){
		List<DailyCalorie> allDC = sessionFactory.getCurrentSession()
				.createQuery("from DailyCalorie").list();
		int total = 0;
		int dc_number = allDC.size();
		logger.info("DC number: " + String.valueOf(dc_number));

		for (int i=0; i<allDC.size(); i++){
			total += calcDailyCalorie(allDC.get(i));
		}
		
		if (dc_number == 0){
			return 0;
		}
		Integer result = (total/dc_number);
		logger.info(result);
		return result;
	}
	
	public Date oneWeekFromDay(Date day){
		Calendar c = Calendar.getInstance();
		c.setTime(day);
		c.add(Calendar.DATE, -6);
		return c.getTime();
	}
	
	public Date oneWeekAfterDay(Date day){
		Calendar c = Calendar.getInstance();
		c.setTime(day);
		c.add(Calendar.DATE, +6);
		return c.getTime();
	}
	
	public Date durationFromStart(Date start, int duration){
		Calendar c = Calendar.getInstance();
		c.setTime(start);
		c.add(Calendar.DATE, duration);
		return c.getTime();
	}
	
	public int getActiveDays(String username){
		int count = 0;
		User user = findByUsername(username);
		Hibernate.initialize(user.getDailyCalorie());
		List<DailyCalorie> dcs = user.getDailyCalorie();
		for (DailyCalorie dc : dcs){
			Hibernate.initialize(dc.getFoodCalorie());
			if (!dc.getFoodCalorie().isEmpty()){
				count++;
			}
		}
		logger.info("# of Active days: " + count);
		return count;
	}
	
	public List<DailyCalorie> getActiveDailyCalorie(String username){
		List<DailyCalorie> results = new ArrayList<DailyCalorie>();
		User user = findByUsername(username);
		Hibernate.initialize(user.getDailyCalorie());
		List<DailyCalorie> dcs = user.getDailyCalorie();
		for (DailyCalorie dc : dcs){
			Hibernate.initialize(dc.getFoodCalorie());
			if (!dc.getFoodCalorie().isEmpty()){
				results.add(dc);
			}
		}
		return results;
	}
	
	public int getTotalDays(String username){
		Date first_day = this.getFirstDay(username);
		int num_of_days = this.daysBetween(first_day, new Date())+1;
		logger.info("First day: " + first_day);
		logger.info("Total days till today: " + num_of_days);
		return num_of_days;
	}
	
	public int daysBetween(Date first, Date second){
		long diff = second.getTime() - first.getTime();
		return (int) (TimeUnit.DAYS.convert(diff, TimeUnit.MILLISECONDS));
	}
	
	@SuppressWarnings("unchecked")
	public Date getFirstDay(String username){
		DailyCalorie dc = new DailyCalorie();
		long id = (Long) sessionFactory.getCurrentSession()
				.createQuery("select user.id from User user where Username=?")
				.setParameter(0, username).list().get(0);
		
		List<DailyCalorie> dcs = sessionFactory.getCurrentSession()
				.createQuery("from DailyCalorie where User_Id=? order by date")
				.setParameter(0, id)
				.setMaxResults(1)
				.list();
		if (dcs.isEmpty()){
			return new Date();
		}
		dc = dcs.get(0);
		Date first_day = dc.getDate();
		return first_day;
	}
	
	public int calcPersonalAverage(String username){
		Date startDate = this.getFirstDay(username);
		float totalCalorie = this.getTotalCalorieBetween(username, startDate, new Date());
		int days = this.getActiveDays(username);
		if (days == 0) return 0;
		double average = (double)totalCalorie/days;
		//average = Double.parseDouble(new DecimalFormat("##.##").format(average));
		return (int) average;
	}
	
	public int calcActiveRatio(String username){
		int totalDays = this.getTotalDays(username);
		int activeDays = this.getActiveDays(username);
		double ratio = (double)activeDays/totalDays*100;
		//ratio = Double.parseDouble(new DecimalFormat("##").format(ratio));
		return (int) ratio;
	}
	
	public Map<String, Integer> getMonthlyCalorie(String username) throws ParseException{
		Calendar now = Calendar.getInstance();
		int month = now.get(Calendar.MONTH)+1;
		//int day = now.get(Calendar.DATE);
		int year = now.get(Calendar.YEAR);
		int daysOfMonth = now.getActualMaximum(Calendar.DAY_OF_MONTH);
		Map<String, Integer> results = new HashMap<String, Integer>();
		DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date start_date = sdf.parse(year + "-" + month + "-01");
		Date finish_date = sdf.parse(year + "-" + month + "-" + (daysOfMonth-1));
		results = this.getWeeklyCalorieBetween(username, start_date, finish_date);
		return results;
	}
	
	public List<DietTask> getActiveDietTasks(String username) throws ParseException{
		List<DietTask> dts = this.getDietTasksByUsername(username);
		List<DietTask> results = new ArrayList<DietTask>();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date today = new Date();
		if (dts.isEmpty()) return null;
		for (DietTask dt : dts){
			Date finish = sdf.parse(dt.getFinish());
			Date start = sdf.parse(dt.getStart());
			if (today.before(finish) && today.after(start)){
				results.add(dt);
			}
		}
		return results;
	}
	
	public List<DietTask> getExpiredDietTasks(String username) throws ParseException{
		List<DietTask> dts = this.getDietTasksByUsername(username);
		List<DietTask> results = new ArrayList<DietTask>();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date today = new Date();
		if (dts.isEmpty()) return results;
		for (DietTask dt : dts){
			Date finish = sdf.parse(dt.getFinish());
			//Date start = sdf.parse(dt.getStart());
			if (today.after(finish)){
				results.add(dt);
			}
		}
		return results;
	}
	
	public List<DietTask> getNotStartDietTasks(String username) throws ParseException{
		List<DietTask> dts = this.getDietTasksByUsername(username);
		List<DietTask> results = new ArrayList<DietTask>();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date today = new Date();
		if (dts != null) return results;
		for (DietTask dt : dts){
			//Date finish = sdf.parse(dt.getFinish());
			Date start = sdf.parse(dt.getStart());
			if (today.before(start)){
				results.add(dt);
			}
		}
		return results;
	}
	
	public int countEatingTooMuchTimes(String username) {
		int count = 0;
		double recommended = 2100;
		List<DailyCalorie> active_dcs = this.getActiveDailyCalorie(username);
		for (DailyCalorie dc : active_dcs){
			//logger.info("Daily Calorie: " + this.calcDailyCalorie(dc));
			if (this.calcDailyCalorie(dc)>recommended){
				count++;
			}
		}
		return count;
	}
}

package com.fitbit.project.web;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;

import com.fitbit.project.domain.DietTask;
import com.fitbit.project.service.UserManager;

@Controller
@RequestMapping(value="/food")
public class AddDietTaskController {

	@Autowired
	private UserManager userManager;
	
	final private Integer CALORIE_PER_KG = 7000;
	
	final private Integer DEFAULT_CALORIE = 2100;
	
	protected final Log logger = LogFactory.getLog(getClass());
	
	@RequestMapping(value="/add_diet/add")
	public ModelAndView requestHandler(@RequestParam("weight_loss") String weightLoss, @RequestParam("start_date") String start,
			@RequestParam("duration") String duration, @RequestParam("email_frequency") String emailFrequency, @RequestParam(value="id", required=false) String id) throws ParseException, NumberFormatException{
		String displayName = createDisplayName();
		Integer totalReducedCalorie = (int) (Double.parseDouble(weightLoss)*CALORIE_PER_KG);
		Integer targetIntake = DEFAULT_CALORIE - totalReducedCalorie/(Integer.valueOf(duration));
		if (targetIntake < (DEFAULT_CALORIE/4)){
			Integer recommend_calorie = DEFAULT_CALORIE / 2;
			Integer recommend_duration = totalReducedCalorie/(DEFAULT_CALORIE - recommend_calorie);
			String error = "Don't push yourself so hard. It's unhealthy to take less than a quarter of the recommedned calorie intake (525 kcal) everyday.";
			Map<String, Object> myModel = new HashMap<String, Object>();
			myModel.put("weight_loss", weightLoss);
			myModel.put("start_date", start);
			myModel.put("recommend_duration", recommend_duration);
			myModel.put("error", error);
			logger.info(error);
			return new ModelAndView("add_diet_task", myModel);
		} else {
			try {
					Authentication auth = SecurityContextHolder.getContext().getAuthentication();
					String username = auth.getName();
					com.fitbit.project.domain.User user = userManager.findByUsername(username);
					DietTask dt = new DietTask();
					dt.setDailyTargetCalorie(targetIntake);
					dt.setDuration(Integer.valueOf(duration));
					dt.setWeightLoss((int)Double.parseDouble(weightLoss));
					dt.setUser(user);
					SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
					Date start_date = sdf.parse(start);
					Date finish_date = userManager.durationFromStart(start_date, Integer.valueOf(duration));
					String state = generateState(start_date, finish_date);
					dt.setState(state);
					dt.setStart(start);
					dt.setFinish(sdf.format(finish_date));
					if (id == null){
						userManager.addDietTask(dt);
					}
					else {
						long exist_id = Long.parseLong(id);
						dt.setId(exist_id);
						userManager.updateDietTask(dt);
					}
				}
			catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();	
			}
		}
		return new ModelAndView("redirect:/food/diet_tasks/");
	}
	
	@RequestMapping(value="/add_diet/")
	public ModelAndView handleAddPage (HttpServletRequest request){
		String displayName = createDisplayName();
		return new ModelAndView("add_diet_task", "displayName", displayName);
	}
	
	@RequestMapping(value="/modify_diet_task")
	public ModelAndView handleModify (@RequestParam("id") String id){
		String displayName = createDisplayName();
		long gotId = Long.parseLong(id, 10);
		DietTask dt = userManager.getDietTaskById(gotId);
		if (dt == null){
			return new ModelAndView("add_diet_task");
		}
		String start = dt.getStart();
		start = start.split(" ")[0];
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("modify", "modify");
		myModel.put("displayName", displayName);
		myModel.put("weight_loss", dt.getWeightLoss());
		myModel.put("duration", dt.getDuration());
		myModel.put("start_date", start);
		myModel.put("id", id);
		return new ModelAndView("add_diet_task", myModel);
	}
	
	@RequestMapping(value="/delete_diet_task")
	public ModelAndView handleDelete (@RequestParam("id") String id){
		long gotId = Long.parseLong(id, 10);
		userManager.deleteDietTaskById(gotId);
		return new ModelAndView("redirect:/food/diet_tasks/");
	}
	
	@RequestMapping(value="/diet_tasks/")
	public ModelAndView handleViewPage (HttpServletRequest request) throws ParseException{
		String displayName = createDisplayName();
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
		String username = auth.getName();
		List<DietTask> dts = userManager.getDietTasksByUsername(username);
		List<Float> totalCalories = new ArrayList<Float>();
		Integer length = dts.size();
		Date today = new Date();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		for (DietTask dt : dts){
			float tc = 0;
			String start = dt.getStart();
			String finish = dt.getFinish();
			Date startDate = sdf.parse(start);
			Date finishDate = sdf.parse(finish);
			if (finishDate.before(today)){
				tc = userManager.getTotalCalorieBetween(username, startDate, finishDate);
			}
			totalCalories.add(tc);
			start = start.split(" ")[0];
			finish = finish.split(" ")[0];
			dt.setStart(start);
			dt.setFinish(finish);
			dt.setState(generateState(startDate, finishDate));
			userManager.updateDietTask(dt);
		}
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("displayName", displayName);
		myModel.put("diet_tasks", dts);
		myModel.put("length", length);
		myModel.put("totalCalories", totalCalories);
		return new ModelAndView("view_diet_task", myModel);
	}
	
	@RequestMapping(value="/diet_tasks/performance")
	public ModelAndView handlePerformance (@RequestParam("id") String id) throws ParseException{
		String displayName = createDisplayName();
		long gotId = Long.parseLong(id, 10);
		DietTask dt = userManager.getDietTaskById(gotId);
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
		String username = auth.getName();
		com.fitbit.project.domain.User user = userManager.findByUsername(username);
	    if (user == null){
	    	return new ModelAndView("new_page");
	    }
	    Map<String, Integer> weeklyCalorie = new LinkedHashMap<String, Integer>();
		Date today = new Date();
		Date finish = sdf.parse(dt.getFinish());
		Date start = sdf.parse(dt.getStart());
		//Date start = userManager.oneWeekFromToday(today);
		if (today.before(finish)){
			weeklyCalorie = userManager.getWeeklyCalorieBetween(username, start, today);
		}
		else {
			weeklyCalorie = userManager.getWeeklyCalorieBetween(username, start, finish);
		}
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("weeklyCalorie", weeklyCalorie);
		myModel.put("allAverage", userManager.calcAllAverageCalorie());
		myModel.put("displayName", displayName);
		myModel.put("task", gotId);
		return new ModelAndView("comparison", myModel);
	}
	
	public String createDisplayName(){
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
		String username = auth.getName();
		com.fitbit.project.domain.User user = userManager.findByUsername(username);
		if (user == null){
			return null;
		}
	    String firstName = user.getFirstName();
	    String lastName = user.getLastName();
	    String displayName = username;
	    if ((firstName != null && firstName != "") && (lastName != null && lastName != "")){
	    	displayName = firstName + " " + lastName;
	    }
	    else if (firstName != null && firstName != ""){
	    	displayName = firstName;
	    }
	    else if (lastName != null && lastName != ""){
	    	displayName = lastName;
	    }
	    return displayName;
	}
	
	public String generateState (Date start_date, Date finish_date){
		Date today = new Date();
		String state = "";
		if (today.before(start_date)){
			state = "Not Started";
		}
		else if (today.after(start_date) && today.before(finish_date)){
			state = "Active";
		}
		else {
			state = "Expired";
		}
		return state;
	}
}

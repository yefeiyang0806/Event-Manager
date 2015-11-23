package com.fitbit.project.service.food;

import junit.framework.TestCase;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.transaction.annotation.Transactional;

import com.fitbit.project.domain.DietTask;
import com.fitbit.project.domain.User;
import com.fitbit.project.domain.DailyCalorie;

import com.fitbit.project.service.UserManager;

@ContextConfiguration(locations = "classpath:persistence-context-test.xml")
@RunWith(SpringJUnit4ClassRunner.class)
public class FoodUserManagerTest extends TestCase{

	@Autowired
	private UserManager userManager;

	private DateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
	
	@Test
	@Transactional
	@Rollback(true)
	public void testParseFloat(){
		Float actualValue = userManager.parseFloat("10.5");
		Float result = (float) 10.5;
		assertEquals(actualValue, result);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testValidatePassword(){
		String pwd1 = "asdfghjkl;'";
		String pwd2 = "asdfghjkl;'";
		boolean testValue = userManager.validatePassword(pwd1, pwd2);
		assertEquals(true, testValue);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testParseGender(){
		String g1 = "male";
		String g2 = "female";
		boolean testValue1 = userManager.parseGender(g1);
		boolean testValue2 = userManager.parseGender(g2);
		assertEquals(true, testValue1);
		assertEquals(false, testValue2);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testCreateDisplayName(){
		String correctName = "Hallo Ye";
		String result = userManager.createDisplayName("yefeiyang1");
		assertEquals(null, result);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testAddUser(){
		User user = new User();
		user.setUsername("testAdd");
		user.setPassoword("testPassword");
		user.setFirstName("testAdd");
		userManager.addUser(user);
		User result = userManager.findByUsername("testAdd");
		assertNotNull(result);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testUpdateUser(){
		User user1 = new User();
		user1.setUsername("testAdd");
		user1.setPassoword("testPassword");
		user1.setFirstName("testAdd");
		userManager.addUser(user1);
		String result = userManager.findByUsername("testAdd").getFirstName();
		assertEquals("testAdd",result);
		
		User userUpdated = new User();
		userUpdated.setUsername("testAdd");
		userUpdated.setId(user1.getId());
		//userUpdated.setPassoword("testPassword2");
		userUpdated.setFirstName("testUpdate");
		userManager.updateUser(userUpdated);
		result = userManager.findByUsername("testAdd").getFirstName();
		assertEquals("testUpdate",result);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testValidateUserShortUserName(){
		User user1 = new User();
		user1.setUsername("testAdd");
		user1.setPassoword("testPassword");
		Map<String, Object> resultSet = userManager.validateUser(user1, "create");
		Set<String> error_msg = (Set<String>) resultSet.get("error_msg");
		String short_username = "Username Length Error. Username should be within 8-20 characters.";
		assertEquals(true, error_msg.contains(short_username));
		assertEquals(1, error_msg.size());
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testValidateUserShortPassword(){
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("test");
		Map<String, Object> resultSet = userManager.validateUser(user1, "create");
		Set<String> error_msg = (Set<String>) resultSet.get("error_msg");
		String short_pwd = "Password Length Error. Password should be within 8-20 characters.";
		assertEquals(true, error_msg.contains(short_pwd));
		assertEquals(1, error_msg.size());
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testValidateUserAlreadyExist(){
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("testtest");
		userManager.addUser(user1);
		
		User user2 = new User();
		user2.setUsername("testAddTest");
		user2.setPassoword("testtest");
		Map<String, Object> resultSet = userManager.validateUser(user2, "create");
		Set<String> error_msg = (Set<String>) resultSet.get("error_msg");
		String already_exist = "User " + user1.getUsername() + " already exists. Please modify your username.";
		assertEquals(true, error_msg.contains(already_exist));
		assertEquals(1, error_msg.size());
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testCheckPassword(){
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("testtest");
		userManager.addUser(user1);
		assertEquals(true, userManager.checkPassword("testAddTest", "testtest"));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testAddDailyCalorie(){
		Date date = new Date();
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("testtest");
		DailyCalorie dc = new DailyCalorie();
		dc.setDate(date);
		dc.setUser(user1);
		List<DailyCalorie> dc_list = new ArrayList<DailyCalorie>();
		dc_list.add(dc);
		user1.setDailyCalorie(dc_list);
		userManager.addUser(user1);
		
		userManager.addDailyCalorie(dc);
		//User user_dc = userManager.findByUsername(user1.getUsername());
		assertEquals(dc,userManager.getDailyCalorieByUserAndDate("testAddTest", sdf.format(date)));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testGetDietTasksByUsername(){
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("testtest");
		DietTask dt = new DietTask();
		dt.setDuration(20);
		dt.setStart("2015-09-09");
		dt.setFinish("2015-10-10");
		dt.setDailyTargetCalorie(1800.00);
		dt.setUser(user1);
		dt.setWeightLoss(10);
		List<DietTask> dt_list = new ArrayList<DietTask>();
		dt_list.add(dt);
		user1.setDietTasks(dt_list);
		userManager.addUser(user1);
		
		assertEquals(dt, userManager.getDietTasksByUsername("testAddTest").get(0));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testFindByUserName(){
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("testtest");
		userManager.addUser(user1);
		assertEquals(user1, userManager.findByUsername("testAddTest"));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testFindByFbId(){
		User user1 = new User();
		user1.setUsername("testAddTest");
		user1.setPassoword("testtest");
		user1.setFbId("testing");
		userManager.addUser(user1);
		String id = String.valueOf(user1.getId());
		assertEquals(user1, userManager.findByFbId(id));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testFormatDateToString() throws ParseException{
		String str_date = "2012-12-12";
		Date date = sdf.parse("2012-12-12");
		String result = userManager.formatDateToString(date);
		assertEquals(str_date,result);
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testAddOneDay() throws ParseException{
		Date previous = sdf.parse("2012-12-12");
		Date addOneDay = sdf.parse("2012-12-13");
		assertEquals(addOneDay, userManager.addOneDay(previous));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testOneWeekFromDay() throws ParseException{
		Date current = sdf.parse("2012-12-12");
		Date oneWeekAgo = sdf.parse("2012-12-6");
		assertEquals(oneWeekAgo, userManager.oneWeekFromDay(current));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testOneWeekAfterDay() throws ParseException{
		Date current = sdf.parse("2012-12-12");
		Date oneWeekAfter = sdf.parse("2012-12-18");
		assertEquals(oneWeekAfter, userManager.oneWeekAfterDay(current));
	}
	
	@Test
	@Transactional
	@Rollback(true)
	public void testDurationFromStart() throws ParseException{
		Date current = sdf.parse("2012-12-12");
		int duration = 20;
		Date after = sdf.parse("2013-01-01");
		assertEquals(after, userManager.durationFromStart(current, duration));
	}
}

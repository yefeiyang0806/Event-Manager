package com.fitbit.project.web;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;

import java.text.DecimalFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.web.servlet.ModelAndView;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;

import com.fitbit.project.domain.DietTask;
import com.fitbit.project.domain.FoodCalorie;
import com.fitbit.project.service.UserManager;

@Controller
@RequestMapping(value="/food")
public class FoodSummaryController {
	
	@Autowired
	private UserManager userManager;
	
	protected final Log logger = LogFactory.getLog(getClass());
	
	@RequestMapping(value="/summary")
	public ModelAndView handleRequest(HttpServletRequest request) throws ParseException{
		Map<String, Object> myModel = new HashMap<String, Object>();
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
		String displayName = userManager.createDisplayName(username);
		List<DietTask> active_dts = userManager.getActiveDietTasks(username);
		int length = 0;
		
		if (active_dts != null){
			length = active_dts.size();
			for (DietTask dt : active_dts){
				String start = dt.getStart();
				String finish = dt.getFinish();
				start = start.split(" ")[0];
				finish = finish.split(" ")[0];
				dt.setStart(start);
				dt.setFinish(finish);
			}
		}
		
		int not_start_tasks = userManager.getNotStartDietTasks(username).size();
		int expired_tasks = userManager.getExpiredDietTasks(username).size();
		
		myModel.put("displayName", displayName);
		myModel.put("active_days", userManager.getActiveDays(username));
		myModel.put("total_days", userManager.getTotalDays(username));
		myModel.put("personal_average", userManager.calcPersonalAverage(username));
		myModel.put("active_ratio", userManager.calcActiveRatio(username));
		myModel.put("monthly_calorie", userManager.getMonthlyCalorie(username));
		myModel.put("allAverage", userManager.calcAllAverageCalorie());
		myModel.put("active_dts", active_dts);
		myModel.put("length", length);
		myModel.put("expired_tasks", expired_tasks);
		myModel.put("not_start_tasks", not_start_tasks);
		logger.info("not start tasks: " + not_start_tasks);
		logger.info("expired_tasks: " + expired_tasks);
		myModel.put("eat_too_much", userManager.countEatingTooMuchTimes(username));
		return new ModelAndView("food_summary",myModel);
	}
}

package com.fitbit.project.web;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.stereotype.Controller;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.web.servlet.ModelAndView;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;

import com.fitbit.project.service.UserManager;

@Controller
@RequestMapping(value="/food")
public class ComparisonController {
	
	private Log logger = LogFactory.getLog(getClass());
	
	@Autowired
	private UserManager userManager;
	
	@RequestMapping(value="/comparison")
	public ModelAndView requestHandler(@RequestParam(value="start_date", required=false) String sDate, @RequestParam(value="finish_date", required=false) String fDate) throws ParseException{
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
		String username = auth.getName();
		com.fitbit.project.domain.User user = userManager.findByUsername(username);
	    if (user == null){
	    	return new ModelAndView("new_page");
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
	    
		Map<String, Integer> weeklyCalorie = new LinkedHashMap<String, Integer>();
		logger.info(weeklyCalorie.toString());
		Date start = null;
		Date finish = null;
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		if (sDate != null && fDate != null){
			Date start_date = sdf.parse(sDate);
			Date finish_date = sdf.parse(fDate);
			start = start_date;
			finish = finish_date;
		}
		else if (sDate == null && fDate != null){
			Date finish_date = sdf.parse(fDate);
			start = userManager.oneWeekFromDay(finish_date);
			finish = finish_date;
		}
		else if (sDate != null && fDate == null){
			Date start_date = sdf.parse(sDate);
			start = start_date;
			finish = userManager.oneWeekAfterDay(start);
		}
		else {
			Date today = new Date();
			finish = today;
			start = userManager.oneWeekFromDay(today);
		}
		weeklyCalorie = userManager.getWeeklyCalorieBetween(username, start, finish);
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("weeklyCalorie", weeklyCalorie);
		myModel.put("allAverage", userManager.calcAllAverageCalorie());
		myModel.put("displayName", displayName);
		return new ModelAndView("comparison", myModel);
	}

}

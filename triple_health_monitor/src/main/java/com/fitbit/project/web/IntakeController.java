package com.fitbit.project.web;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;

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

import com.fitbit.project.domain.FoodCalorie;
import com.fitbit.project.service.UserManager;

@Controller
@RequestMapping(value="/food")
public class IntakeController {
	
	protected final Log logger = LogFactory.getLog(getClass());
	
	@Autowired
	private UserManager userManager;
	
	@RequestMapping(value={"/", "/home"})
	public ModelAndView handleHomeRequest(HttpServletRequest request){
	    String displayName = createDisplayName();
	    return new ModelAndView("food_home", "displayName", displayName);
	}
	
	@RequestMapping(value="/intake_calorie")
	public ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response){
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    //logger.info(auth.getName());
	    //logger.info(username);
	    Boolean not_today = false;
	    Date origin_date = new Date();
	    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
	    String date = sdf.format(origin_date);
		if (request.getParameter("datepicker") != null && request.getParameter("datepicker") != ""){
			date = request.getParameter("datepicker");
			not_today = true;
			//logger.info(date);
		}
		List<FoodCalorie> food_list = new ArrayList<FoodCalorie>();
		food_list = userManager.getFoodListByUserAndDate(username, date);
		int total = 0;
		Map<String, Object> myModel = new HashMap<String, Object>();
		if (food_list != null){
			for (FoodCalorie fl : food_list){
				total += fl.getCalorie();
			}
			myModel.put("length", food_list.size());
			myModel.put("total", total);
		}
		myModel.put("food_list", food_list);
		
		if (not_today){
			myModel.put("date", date);
		}
		String displayName = createDisplayName();
		myModel.put("displayName", displayName);
		if (displayName == null){
	    	return new ModelAndView("food_home");
	    }
		return new ModelAndView("intake_calorie", myModel);
	}
	
	@RequestMapping(value="/add_food")
	public ModelAndView requestHandler(HttpServletRequest request){
		Date origin_date = new Date();
		logger.info("Post date to add_food");
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		String date = sdf.format(origin_date);
		if (request.getParameter("date") != null && request.getParameter("date") != ""){
			date = request.getParameter("date");
		}
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("date", date);
		myModel.put("displayName", displayName);
		return new ModelAndView("add_food", myModel);
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
	
}

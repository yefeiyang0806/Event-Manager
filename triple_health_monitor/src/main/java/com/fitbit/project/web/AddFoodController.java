package com.fitbit.project.web;

import javax.servlet.http.HttpServletRequest;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;

import com.fitbit.project.domain.DailyCalorie;
import com.fitbit.project.domain.FoodCalorie;
import com.fitbit.project.service.UserManager;


@Controller
@RequestMapping(value="/add_food")
public class AddFoodController {
	
	@Autowired
	private UserManager userManager;
	
	protected final Log logger = LogFactory.getLog(getClass());
	
	@RequestMapping(value="/add", method=RequestMethod.POST)
	public ModelAndView requestHandler(HttpServletRequest request) throws ParseException{
		List<FoodCalorie> foods = new ArrayList<FoodCalorie>();
		Boolean not_today = false;
		Date origin_date = new Date();
	    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
	    String date = sdf.format(origin_date);
		if (request.getParameter("datepicker") != null && request.getParameter("datepicker") != ""){
			date = request.getParameter("datepicker");
			not_today = true;
		}
		logger.info(date);
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    DailyCalorie dc = new DailyCalorie();
	    dc = userManager.getDailyCalorieByUserAndDate(username, date);
	    logger.info("Find DC by this date: "+date);
	    if (dc == null){
	    	logger.info("No DC found!!!");
	    	dc = new DailyCalorie();
	    	dc.setUser(userManager.findByUsername(username));
	    	Date target_date = sdf.parse(date);
	    	dc.setDate(target_date);
	    	userManager.addDailyCalorie(dc);
	    	//logger.info("DC ID!!!!" + dc.getId());
	    }
	    
		for (int i=0; i<8; i++){
			if (request.getParameter("food_"+i) != null && request.getParameter("calo_"+i) != null &&
					request.getParameter("food_"+i) != "" && request.getParameter("calo_"+i) != ""){
				int ca = Integer.parseInt(request.getParameter("calo_"+i));
				String food = request.getParameter("food_"+i);
				foods.add(new FoodCalorie(food,ca,dc));
			}
		}
		userManager.addFoodCalorie(foods);
		if (not_today){
			return new ModelAndView("redirect:/food/intake_calorie?datepicker="+date);
		}
		return new ModelAndView("redirect:/food/intake_calorie");
	}
	
}

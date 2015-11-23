package com.fitbit.project.web;

import java.util.Locale;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import com.fitbit.project.service.UserManager;

/**
 * Handles requests for the application home page.
 */
@Controller
public class HomeController {
	
	private static final Logger logger = LoggerFactory.getLogger(HomeController.class);

	@Autowired
	private UserManager userManager;
	
	@RequestMapping(value = {"/", "/home"}, method = RequestMethod.GET)
	public ModelAndView home(Locale locale, Model model) {
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
	    	displayName = firstName + " " + lastName;
	    }
	    else if (firstName != null && firstName != ""){
	    	displayName = firstName;
	    }
	    else if (lastName != null && lastName != ""){
	    	displayName = lastName;
	    }
		
		return new ModelAndView("new_page", "displayName", displayName);
	}
	
}

package com.fitbit.project.web;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.stereotype.Controller;

import java.util.HashMap;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.web.servlet.ModelAndView;

@Controller
@RequestMapping(value="/login/**")
public class LoginController {
	
	private Log logger = LogFactory.getLog(getClass());
	
	@RequestMapping("/")
	public ModelAndView handleRequest(
			@RequestParam(value="error", required=false) String error,
			@RequestParam(value="logout", required=false) String logout){
		
		Map<String, Object> myModel = new HashMap<String, Object>();
		if (error != null){
			logger.info("Found error!!!");
			String errorText = "Invalid username or password!";
			myModel.put("error", errorText);
		}
		if (logout != null){
			logger.info("Found logout!!!");
			String logoutText = "Thank you for using our system. See you soon.";
			myModel.put("msg", logoutText);
		}
		return new ModelAndView("login", myModel);
	}
	
	@RequestMapping(value="/new_page")
	public ModelAndView handleNewRequest(HttpServletRequest request){
		return new ModelAndView("new_page");
	}
		
}
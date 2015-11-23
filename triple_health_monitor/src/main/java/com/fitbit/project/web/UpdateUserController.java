package com.fitbit.project.web;

import javax.servlet.http.HttpServletRequest;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import javax.annotation.Resource;
import javax.validation.Valid;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.fitbit.project.domain.User;
import com.fitbit.project.service.UserManager;

@Controller
@RequestMapping(value="/user")
public class UpdateUserController {
	
	@Resource(name="userManager")
	private UserManager userManager;
	
	protected final Log logger = LogFactory.getLog(getClass());
	
	@RequestMapping(value="/update/")
	public ModelAndView requestHandler(HttpServletRequest request){
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
		String username = auth.getName();
		User user = userManager.findByUsername(username);
		Map<String, Object> myModel = new HashMap<String, Object>();
		if (user == null){
	    	return new ModelAndView("new_page");
	    }
	    String firstName = user.getFirstName();
	    String lastName = user.getLastName();
	    String displayName = userManager.createDisplayName(username);
	    if ((firstName != null && firstName != "") && (lastName != null && lastName != "")){
	    	displayName = firstName + lastName;
	    	myModel.put("last_name", lastName);
	    	myModel.put("first_name", firstName);
	    }
	    else if (firstName != null && firstName != ""){
	    	displayName = firstName;
	    	myModel.put("first_name", firstName);
	    }
	    else if (lastName != null && lastName != ""){
	    	displayName = lastName;
	    	myModel.put("last_name", lastName);
	    }
	    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
	    String birthday = sdf.format(user.getBirthday());
	    myModel.put("user", user);
	    myModel.put("birthday", birthday);
	    myModel.put("displayName", displayName);
	    return new ModelAndView("update_profile", myModel);
	    
	}
	
	@SuppressWarnings("unchecked")
	@RequestMapping(value="/update/confirm")
	public ModelAndView updateHandler(HttpServletRequest request){
		Map<String, Object> myModel = new HashMap<String, Object>();
		Set<String> error_msg = new HashSet<String>();
		User user = new User();
		Long id = Long.valueOf(request.getParameter("id"));
		String username = request.getParameter("username");
		String firstName = request.getParameter("firstName");
		String lastName = request.getParameter("lastName");
		String old_password = request.getParameter("old_password");
		String password = request.getParameter("password");
		String password2 = request.getParameter("password2");
		String gender = request.getParameter("gender");
		String birthday = request.getParameter("datepicker");
		String displayName = userManager.createDisplayName(username);
		myModel.put("displayName", displayName);
		logger.info("Birthday: " + birthday);
		Float weight = this.userManager.parseFloat(request.getParameter("weight"));
		Float height = this.userManager.parseFloat(request.getParameter("height"));
		String email = request.getParameter("email");
		myModel.put("birthday", birthday);
		
		user.setId(id);
		user.setUsername(username);
		user.setFirstName(firstName);
		user.setLastName(lastName);
		user.setEmail(email);
		user.setHeight(height);
		user.setWeight(weight);
		user.setGender(this.userManager.parseGender(gender));
		
		Boolean allowed_change_password = true;
		if (old_password != null && !old_password.equals("") && (!password.equals("") || !password2.equals(""))){
			allowed_change_password = userManager.checkPassword(username, old_password);
			if (allowed_change_password == false){
				error_msg.add("Old Password is incorrect.");
				myModel.put("error_msg", error_msg);
				myModel.put("user", user);
				return new ModelAndView("update_profile", myModel);
			}
			else if (allowed_change_password == true && !userManager.validatePassword(password, password2)){
				error_msg.add("Two password are different. Please re-enter password.");
				myModel.put("error_msg", error_msg);
				myModel.put("user", user);
				return new ModelAndView("update_profile", myModel);
			}
			else {
				user.setPassoword(password);
			}
			if (password.length()>20 || password.length()<8){
				error_msg.add("Name Format Error. Name should only contains letters.");
				myModel.put("error_msg", error_msg);
				myModel.put("user", user);
				myModel.put("old_password", old_password);
				return new ModelAndView("update_profile", myModel);
			}
		}
		else if ((old_password == null || old_password.equals("")) && (!password.equals("") || !password2.equals(""))){
			error_msg.add("Old Password is required before changing password.");
			myModel.put("error_msg", error_msg);
			myModel.put("user", user);
			return new ModelAndView("update_profile", myModel);
		}
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date new_birthday = new Date();
		try {
			new_birthday = sdf.parse(birthday);
		} catch (ParseException e) {
			e.printStackTrace();
			error_msg.add("Birthday Format Error. Please follow the datepicker format.");
			myModel.put("error_msg", error_msg);
			myModel.put("user", user);
			myModel.put("old_password", old_password);
			return new ModelAndView("update_profile", myModel);
		}
		user.setBirthday(new_birthday);
		
		Map<String, Object> validate = userManager.validateUser(user, "update");
		boolean validate_result = (Boolean)validate.get("result");
		if (validate_result){
			this.userManager.updateUser(user);
		}
		else {
			error_msg.addAll((Set<String>)validate.get("error_msg"));
			myModel.put("error_msg", error_msg);
			myModel.put("user", user);
			if (user.getPassword() != null){
				myModel.put("password2", password2);
				myModel.put("old_password", old_password);
			}
			if (request.getParameter("providerId") != null && request.getParameter("providerId").equals("facebook")){
				myModel.put("providerUserId", request.getParameter("providerUserId"));
				myModel.put("providerId", request.getParameter("providerId"));
			}
			return new ModelAndView("update_profile", myModel);
		}
		return new ModelAndView("redirect:/home/");
	}
}

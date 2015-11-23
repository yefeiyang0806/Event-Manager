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

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.fitbit.project.domain.User;
import com.fitbit.project.service.UserManager;


@Controller
@RequestMapping(value="/user")
public class CreateUserController {
	
	@Resource(name="userManager")
	private UserManager userManager;
	
	protected final Log logger = LogFactory.getLog(getClass());
	
	@SuppressWarnings("unchecked")
	@RequestMapping(value="/create")
	public ModelAndView requestHandler(HttpServletRequest request){
		Map<String, Object> myModel = new HashMap<String, Object>();
		Set<String> error_msg = new HashSet<String>();
		User user = new User();
		String username = request.getParameter("username");
		String firstName = request.getParameter("firstName");
		String lastName = request.getParameter("lastName");
		String password = request.getParameter("password");
		String password2 = request.getParameter("password2");
		String gender = request.getParameter("gender");
		Float weight = this.userManager.parseFloat(request.getParameter("weight"));
		Float height = this.userManager.parseFloat(request.getParameter("height"));
		String email = request.getParameter("email");
		
		logger.info("password 2: " + password2);
		logger.info("password1:" + password);
		
		Boolean two_password_same = this.userManager.validatePassword(password, password2);
		logger.info("Compare result:" + two_password_same);
	
		user.setUsername(username);
		user.setPassoword(password);
		user.setFirstName(firstName);
		user.setLastName(lastName);
		user.setEmail(email);
		user.setHeight(height);
		user.setWeight(weight);
		user.setGender(this.userManager.parseGender(gender));
		
		String birthday_text = request.getParameter("datepicker");
		logger.info("birthday: " + birthday_text);
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
		Date birthday = new Date();
		try {
			birthday = sdf.parse(birthday_text);
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			error_msg.add("Birthday Format Error. Please follow the datepicker format.");
			myModel.put("error_msg", error_msg);
			myModel.put("user", user);
			myModel.put("password2", password2);
			if (request.getParameter("providerId") != null && request.getParameter("providerId").equals("facebook")){
				myModel.put("providerUserId", request.getParameter("providerUserId"));
				myModel.put("providerId", request.getParameter("providerId"));
			}
			return new ModelAndView("join", myModel);
		}
		user.setBirthday(birthday);
		
		myModel.put("birthday", birthday_text);
		if (!two_password_same){
			error_msg.add("Two password are different. Please re-enter password.");
			myModel.put("error_msg", error_msg);
			myModel.put("user", user);
			myModel.put("password2", password2);
			if (request.getParameter("providerId") != null && request.getParameter("providerId").equals("facebook")){
				myModel.put("providerUserId", request.getParameter("providerUserId"));
				myModel.put("providerId", request.getParameter("providerId"));
			}
			return new ModelAndView("join", myModel);
		}
		
		Map<String, Object> validate = userManager.validateUser(user, "create");
		boolean validate_result = (Boolean)validate.get("result");
		String userId = null;
		if (validate_result){
			this.userManager.addUser(user);
			userId = String.valueOf(user.getId());
		}
		else {
			error_msg.addAll((Set<String>)validate.get("error_msg"));
			myModel.put("error_msg", error_msg);
			myModel.put("user", user);
			myModel.put("password2", password2);
			if (request.getParameter("providerId") != null && request.getParameter("providerId").equals("facebook")){
				myModel.put("providerUserId", request.getParameter("providerUserId"));
				myModel.put("providerId", request.getParameter("providerId"));
			}
			return new ModelAndView("join", myModel);
		}
		
		if (request.getParameter("providerId") != null && request.getParameter("providerId").equals("facebook") ){
			Map<String, Object> userConnection = new HashMap<String,Object>();
			userConnection.put("firstName", request.getParameter("firstName"));
			userConnection.put("lastName", request.getParameter("lastName"));
			userConnection.put("email", request.getParameter("fb_email"));
			userConnection.put("providerUserId", request.getParameter("providerUserId"));
			logger.info("ProviderUserId: "+request.getParameter("providerUserId"));
			userConnection.put("providerId", request.getParameter("providerId"));
			userConnection.put("userId", userId);
			this.userManager.addUserConnection(userConnection);
		}
		return new ModelAndView("new_page");
		
			//return new ModelAndView("login");	
	}
}

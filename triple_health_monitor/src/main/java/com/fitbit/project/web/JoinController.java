package com.fitbit.project.web;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.context.request.WebRequest;
import org.springframework.stereotype.Controller;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.social.connect.ConnectionRepository;
import org.springframework.social.connect.Connection;
import org.springframework.social.connect.ConnectionKey;
import org.springframework.social.connect.UserProfile;
import org.springframework.social.connect.jdbc.JdbcUsersConnectionRepository;
import org.springframework.social.connect.web.ProviderSignInUtils;
import org.springframework.social.facebook.api.Facebook;
import org.springframework.social.facebook.api.User;

import java.util.HashMap;
import java.util.Map;

import javax.persistence.Column;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.servlet.ModelAndView;

@Controller
@RequestMapping(value="/join")
public class JoinController {
	
	private Log logger = LogFactory.getLog(getClass());
	
	//private JdbcUsersConnectionRepository usersConnectionRepository;
	
	@RequestMapping(value="/")
	public ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response){
		return new ModelAndView("join");
	}
	
	@RequestMapping(value="/fb/")
	public ModelAndView handleFbRequest(WebRequest request){
		Connection<?> connection = ProviderSignInUtils.getConnection(request);
		
		//Connection<Facebook> connection = connectionRepository.findPrimaryConnection(Facebook.class);
		//connection = (Connection<Facebook>)connection;
	    if (connection != null) {
	    	logger.info("Got connection!");
	    	Map<String, Object> myModel = new HashMap<String, Object>();
	        UserProfile up = (connection.fetchUserProfile());
	        ConnectionKey ck = connection.getKey();
	        String firstName = up.getFirstName();
	        String lastName = up.getLastName();
	        String username = up.getUsername();
	        String email = up.getEmail();
	        String providerUserId = ck.getProviderUserId();
	        String providerId = ck.getProviderId();
	        logger.info("Got email: " + providerUserId);
	        myModel.put("username", username);
	        myModel.put("email", email);
	        myModel.put("providerUserId", providerUserId);
	        myModel.put("providerId", providerId);
	        myModel.put("firstName", firstName);
	        myModel.put("lastName", lastName);
	        return new ModelAndView("join", myModel);
	    } else {
	        return new ModelAndView("join");
	    }
	}
	
}

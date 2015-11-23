package com.fitbit.project.service;

import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.fitbit.project.domain.User;

@Service(value="activityUserManager")
@Transactional
public class ActivityUserManager {
	@Autowired
	private SessionFactory sessionFactory;
	
	@Autowired
	private UserManager userManager;
	
	public User getCurrentUser(){
		
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    User user = this.userManager.findByUsername(username);
		
		return user;
		
	}
	
}

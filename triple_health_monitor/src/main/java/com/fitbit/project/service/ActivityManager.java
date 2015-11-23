package com.fitbit.project.service;

import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.fitbit.project.domain.Activity;
import com.fitbit.project.domain.ActivityGoal;
import com.fitbit.project.domain.User;



@Service(value="activityManager")
@Transactional
public class ActivityManager {
	@Autowired
	private SessionFactory sessionFactory;
	
	@Autowired
	private UserManager userManager;
	
	private final Log logger = LogFactory.getLog(getClass());
	
	
	public void importActivityData(Activity activity){
		
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    User user = this.userManager.findByUsername(username);
	    activity.setUser(user);
		this.sessionFactory.getCurrentSession().save(activity);
		
	}
	
	public List<Activity> getActivities(){
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    User user = this.userManager.findByUsername(username);
		//Hibernate.initialize(user.getActivityGoals());
	    
		List<Activity> activity = null;
		logger.info(user.getActivities().size());
		if(user.getActivities().size()==0){
				activity.add(new Activity());
				return activity;
				
		}
		else{
				activity = user.getActivities();
				
		}
		return activity; 

	}
}

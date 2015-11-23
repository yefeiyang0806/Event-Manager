package com.fitbit.project.service;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hibernate.Hibernate;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.fitbit.project.domain.ActivityGoal;
import com.fitbit.project.domain.User;


@Service(value="activityGoalManager")
@Transactional
public class ActivityGoalManager {

	@Autowired
	private SessionFactory sessionFactory;
	
	@Autowired
	private UserManager userManager;
	
	private final Log logger = LogFactory.getLog(getClass());
	
	public void setGoal(ActivityGoal goal){
		
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    User user = this.userManager.findByUsername(username);
	    Date now = new java.util.Date();
	    goal.setUser(user);
	    goal.setTime(now);
		this.sessionFactory.getCurrentSession().save(goal);

	}
	
	public ActivityGoal getGoalById(long id){
		
		Session currentSession = this.sessionFactory.getCurrentSession();
		ActivityGoal activityGoal = (ActivityGoal)currentSession.get(ActivityGoal.class, id);  
		return activityGoal;
	}
	
	public List<ActivityGoal> getGoalByUser(){
		
		Authentication auth = SecurityContextHolder.getContext().getAuthentication();
	    String username = auth.getName();
	    User user = this.userManager.findByUsername(username);
		//Hibernate.initialize(user.getActivityGoals());
//		ActivityGoal goal;
		List<ActivityGoal> activityGoals;
		logger.info(user.getActivityGoals().size());
//		if(user.getActivityGoals().size()==0){
//				goal = new ActivityGoal();
//				return goal;
//				
//		}
//		else{
				activityGoals = user.getActivityGoals();
//				int count = activityGoals.size();
//				goal= activityGoals.get(count-1);
//		}
		return activityGoals; 

	}
}

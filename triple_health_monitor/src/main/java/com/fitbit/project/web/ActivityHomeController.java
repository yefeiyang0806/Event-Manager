package com.fitbit.project.web;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.fitbit.project.domain.Activity;
import com.fitbit.project.domain.ActivityGoal;
import com.fitbit.project.domain.User;
import com.fitbit.project.service.ActivityGoalManager;
import com.fitbit.project.service.ActivityManager;
import com.fitbit.project.service.ActivityUserManager;
import com.fitbit.project.service.UserManager;


@Controller
@RequestMapping(value="/activity")
public class ActivityHomeController {
	
	@Autowired
	private ActivityGoalManager activityGoalManager;
	
	@Autowired
	private ActivityUserManager activityUserManager;
	
	@Autowired
	private ActivityManager activityManager;
	
	@Autowired
	private UserManager userManager;
	

	@RequestMapping(value="")
	public ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response){
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("displayName", displayName);
		return new ModelAndView("activity_home", myModel);
	}
	
	@RequestMapping(value="/user_profile")
	public ModelAndView getUserProfile(HttpServletRequest request, HttpServletResponse response){
		String now = (new java.util.Date()).toString();
        Map<String, Object> myModel = new HashMap<String, Object>();
        myModel.put("now", now);
        myModel.put("user", this.activityUserManager.getCurrentUser());
        return new ModelAndView("user_profile", myModel);
	}
	
	@RequestMapping(value="/trophy_room")
	public ModelAndView getTrophyRoom(HttpServletRequest request, HttpServletResponse response){
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("displayName", displayName);
		return new ModelAndView("trophy_room", myModel);
	}
	
	@RequestMapping(value="/activity", method=RequestMethod.GET)
	public ModelAndView getTrackActivity(Model uiModel){
		List<Activity> activities = activityManager.getActivities();
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("displayName", displayName);
		myModel.put("activities", activities);
		return new ModelAndView("track_activity", myModel);
	}
	
	@RequestMapping(value="/goal", method=RequestMethod.GET)
	public ModelAndView getGoals(Model uiModel){
		List<ActivityGoal> goals = this.activityGoalManager.getGoalByUser();
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		myModel.put("displayName", displayName);
		myModel.put("goals", goals);
		return new ModelAndView("display_goal", myModel);	
	}
	
	
	@RequestMapping(value="/goal/{id}", method=RequestMethod.GET)
	public String getGoal(@PathVariable("id") Long id, Model uiModel){
		ActivityGoal activityGoal = this.activityGoalManager.getGoalById(id);
		uiModel.addAttribute("goal", activityGoal);
		
		return "set_goal_success";
	}
	
	
	
	@RequestMapping(value="/set_goal", method=RequestMethod.GET)
	public ModelAndView setGoal(Model uiModel){
		
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		ActivityGoal goal = new ActivityGoal();
		myModel.put("displayName", displayName);
		myModel.put("goal", goal);
		return new ModelAndView("set_goal", myModel);	
	}
	
	
	@RequestMapping(value="/set_goal", method=RequestMethod.POST)
	public String setGoal(@Valid ActivityGoal goal, final RedirectAttributes redirectAttributes){
		String displayName = createDisplayName();
		Map<String, Object> myModel = new HashMap<String, Object>();
		redirectAttributes.addFlashAttribute("displayName", displayName);
		redirectAttributes.addFlashAttribute("css","success");
		redirectAttributes.addFlashAttribute("msg","Goal create Success!");
		this.activityGoalManager.setGoal(goal);
//		myModel.put("goal",activityGoalManager.getGoalById(goal.getId()));
		return "redirect:/activity/goal/" + goal.getId();
		
	}
	
	@RequestMapping(value="/importdata", method=RequestMethod.GET)
	public ModelAndView importActvityData(Model uiModel){
		 Activity activity = new Activity();
		 String displayName = createDisplayName();
		 Map<String, Object> myModel = new HashMap<String, Object>();
		 myModel.put("displayName", displayName);
		 myModel.put("activity", activity);
		 return new ModelAndView("importdata", myModel);		
	}
	
	@RequestMapping(value="/importdata", method=RequestMethod.POST)
	public String importActvityData(@Valid Activity activity){

		this.activityManager.importActivityData(activity);
		return "redirect:/activity/track_activity";
		
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
	    	displayName = firstName + lastName;
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

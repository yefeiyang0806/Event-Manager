package com.fitbit.project.web;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import com.fitbit.project.domain.SleepTime;
import com.fitbit.project.domain.SleepTimeChart;
import com.fitbit.project.service.SleepTimeManager;
import com.fitbit.project.service.UserManager;


@Controller
@RequestMapping(value = "/")
public class SleepTrackController {
	
	@Autowired
	private UserManager userManager;
	
	@Autowired
	private SleepTimeManager sleepTimeManager;
	
	@RequestMapping(value = "/sleeptime")
	public ModelAndView handleRequest() {
		return new ModelAndView("sleeptime");
	}
	
	@RequestMapping(value = "/sleeptime/getdata")
	@ResponseBody
	public List<SleepTimeChart> getData(@RequestParam("from") String from, @RequestParam("to") String to) throws Exception {
		return sleepTimeManager.getSleepTimeData(1, from, to);
	}

}

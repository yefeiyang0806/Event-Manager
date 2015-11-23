package com.fitbit.project.service;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.fitbit.project.domain.*;

@Service(value="sleepTimeManager")
@Transactional
public class SleepTimeManager {
	
	@Autowired
	private SessionFactory sessionFactory;
	
	public void setSessionFactory(SessionFactory sf){
		this.sessionFactory = sf;
	}
	
	@SuppressWarnings("unchecked")
	public List<SleepTime> findUserSleepData (long userId, String from, String to) throws Exception {
		List<SleepTime> times = new ArrayList<SleepTime>();
		DateFormat df = new SimpleDateFormat("yy-MM-dd"); 
		if (from != "" && to != "") {
			Date dateFrom = df.parse(from);
			Date dateTo = df.parse(to);
			times = sessionFactory.getCurrentSession()
					.createQuery("from SleepTime where User_Id=? and date>=? and date<=?")
					.setParameter(0, userId)
					.setParameter(1, dateFrom)
					.setParameter(2, dateTo)
					.list();
		}
		else {
			times = sessionFactory.getCurrentSession()
				.createQuery("from SleepTime where User_Id=?")
				.setParameter(0, userId)
				.list();
		}

		return times;
	}
	
	public List<SleepTimeChart> getSleepTimeData(long userId, String from, String to) throws Exception {
		List<SleepTime> times = findUserSleepData(userId, from, to);
		List<SleepTimeChart> data = new ArrayList<SleepTimeChart>();
		for (SleepTime time : times) {
			data.add(new SleepTimeChart(time.getDate().getTime(), time.getDuration()));
		}
		return data;
	}
	
}

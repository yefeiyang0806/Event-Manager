package com.fitbit.project.domain;

public class SleepTimeChart {
	
	private long date;
	private int duration;
	
	public SleepTimeChart() { }
	
	public SleepTimeChart(long date, int duration) {
		this.date = date;
		this.duration = duration;
	}
	
	public long getDate() {
		return date;
	}
	
	public void setDate(long date) {
		this.date = date;
	}
	
	public int getDuration() {
		return duration;
	}
	
	public void setDuration(int duration) {
		this.duration = duration;
	}

}

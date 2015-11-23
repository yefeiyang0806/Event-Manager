package com.fitbit.project.domain;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.JoinColumn;
import javax.persistence.Id;
import javax.persistence.Table;

import com.fitbit.project.domain.FoodCalorie;
import com.fitbit.project.domain.User;

import javax.persistence.OneToMany;
import javax.persistence.ManyToOne;

@Entity
@Table(name="SleepTime")
public class SleepTime implements Serializable {
	
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@Column(name="date")
	private Date date;
	
	@Column(name="start_time")
	private Date startTime;
	
	@Column(name="duration")
	private int duration;
	
	@Column(name="goal")
	private int goal;
	
	@ManyToOne
	@JoinColumn(name="User_Id", nullable=false)
	private User user;

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public Date getDate() {
		return date;
	}

	public void setDate(Date date) {
		this.date = date;
	}

	public Date getStartTime() {
		return startTime;
	}

	public void setStartTime(Date startTime) {
		this.startTime = startTime;
	}

	public int getDuration() {
		return duration;
	}

	public void setDuration(int duration) {
		this.duration = duration;
	}

	public int getGoal() {
		return goal;
	}

	public void setGoal(int goal) {
		this.goal = goal;
	}

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}
	
}

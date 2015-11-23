package com.fitbit.project.domain;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name="ActivityGoal")
public class ActivityGoal implements Serializable {
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@ManyToOne
	@JoinColumn(name="User_Id", nullable=false)
	private User user;
	
	@Column(name="CaloriesOut")
	private int caloriesOut;
	
	@Column(name="Distance")
	private Float distance;
	
	@Column(name="Floors")
	private int floors;
	
	@Column(name="Steps")
	private int steps;
	
	@Column(name="Period")
	private String period;
	
	@Column(name="Time")
	private Date time;

	public long getId() {
		return id;
	}

	public Date getTime() {
		return time;
	}

	public void setTime(Date time) {
		this.time = time;
	}

	public void setId(long id) {
		this.id = id;
	}

	public User getUser() {
		return user;
	}

	public void setUser(User user) {
		this.user = user;
	}

	public int getCaloriesOut() {
		return caloriesOut;
	}

	public void setCaloriesOut(int caloriesOut) {
		this.caloriesOut = caloriesOut;
	}

	public Float getDistance() {
		return distance;
	}

	public void setDistance(Float distance) {
		this.distance = distance;
	}

	public int getFloors() {
		return floors;
	}

	public void setFloors(int floors) {
		this.floors = floors;
	}

	public int getSteps() {
		return steps;
	}

	public void setSteps(int steps) {
		this.steps = steps;
	}

	public String getPeriod() {
		return period;
	}

	public void setPeriod(String period) {
		this.period = period;
	}
	
	

}

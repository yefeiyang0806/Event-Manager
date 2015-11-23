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
@Table(name="Activity")
public class Activity implements Serializable {
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@ManyToOne
	@JoinColumn(name="User_Id", nullable=false)
	private User user;
	
	@Column(name="ActivityParentId")
	private int activityParentId;
	
	@Column(name="Calories")
	private int calories;
	
	@Column(name="Description")
	private String description;
	
	@Column(name="Distance")
	private float distance;
	
	@Column(name="Duration")
	private int duration;
	
	@Column(name="HasStartTime")
	private String hasStartTime;

	@Column(name="IsFavorite")
	private String isFavorite;
	
	@Column(name="LogId")
	private int logId;
	
	@Column(name="Name")
	private String name;
	
	@Column(name="StartTime")
	private String startTime;
	
	@Column(name="Steps")
	private int steps;
	
	@Column(name="Date")
	private Date date;
	
	@Column(name="CaloriesBMR")
	private int caloriesBMR;
	
	@Column(name="CaloriesOut")
	private int caloriesOut;
	
	@Column(name="Elevation")
	private float elevation;
	
	@Column(name="FairlyActiveMinutes")
	private int fairlyActiveMinutes;
	
	@Column(name="Floors")
	private int floors;
	
	@Column(name="LightlyActiveMinutes")
	private int lightlyActiveMinutes;
	
	@Column(name="MarginalCalories")
	private int marginalCalories;
	
	@Column(name="SedentaryMinutes")
	private int sedentaryMinutes;
	
	@Column(name="VeryActiveMinutes")
	private int veryActiveMinutes;

	public long getId() {
		return id;
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

	public int getActivityParentId() {
		return activityParentId;
	}

	public void setActivityParentId(int activityParentId) {
		this.activityParentId = activityParentId;
	}

	public int getCalories() {
		return calories;
	}

	public void setCalories(int calories) {
		this.calories = calories;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public float getDistance() {
		return distance;
	}

	public void setDistance(float distance) {
		this.distance = distance;
	}

	public int getDuration() {
		return duration;
	}

	public void setDuration(int duration) {
		this.duration = duration;
	}

	public String getHasStartTime() {
		return hasStartTime;
	}

	public void setHasStartTime(String hasStartTime) {
		this.hasStartTime = hasStartTime;
	}

	public String getIsFavorite() {
		return isFavorite;
	}

	public void setIsFavorite(String isFavorite) {
		this.isFavorite = isFavorite;
	}

	public int getLogId() {
		return logId;
	}

	public void setLogId(int logId) {
		this.logId = logId;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getStartTime() {
		return startTime;
	}

	public void setStartTime(String startTime) {
		this.startTime = startTime;
	}

	public int getSteps() {
		return steps;
	}

	public void setSteps(int steps) {
		this.steps = steps;
	}

	public Date getDate() {
		return date;
	}

	public void setDate(Date date) {
		this.date = date;
	}

	public int getCaloriesBMR() {
		return caloriesBMR;
	}

	public void setCaloriesBMR(int caloriesBMR) {
		this.caloriesBMR = caloriesBMR;
	}

	public int getCaloriesOut() {
		return caloriesOut;
	}

	public void setCaloriesOut(int caloriesOut) {
		this.caloriesOut = caloriesOut;
	}

	public float getElevation() {
		return elevation;
	}

	public void setElevation(float elevation) {
		this.elevation = elevation;
	}

	public int getFairlyActiveMinutes() {
		return fairlyActiveMinutes;
	}

	public void setFairlyActiveMinutes(int fairlyActiveMinutes) {
		this.fairlyActiveMinutes = fairlyActiveMinutes;
	}

	public int getFloors() {
		return floors;
	}

	public void setFloors(int floors) {
		this.floors = floors;
	}

	public int getLightlyActiveMinutes() {
		return lightlyActiveMinutes;
	}

	public void setLightlyActiveMinutes(int lightlyActiveMinutes) {
		this.lightlyActiveMinutes = lightlyActiveMinutes;
	}

	public int getMarginalCalories() {
		return marginalCalories;
	}

	public void setMarginalCalories(int marginalCalories) {
		this.marginalCalories = marginalCalories;
	}

	public int getSedentaryMinutes() {
		return sedentaryMinutes;
	}

	public void setSedentaryMinutes(int sedentaryMinutes) {
		this.sedentaryMinutes = sedentaryMinutes;
	}

	public int getVeryActiveMinutes() {
		return veryActiveMinutes;
	}

	public void setVeryActiveMinutes(int veryActiveMinutes) {
		this.veryActiveMinutes = veryActiveMinutes;
	}	
	
}

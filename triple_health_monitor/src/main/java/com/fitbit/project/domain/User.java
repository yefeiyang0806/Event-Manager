package com.fitbit.project.domain;

import java.io.Serializable;
import java.util.List;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import com.fitbit.project.domain.DietTask;

import javax.persistence.OneToMany;;

@Entity
@Table(name="User")
public class User implements Serializable{
	
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@Column(name="DoB")
	private Date birthday;
	
	@Column(name="FirstName")
	private String firstName;
	
	@Column(name="LastName")
	private String lastName;
	
	@Column(name="Height")
	private Float height;
	
	@Column(name="Weight")
	private Float weight;
	
	//Gender: 0 for female and 1 for male;
	@Column(name="Gender")
	private Boolean gender;
	
	@Column(name="Email", unique=true)
	private String email;
	
	@Column(name="Username", unique=true)
	private String username;
	
	@Column(name="Password")
	private String password;
	
	@Column(name="FB_id", unique=true)
	private String fb_id;
	
	@Column(name="Enabled")
	private Boolean enabled = true;
	
	@Column(name="Role")
	private String role = "USER";
	
	@OneToMany(mappedBy="user")
	private List<DietTask> dietTasks;
	
	@OneToMany(mappedBy="user")
	private List<DailyCalorie> dailyCalorie;
	
	@OneToMany(mappedBy="user")
	private List<Activity> activities;
	
	@OneToMany(mappedBy="user")
	private List<ActivityGoal> activityGoals;

	@OneToMany(mappedBy="user")
	private List<SleepTime> sleepTime;

	

	public List<Activity> getActivities() {
		return activities;
	}

	public void setActivities(List<Activity> activities) {
		this.activities = activities;
	}

	public List<ActivityGoal> getActivityGoals() {
		return activityGoals;
	}

	public void setActivityGoals(List<ActivityGoal> activityGoals) {
		this.activityGoals = activityGoals;
	}	
	
	public long getId(){
		return this.id;
	}
	
	public void setId(long id){
		this.id = id;
	}
	
	public Date getBirthday(){
		return this.birthday;
	}
	
	public void setBirthday(Date birthday){
		this.birthday = birthday;
	}
	
	public Float getHeight(){
		return this.height;
	}
	
	public void setHeight(Float height){
		this.height = height;
	}
	
	public Float getWeight(){
		return this.weight;
	}
	
	public void setWeight(Float weight){
		this.weight = weight;
	}
	
	public Boolean getGender(){
		return this.gender;
	}
	
	public void setGender(Boolean gender){
		this.gender = gender;
	}
	
	public String getEmail(){
		return this.email;
	}
	
	public void setEmail(String email){
		this.email = email;
	}
	
	public String getUsername(){
		return this.username;
	}
	
	public void setUsername(String username){
		this.username = username;
	}
	
	public String getFirstName(){
		return this.firstName;
	}
	
	public void setFirstName(String firstName){
		this.firstName = firstName;
	}
	
	public String getLastName(){
		return this.lastName;
	}
	
	public void setLastName(String lastName){
		this.lastName = lastName;
	}
	
	public String getPassword(){
		return this.password;
	}
	
	public void setPassoword(String password){
		this.password = password;
	}
	
	public Boolean getEnabled(){
		return this.enabled;
	}
	
	public void setEnabled(Boolean enabled){
		this.enabled = enabled;
	}
	
	public String getRole(){
		return this.role;
	}
	
	public void setRole(String role){
		this.role = role;
	}
	
	public String getFbId(){
		return this.fb_id;
	}
	
	public void setFbId(String fb_id){
		this.fb_id = fb_id;
	}
	
	public List<DietTask> getDietTasks(){
		return this.dietTasks;
	}
	
	public void setDietTasks(List<DietTask> dietTasks){
		this.dietTasks = dietTasks;
	}
	
	public List<DailyCalorie> getDailyCalorie(){
		return this.dailyCalorie;
	}
	
	public void setDailyCalorie(List<DailyCalorie> dailyCalorie){
		this.dailyCalorie = dailyCalorie;
	}

	public List<SleepTime> getSleepTime() {
		return sleepTime;
	}

	public void setSleepTime(List<SleepTime> sleepTime) {
		this.sleepTime = sleepTime;
	}
}
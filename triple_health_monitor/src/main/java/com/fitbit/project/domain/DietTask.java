package com.fitbit.project.domain;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import com.fitbit.project.domain.User;

@Entity
@Table(name="DietTask")
public class DietTask implements Serializable{
	
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@Column(name="Duration")
	private int duration;
	
	@Column(name="WeightLoss")
	private float weightLoss;
	
	@Column(name="Start")
	private String start;
	
	@Column(name="Finish")
	private String finish;
	
	@Column(name="State")
	private String state;
	
	@Column(name="DailyTargetCalorie")
	private double dailyTargetCalorie;
	
	@ManyToOne
	@JoinColumn(name="User_Id", nullable=false)
	private User user;
	
	private final static float CALORIE_PER_KILO = 7700;
	
	public long getId(){
		return this.id;
	}
	
	public void setId(long id){
		this.id = id;
	}
	
	public int getDuration(){
		return this.duration;
	}
	
	public void setDuration(int duration){
		this.duration = duration;
	}
	
	public float getWeightLoss(){
		return this.weightLoss;
	}
	
	public void setWeightLoss(float weightLoss){
		this.weightLoss = weightLoss;
	}
	
	public String getStart(){
		return this.start;
	}
	
	public void setStart(String start){
		this.start = start;
	}
	
	public String getFinish(){
		return this.finish;
	}
	
	public void setFinish(String finish){
		this.finish = finish;
	}
	
	public String getState(){
		return this.state;
	}
	
	public void setState(String state){
		this.state = state;
	}
	
	public double getDailyTargetCalorie(){
		return this.dailyTargetCalorie;
	}
	
	public void setDailyTargetCalorie(double calorie){
		this.dailyTargetCalorie = calorie;
	}
	
	public User getUser(){
		return this.user;
	}
	
	public void setUser(User user){
		this.user = user;
	}
	
}

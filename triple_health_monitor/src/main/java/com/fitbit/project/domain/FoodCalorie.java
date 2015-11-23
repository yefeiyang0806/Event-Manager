package com.fitbit.project.domain;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import com.fitbit.project.domain.DailyCalorie;

@Entity
@Table(name="FoodCalorie")
public class FoodCalorie implements Serializable {
	
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@Column(name="Food")
	private String food;
	
	@Column(name="Calorie")
	private int calorie;
	
	@ManyToOne
	@JoinColumn(name="DailyCalorie_Id", nullable=false)
	private DailyCalorie dailyCalorie;
	
	public FoodCalorie(){
		
	}
	
	public FoodCalorie(String food, int calorie, DailyCalorie dc){
		this.food = food;
		this.calorie = calorie;
		this.dailyCalorie = dc;
	}
	
	public long getId(){
		return this.id;
	}
	
	public void setId(long id){
		this.id = id;
	}
	
	public String getFood(){
		return this.food;
	}
	
	public void setFood(String food){
		this.food = food;
	}
	
	public int getCalorie(){
		return this.calorie;
	}
	
	public void setCalorie(int calorie){
		this.calorie = calorie;
	}
	
	public DailyCalorie getDailyCalorie(){
		return this.dailyCalorie;
	}
	
	public void setDailyCalorie (DailyCalorie dailyCalorie){
		this.dailyCalorie = dailyCalorie;
	}
}

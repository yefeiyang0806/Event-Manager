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
@Table(name="DailyCalorie")
public class DailyCalorie implements Serializable {
	
	@Id
	@GeneratedValue
	@Column(name="Id")
	private long id;
	
	@Column(name="date")
	private Date date;
	
	@OneToMany(mappedBy="dailyCalorie")
	private List<FoodCalorie> foodCalorie;
	
	@ManyToOne
	@JoinColumn(name="User_Id", nullable=false)
	private User user;
	
	public long getId(){
		return this.id;
	}
	
	public void setId(long id){
		this.id = id;
	}
	
	public Date getDate(){
		return this.date;
	}
	
	public void setDate (Date date){
		this.date = date;
	}
	
	public List<FoodCalorie> getFoodCalorie(){
		return this.foodCalorie;
	}
	
	public FoodCalorie getFoodCalorie(int index){
		if (index>=this.foodCalorie.size()){
			return null;
		}
		else {
			return this.foodCalorie.get(index);
		}
	}
	
	public void setFoodCalorie (List<FoodCalorie> foodCalorie){
		this.foodCalorie = foodCalorie;
	}
	
	public void setFoodCalorie(FoodCalorie singleFood){
		this.foodCalorie.add(singleFood);
	}
	
	public User getUser(){
		return this.user;
	}
	
	public void setUser(User user){
		this.user = user;
	}
	
	
}

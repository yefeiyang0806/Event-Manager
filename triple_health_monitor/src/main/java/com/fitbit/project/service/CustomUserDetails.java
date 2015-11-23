package com.fitbit.project.service;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.social.security.SocialUser;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

public class CustomUserDetails extends SocialUser {
	
	private String email;
	private Date birthday;
	private Boolean gender;
	private Float weight;	
	private Float height;
	private String role;
	private String fb_id;
	
	public Float getHeight(){
		return height;
	}
	
	public String getRole(){
		return role;
	}
	
	public Float getWeight(){
		return weight;
	}
	
	public Boolean getGender(){
		return gender;
	}
	
	public Date getBirthday(){
		return birthday;
	}
	
	public String getEmail(){
		return email;
	}
	
	public String getFbId(){
		return fb_id;
	}
	
	public CustomUserDetails(String username, String password, Collection<? extends GrantedAuthority> authorities) {
        super(username, password, authorities);
	}
	
	public static Builder getBuilder(){
		return new Builder();
	}
	
	public static class Builder {
		private String email;
		private Date birthday;
		private Boolean gender;
		private Float weight;	
		private Float height;
		private String role;
		private String fb_id;
		private String username;
		private String password;
		private List<GrantedAuthority> authorities;
		
		public Builder() {
            this.authorities = new ArrayList<GrantedAuthority>();
        }
		
		public Builder email(String email){
			this.email = email;
			return this;
		}
		
		public Builder birthday(Date birthday){
			this.birthday = birthday;
			return this;
		}
		
		public Builder gender(Boolean gender){
			this.gender = gender;
			return this;
		}
		
		public Builder weight (Float weight){
			this.weight = weight;
			return this;
		}
		
		public Builder height (Float height){
			this.height = height;
			return this;
		}
		
		public Builder role (String role){
			SimpleGrantedAuthority authority = new SimpleGrantedAuthority(role);
            this.authorities.add(authority);
            return this;
		}
		
		public Builder fb_id (String fb_id){
			this.fb_id = fb_id;
			return this;
		}
		
		public Builder username(String username){
			this.username = username;
			return this;
		}
		
		public Builder password (String password){
			if (password == null){
				password = "SocialUser";
			}
			this.password = password;
			return this;
		}
		
		public CustomUserDetails build(){
			CustomUserDetails cud = new CustomUserDetails(this.username, this.password, this.authorities);
			cud.birthday = birthday;
			cud.email = email;
			cud.fb_id = fb_id;
			cud.gender = gender;
			cud.height = height;
			cud.weight = weight;
			cud.role = role;
			return cud;
		}
		
	}
}

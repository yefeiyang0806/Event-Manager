package com.fitbit.project.domain;

import java.io.Serializable;
import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name="UserConnection")
public class UserConnection implements Serializable {
	
	@EmbeddedId
	private UserAndProvider userAndProvider;
	
	@Column(name="rank")
	private int rank = 1;
	
	@Column(name="accessToken")
	private String accessToken = "hello";
	
	public void setRank(int rank){
		this.rank = rank;
	}
	
	public int getRank(){
		return this.rank;
	}
	
	public void setAccessToken(String accessToken){
		this.accessToken = accessToken;
	}
	
	public String getAccessToken(){
		return this.accessToken;
	}
	
	public void setUserAndProvider(UserAndProvider uap){
		this.userAndProvider = uap;
	}
	
	public UserAndProvider getUserAndProvider(){
		return this.userAndProvider;
	}
	
	@Embeddable
	public class UserAndProvider implements Serializable{
		@Column(name="userId")
		private String userId;
		
		@Column(name="providerId")
		private String providerId;
		
		@Column(name="providerUserId")
		private String providerUserId;
		
		public void setUserId(String userId){
			this.userId = userId;
		}
		
		public String getUserId(){
			return this.userId;
		}
		
		public void setProviderId(String providerId){
			this.providerId = providerId;
		}
		
		public String getProviderId(){
			return this.providerId;
		}
		
		public void setProviderUserId(String providerUserId){
			this.providerUserId = providerUserId;
		}
		
		public String getProviderUserId(){
			return this.providerUserId;
		}
	}

}

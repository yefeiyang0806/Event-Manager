package com.fitbit.project.service;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.social.security.SocialUserDetails;
import org.springframework.social.security.SocialUserDetailsService;
import org.springframework.social.security.SocialUser;
import org.springframework.stereotype.Service;

@Service("mySocialUserDetailsService")
public class FbSocialUserDetailsService implements SocialUserDetailsService{

	@Autowired
	@Qualifier("userManager")
	private UserManager userManager;
	
	/*
	 * Currently useless since the FB would check fb_id while the local login checks username.
	 * */
	
	/*private UserDetailsService userDetailsService;
 
	public FbSocialUserDetailsService(UserDetailsService userDetailsService){
		this.userDetailsService = userDetailsService;
	}*/
	
	private Log logger = LogFactory.getLog(getClass());
	
	@Override
	public CustomUserDetails loadUserByUserId(final String userId) throws UsernameNotFoundException{
		com.fitbit.project.domain.User user = userManager.findByFbId(userId);
		logger.info("FBSOCIAL userID: " + userId);
		//if (user == null){
			//com.fitbit.project.domain.User fb_user = new com.fitbit.project.domain.User();
			//fb_user.setRole("USER");
			//fb_user.setFbId(userId);
			//userManager.addUser(fb_user);
			//user = fb_user;
		//}
		CustomUserDetails cud = CustomUserDetails.getBuilder()
				.email(user.getEmail())
				.gender(user.getGender())
				.birthday(user.getBirthday())
				.fb_id(user.getFbId())
				.height(user.getHeight())
				.weight(user.getWeight())
                .password(user.getPassword())
                .role(user.getRole())
                .username(user.getUsername())
                .build();
		return cud;
	}
	
	public void setUserManager(UserManager userManager){
		this.userManager = userManager;
	}
	
	private User buildUserForAuthentication(com.fitbit.project.domain.User user, List<GrantedAuthority> authorities){
		return new User(user.getUsername(), user.getPassword(), user.getEnabled(), true, true, true, authorities);
	}
}

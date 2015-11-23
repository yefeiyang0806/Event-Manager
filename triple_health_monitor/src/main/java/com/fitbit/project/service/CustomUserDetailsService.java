package com.fitbit.project.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.fitbit.project.service.UserManager;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;;

@Service("myUserDetailsService")
public class CustomUserDetailsService implements UserDetailsService {
	
	@Autowired
	@Qualifier("userManager")
	private UserManager userManager;
	
	private Log logger = LogFactory.getLog(getClass());
	
	@Override
	public UserDetails loadUserByUsername(final String username)throws UsernameNotFoundException {
		logger.info("I'me here");
		com.fitbit.project.domain.User user = userManager.findByUsername(username);
		logger.info("My role: "+user.getRole());
		//SimpleGrantedAuthority userAuth = new SimpleGrantedAuthority(user.getRole());
		//List<GrantedAuthority> authorities = new ArrayList<GrantedAuthority>();
		//authorities.add(userAuth);
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
	
	//private User buildUserForAuthentication(com.fitbit.project.domain.User user, List<GrantedAuthority> authorities){
	//	return new User(user.getUsername(), user.getPassword(), user.getEnabled(), true, true, true, authorities);
	//}
	
}

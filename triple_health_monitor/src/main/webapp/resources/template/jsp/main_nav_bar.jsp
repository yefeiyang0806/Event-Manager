<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>	
	<div class="navbar-wrapper">
      <div class="container">

        <nav class="navbar navbar-inverse navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/project/home/">Triple Health Monitor</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li class="active"><a href="/project/home/">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Service Categories <span class="caret"></span></a>
                  <ul class="dropdown-menu">
                    <li><a href="/project/activity/">Activities</a></li>
                    <li><a href="/project/food/home/">Food Intake</a></li>
                    <li><a href="/project/sleeptime/">Sleep Track</a></li>
                    <li role="separator" class="divider"></li>
                    <li class="dropdown-header">Account Info</li>
                    <li><a href="/project/user/update/">Update Profile</a></li>
                    <li><a href="#">One more separated link</a></li>
                  </ul>
                </li>
              </ul>
              
              
              <ul class="nav navbar-nav navbar-right">
              <c:if test="${ empty displayName }">
        		<li><p class="navbar-text">Already have an account?</p></li>
        		<li class="dropdown">
          		  <a href="#" class="dropdown-toggle" data-toggle="dropdown"><b>Login</b> <span class="caret"></span></a>
					<ul id="login-dp" class="dropdown-menu">
					  <li>
					 	<div class="row">
						  <div class="col-md-12">
							Login via
							  <div class="social-buttons">
								<a href="${pageContext.request.contextPath}/auth/facebook" class="btn btn-fb"><i class="fa fa-facebook"></i> Facebook</a>
								<!--  a href="#" class="btn btn-tw"><i class="fa fa-twitter"></i> Twitter</a>-->
							  </div>
                              or
							  <form class="form" role="form" method="post" action="/project/j_spring_security_check" method='POST' accept-charset="UTF-8" id="login-nav">
								<div class="form-group">
								  <label class="sr-only" for="exampleInputEmail2">Username</label>
								  <input type="text" class="form-control" name="username" placeholder="Username" required>
								</div>
								<div class="form-group">
								  <label class="sr-only" for="exampleInputPassword2">Password</label>
								  <input type="password" class="form-control" name="password" placeholder="Password" required>
                                  <div class="help-block text-right"><a href="">Forget the password ?</a></div>
								</div>
								<div class="form-group">
								  <button type="submit" class="btn btn-primary btn-block">Sign in</button>
								</div>
							  </form>
							</div>
							<div class="bottom text-center">
								New here ? <a href="/project/join/"><b>Join Us</b></a>
							</div>
					 	  </div>
						</li>
					  </ul>
              	</li>
              	</c:if>
              	<c:if test="${ not empty displayName }">
              		<li><p class="navbar-text">Hello, ${displayName} </p></li>
              		<li><a href="/project/j_spring_security_logout">Logout</a></li>
              	</c:if>
              </ul>
            </div>
          </div>
        </nav>

      </div>
    </div>
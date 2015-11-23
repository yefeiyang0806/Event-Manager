<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Join--Triple Health Monitor</title>

    <!-- Bootstrap -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">
    <link href="<c:url value="/resources/template/css/carousel.css" />" rel="stylesheet">
    
    <!-- jQuery -->
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
  	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  	<script src="<c:url value="/resources/bootstrap-3.3.5-dist/js/bootstrap.min.js" />"></script>
    
    <script>
  		$(function() {
  	    	$( "#datepicker" ).datepicker({ minDate: "-70Y", maxDate: "0", dateFormat: "yy-mm-dd",changeMonth: true, changeYear: true});
  	  	});
  	</script>
  	
  	<style type="text/css">
  		.colorgraph {
  			height: 5px;
  			border-top: 0;
  			background: #c4e17f;
  			border-radius: 5px;
  			background-image: -webkit-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
  			background-image: -moz-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
  			background-image: -o-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
  			background-image: linear-gradient(to right, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
		}
		
  	</style>
    
  </head>
  <body>
	<c:import url='/resources/template/jsp/main_nav_bar.jsp' />
    <div class="mw">
	<div class="container">
	<br /><br /><br /><br />
	  <div class="row">
	    <div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
		  <form role="form" method=POST action="/project/user/update/confirm/">
			<h2>Update Profile:</h2>
			<c:if test="${ not empty error_msg }">
			  <br />
			  <div class="panel panel-danger">
                <div class="panel-heading">
                  <h3 class="panel-title">Updating Failed</h3>
                </div>
                <div class="panel-body">
			  	  <c:forEach items="${ error_msg }" var="item">
			    	<h5 class="text-warning">* ${ item }</h5>
			  	  </c:forEach>
			  	</div>
			  </div>
			</c:if>
			<hr class="colorgraph">
			<div class="row">
<!-- 			  <h3>Account Info</h3><br/> -->
			  <div class="col-xs-12 col-sm-6 col-md-6">
				<c:choose>
				<c:when test="${empty user.firstName}">
				  <div class="form-group">
					<input type="text" name="firstName" class="form-control input-lg" placeholder="First Name">
				  </div>
				</c:when>
				<c:when test="${not empty user.firstName}">
				  <div class="form-group">
					<input type="text" name="firstName" class="form-control input-lg" placeholder="First Name" value="${user.firstName}">
				  </div>
				</c:when>
				</c:choose>
			  </div>
			  <div class="col-xs-12 col-sm-6 col-md-6">
				<c:choose>
				<c:when test="${empty user.lastName}">
				  <div class="form-group">
					<input type="text" name="lastName" class="form-control input-lg" placeholder="Last Name">
				  </div>
				</c:when>
				<c:when test="${not empty user.lastName}">
				  <div class="form-group">
					<input type="text" name="lastName" class="form-control input-lg" placeholder="Last Name" value="${user.lastName}">
				  </div>
				</c:when>
				</c:choose>
			  </div>
			</div>
			<div class="form-group">
			  <c:if test="${not empty user.username}">
				<input type="text" name="username" class="form-control input-lg" value="${ user.username }" placeholder="Username" disabled/>
				<input type="hidden" name="username" class="form-control input-lg" value="${ user.username }"/>
			  </c:if>		
			  <c:if test="${empty user.username}">
				<input type="text" name="username" class="form-control input-lg" placeholder="Username"/>
			  </c:if>
			</div>
			<div class="form-group">
			  <c:choose>
			  <c:when test="${empty user.email}">
				<input type="email" name="email" class="form-control input-lg" placeholder="Email Address"/>
			  </c:when>
			  <c:when test="${not empty user.email}">
				<input type="email" name="email" class="form-control input-lg" placeholder="Email Address" value="${ user.email }">
				<input type="hidden" name="fb_email" value="${ user.email }"/>
			  </c:when>
			  </c:choose>
			</div>
			<hr class="colorgraph">
			<div class="row">
			  <div class="col-xs-12 col-sm-6 col-md-6">
			    <div class="form-group" align="right">
			      <h3 class="text-primary">Old Password:</h3>
			      <p>Please leave this part blank if you don't want to change password.</p>
			    </div>
			  </div>
			  <div class="col-xs-12 col-sm-6 col-md-6" style="margin-top:5%;">
			    <div class="form-group">
			      <input type="password" name="old_password" class="form-control input-lg" placeholder="Old Password">
			    </div>
			  </div>
			</div>
			
			<div class="row">
			  <div class="col-xs-12 col-sm-6 col-md-6">
			    <div class="form-group">
			      <input type="password" name="password" class="form-control input-lg" placeholder="New Password">
			    </div>
			  </div>
			  <div class="col-xs-12 col-sm-6 col-md-6">
			    <div class="form-group">
			      <input type="password" name="password2" class="form-control input-lg" placeholder="Confirm New Password">
			    </div>
			  </div>
			</div>
			<hr class="colorgraph">
			<div class="row">
<!-- 			  <h3>Personal Details</h3><br/> -->
			  <div class="col-xs-12 col-sm-6 col-md-6">
				<div class="form-group">
			  	  <font size="4">Gender: </font>
			  	  <c:choose>
			  		<c:when test="${not empty user.gender and user.gender == true}">
			  	      <label class="btn btn-default"><input type="radio" name="gender" value="male" checked>Male</label>
			  	  	  <label class="btn btn-default"><input type="radio" name="gender" value="female">Female</label>
			  	  	</c:when>
			  	  	<c:when test="${not empty user.gender and user.gender == false}">
			  	      <label class="btn btn-default"><input type="radio" name="gender" value="male">Male</label>
			  	  	  <label class="btn btn-default"><input type="radio" name="gender" value="female" checked>Female</label>
			  	  	</c:when>
			  	  	<c:when test="${empty user.gender}">
			  	      <label class="btn btn-default"><input type="radio" name="gender" value="male">Male</label>
			  	  	  <label class="btn btn-default"><input type="radio" name="gender" value="female">Female</label>
			  	  	</c:when>
			  	  </c:choose>
			  	</div>
			  </div>
			  <div class="col-xs-12 col-sm-6 col-md-6">
				<div class="form-group">
				  <c:choose>
			  		<c:when test="${empty birthday}">
					<input type="text" id="datepicker" name="datepicker" class="form-control input-lg" placeholder="Birthday" />
					</c:when>
					<c:when test="${not empty birthday}">
					<input type="text" id="datepicker" name="datepicker" class="form-control input-lg" value="${ birthday }" />
					</c:when>
				  </c:choose>
				</div>
			  </div>
			</div>
			<div class="row">
			  <div class="col-xs-12 col-sm-6 col-md-6">
				<div class="form-group">
				<c:choose>
			  	  <c:when test="${empty user.weight}">
			  	    <h5>Weight (in kg)</h5> <input type="number" name="weight" class="form-control input-lg"/>
			  	  </c:when>
			  	  <c:when test="${not empty user.weight}">
			  	    <h5>Weight (in kg)</h5> <input type="number" name="weight" class="form-control input-lg" value="${ user.weight }"/>
			  	  </c:when>
			  	</c:choose>
			  	</div>
			  </div>
			  <div class="col-xs-12 col-sm-6 col-md-6">
				<div class="form-group">
				  <c:choose>
			  	  <c:when test="${empty user.height}">
					<h5>Height (in cm)</h5> <input type="number" name="height" class="form-control input-lg"/>
				  </c:when>
				  <c:when test="${not empty user.height}">
					<h5>Height (in cm)</h5> <input type="number" name="height" class="form-control input-lg" value="${ user.height }"/>
				  </c:when>
				  </c:choose>
				  <input type="hidden" name="id" value="${ user.id }"/>
				</div>
			  </div>
			</div>				

			<hr class="colorgraph">
			<div class="row">
				<div class="col-xs-12 col-md-6" style="margin-left:25%;">
				  <input type="submit" id="update" class="btn btn-primary btn-block btn-lg" value="Update">
				</div>
			</div>
		  </form>
		</div>
	  </div>
	</div>
	</div>
  </body>
</html>
<%@ page session="false"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %> 
<%@ taglib prefix="sf" uri="http://www.springframework.org/tags/form"%> 
<!DOCTYPE html>
<html lang="en">
  <head>
  <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
     <title>Activity Set Goal</title>

    <!-- Bootstrap -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">
    <%-- <link href="<c:url value="/resources/template/css/carousel.css" />" rel="stylesheet"> --%>
	<link href="<c:url value="/resources/template/css/dashboard.css" />" rel="stylesheet">   
    <link rel="stylesheet" href="resources/css/nv.d3.css" />
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  
 </head>
<body>
	
	<%@ include file="/resources/template/jsp/activity_nar_bar.jsp" %>
	<div class="container-fluid">
	<div class="row">
	<div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar" id="wow">
            <li ><a href="/project/activity/">Overview <span class="sr-only">(current)</span></a></li>
            <li class="active"><a href="/project/activity/goal">Set Goal</a></li>
            <li><a href="/project/activity/activity">Check Activity</a></li>
            <li><a href="/project/activity/trophy_room">Trophy Room</a></li>
          </ul>
          
	</div>

	<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
	
	<h1 class="page-header">Set personal goal</h1>
	<br>
	<div class="table-responsive">
	
			<c:if test="${not empty msg}">
		<div class="panel panel-warning" role="alert">
			<button type="button" class="close" data-dismiss="alert" 
                                aria-label="Close">
				<span aria-hidden="true">×</span>
			</button>
			<strong>${msg}</strong>
		</div>
	</c:if>

	<h1>Goal Detail</h1>
	<br />

	<div class="row">
		<label class="col-sm-2">Calories Out</label>
		<div class="col-sm-10">${goal.caloriesOut}</div>
	</div>

	<div class="row">
		<label class="col-sm-2">Distance</label>
		<div class="col-sm-10">${goal.distance}</div>
	</div>

	<div class="row">
		<label class="col-sm-2">Floors</label>
		<div class="col-sm-10">${goal.floors}</div>
	</div>

	<div class="row">
		<label class="col-sm-2">Steps</label>
		<div class="col-sm-10">${goal.steps}</div>
	</div>
	
	<div class="row">
		<label class="col-sm-2">Period</label>
		<div class="col-sm-10">${goal.period}</div>
	</div>
	<div class="row">
		<label class="col-sm-2">Time</label>
		<div class="col-sm-10">${goal.time}</div>
	</div>
	
	</div>
	</div>
	</div>
	</div>
	 <%@ include file="/WEB-INF/views/headers/footer.jsp" %> 	
</body>
</html>	
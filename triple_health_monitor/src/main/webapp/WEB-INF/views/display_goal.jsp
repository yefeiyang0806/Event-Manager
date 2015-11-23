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
	
	<h1 class="page-header">User Goal History</h1>
	<br>
	<div class="table-responsive">
	
	
		<fieldset>
			<table class="table table-hover">
				<thead>
				<tr>
					<th>Calories Out</th>
					<th>Distance</th>
					<th>Floors</th>
					<th>Steps</th>
					<th>Period</th>
					<th>Create Time</th>
				</tr>
				</thead>
			<c:forEach items="${goals}" var="goal">
				<tbody>
				<tr>
					<td>${goal.caloriesOut}</td>
					<td>${goal.distance}</td>
					<td>${goal.floors}</td>
					<td>${goal.steps}</td>
					<td>${goal.period}</td>
					<td>${goal.time}</td>
				</tr>
				
				
			</c:forEach>
				<tr>
					<th><a href="/project/activity/set_goal"><button>Set New Goal</button></a></th>
					
				</tr>
				</tbody>
			</table>
		</fieldset>
	
	
	
	</div>
	</div>
	</div>
	</div>
	 <%@ include file="/WEB-INF/views/headers/footer.jsp" %> 	
</body>
</html>	
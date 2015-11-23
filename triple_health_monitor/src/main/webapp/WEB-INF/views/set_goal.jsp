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
	
	<sf:form method="POST" modelAttribute="goal">
		<fieldset>
			<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
				<div class="form-group">
    		  		<label for="CaloriesOut" class="col-sm-4 control-label">CaloriesOut</label>
    		  		<div class="col-sm-4">
    		  			<div class="input-group">
      			  			<input type="number" class="form-control" id="caloriesOut" name="caloriesOut">
      			  			<div class="input-group-addon">kj</div>
      					</div>
      		  		</div>
      			</div>
      			<div class="form-group">
    		  		<label for="Distance" class="col-sm-4 control-label">Distance</label>
    		  		<div class="col-sm-4">
    		  			<div class="input-group">
      			  			<input type="number" class="form-control" id="distance" name="distance">
      			  			<div class="input-group-addon">m</div>
      					</div>
      		  		</div>
      			</div>
				
				<div class="form-group">
    		  		<label for="Floors" class="col-sm-4 control-label">Floors</label>
    		  		<div class="col-sm-4">
    		  			<div class="input-group">
      			  			<input type="number" class="form-control" id="floors" name="floors">
      			  			<div class="input-group-addon">m</div>
      					</div>
      		  		</div>
      			</div>
      			
      			<div class="form-group">
    		  		<label for="Steps" class="col-sm-4 control-label">Steps</label>
    		  		<div class="col-sm-4">
    		  			<div class="input-group">
      			  			<input type="number" class="form-control" id="steps" name="steps">
      			  			<div class="input-group-addon">m</div>
      					</div>
      		  		</div>
      			</div>
				
				<div class="form-group">
    		  		<label for="Period" class="col-sm-4 control-label">Period</label>
    		  		<div class="col-sm-4">
    		  			<div class="input-group">
      			  			<Select  class="form-control" id="period" name="period">
      			  				<option value="weekly">Daily</option>
      			  				<option value="weekly">Weekly</option>
      			  				<option value="monthly">Monthly</option>
      			  				<option value="other">Other</option>
      			  			</Select>
      					</div>
      		  		</div>
      			</div>
				
				
				<tr>
					<th><a href="activity_home"><button>Cancel</button></a></th>
					<td><sf:hidden path="id"/> 
					<td><input type="submit" value="Update"/></td>
				</tr>
			</div>
		</fieldset>
	</sf:form>
	</div>
	</div>
	</div>
	</div>
	 <%@ include file="/WEB-INF/views/headers/footer.jsp" %> 	
</body>
</html>	
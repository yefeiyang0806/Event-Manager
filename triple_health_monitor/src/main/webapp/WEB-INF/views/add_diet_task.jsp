<%@page session="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Add Diet Task</title>

    <!-- Bootstrap core CSS -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="<c:url value="/resources/template/css/dashboard.css" />" rel="stylesheet">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    
    <style>
      .list-unstyled li {
      	margin: 1em 0 1em 0;
      }
      .date_pick_display {
      	margin: 0.5em 0 0.5em 0;
      }
    </style>
    
    </head>

<body>
  	<c:import url='/resources/template/jsp/food_nav_bar.jsp' />
  	
  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="<c:url value="/resources/bootstrap-3.3.5-dist/js/bootstrap.min.js" />"></script>
    
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li class="active"><a href=""><strong>Overview</strong><span class="sr-only">(current)</span></a></li>
            <li>
              <ul class="list-unstyled" style="margin-left: 15%;">
                <li><a href="/project/food/intake_calorie/">Go Back</a></li>
            	<li><h5>Select a Date:</h5>
            	  <form action="/project/food/intake_calorie/" method="POST">
            	  <div class="date_pick_display"><input type="text" id="datepicker" name="datepicker" /></div>
            	  <div style="width: 50%;">
            		<button type="submit" class="btn btn-sm btn-primary btn-block" id="activate_date">Go Check</button>
            	  </div>
            	  </form>
            	</li>
              </ul>
            </li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="/project/food/home/"><strong>Food Home Page</strong><span class="sr-only">(current)</span></a></li>
            <li><a href="/project/food/intake_calorie/">Calorie Intake</a></li>
            <li><a href="/project/food/comparison/">Compare With Others</a></li>
            <li class="active"><a href="/project/food/add_diet/">Set Diet Tasks</a></li>
            <li><a href="/project/food/diet_tasks/">My Diet Tasks</a></li>
            <li><a href="/project/food/summary/">Food Summary</a></li>
            <li><a href="/project/user/update/">Update Profile</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
        <c:if test="${not empty modify }">
          <h1 class="page-header">Modify Diet Task</h1>
        </c:if>
        <c:if test="${ empty modify }">
          <h1 class="page-header">Add Diet Task</h1>
        </c:if>
          <c:if test="${not empty error}">
			<div class="panel panel-danger">
              <div class="panel-heading">
              	<h2 class="panel-title">Create Diet Task Failed.</h2>
              </div>
              <div class="panel-body">
              	  ${error}
              </div>
          	</div>
		  </c:if>
          <form class="form-horizontal" action="/project/food/add_diet/add/" method="post">
          <div class="spacer" style="height:10%;">&nbsp;</div>
          
          <c:if test="${empty weight_loss}">
            <div class="form-group">
    		  <label for="weight_loss" class="col-sm-4 control-label"><font size="4">Target Weight Reduction:</font></label>
    		  <div class="col-sm-4">
    		  	<div class="input-group">
      			  <input type="number" class="form-control" id="weight_loss" name="weight_loss" placeholder="present in kg">
      			  <div class="input-group-addon">kg</div>
      			</div>
      		  </div>
      		</div>
      	  </c:if>
      	  <c:if test="${not empty weight_loss}">
            <div class="form-group">
    		  <label for="weight_loss" class="col-sm-4 control-label"><font size="4">Target Weight Reduction:</font></label>
    		  <div class="col-sm-4">
    		  	<div class="input-group">
      			  <input type="number" class="form-control" id="weight_loss" name="weight_loss" value="${weight_loss}">
      			  <div class="input-group-addon">kg</div>
      			</div>
      		  </div>
      		</div>
      	  </c:if>
      	  
      	  <c:if test="${empty recommend_duration and empty duration}">
      		<div class="form-group">
    		  <label for="duration" class="col-sm-4 control-label"><font size="4">Task Duration:</font></label>
    		  <div class="col-sm-4">
    		    <div class="input-group">
      			  <input type="number" class="form-control" id="duration" name="duration" placeholder="present in days">
      			  <div class="input-group-addon">days</div>
      			</div>
      		  </div>
      		</div>
      	  </c:if>
      	  <c:if test="${not empty recommend_duration}">
      		<div class="form-group has-warning">
    		  <label for="duration" class="col-sm-4 control-label"><font size="4">Task Duration:</font></label>
    		  <div class="col-sm-4">
    		    <div class="input-group">
      			  <input type="number" class="form-control" id="duration" name="duration" value="${recommend_duration}">
      			  <div class="input-group-addon">days</div>
      			</div>
      		  </div>
      		</div>
      	  </c:if>
      	  <c:if test="${not empty duration}">
      		<div class="form-group">
    		  <label for="duration" class="col-sm-4 control-label"><font size="4">Task Duration:</font></label>
    		  <div class="col-sm-4">
    		    <div class="input-group">
      			  <input type="number" class="form-control" id="duration" name="duration" value="${duration}">
      			  <div class="input-group-addon">days</div>
      			</div>
      		  </div>
      		</div>
      	  </c:if>
      	  
      	  <c:if test="${empty start_date}">
      		<div class="form-group">
    		  <label for="start_date" class="col-sm-4 control-label"><font size="4">Start Date:</font></label>
    		  <div class="col-sm-4">
      			<input type="text" class="form-control" id="start_date" name="start_date" placeholder="yyyy-mm-dd">
      		  </div>
      		</div>
      	  </c:if>
      	  <c:if test="${not empty start_date}">
      		<div class="form-group">
    		  <label for="start_date" class="col-sm-4 control-label"><font size="4">Start Date:</font></label>
    		  <div class="col-sm-4">
      			<input type="text" class="form-control" id="start_date" name="start_date" value="${ start_date }">
      		  </div>
      		</div>
      	  </c:if>
      	  
      	  
      		<div class="form-group">
    		  <label for="email_frequency" class="col-sm-4 control-label"><font size="4">Email Frequency:</font></label>
    		  <div class="col-sm-2" style="margin-left:5%;">
    		  	<div class="radio" >
      			  <input type="radio" id="email_frequency" name="email_frequency" value="daily">Daily
      			</div>
      			<div class="radio" style="display:inline-block;">
      			  <input type="radio" id="email_frequency" name="email_frequency" value="weekly" checked>Weekly
      			</div>
      		  </div>
      		  <div class="col-sm-2">
      		  	<div class="radio">
      			  <input type="radio"  id="email_frequency" name="email_frequency" value="monthly">Monthly
      			</div>
      			<div class="radio" style="display:inline-block;">
      			  <input type="radio" id="email_frequency" name="email_frequency" value="never">Never
      			</div>
      		  </div>
      		</div>
      		<c:if test="${not empty modify }">
      		  <input type="hidden" name="id" value="${ id }">
      		  <div style="margin:5% 40% 0 40%;width:20%;"><input type="submit" class="btn btn-sm btn-primary" id="diet_submit_btn" value="Update"></div>
      		</c:if>
      		<c:if test="${ empty modify }">
      		  <div style="margin:5% 40% 0 40%;width:20%;"><input type="submit" class="btn btn-sm btn-primary" id="diet_submit_btn" value="Create"></div>
      		</c:if>
      	  </form>
      	</div>
      </div>
    </div>
   
    <!-- Add script at last -->  
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script>
      $(function() {
	    $( "#datepicker" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
	    
	    $( "#start_date" ).datepicker({ minDate: "-2M", maxDate: "+2M", dateFormat: "yy-mm-dd"});
	    
	  });
    </script>
          
          
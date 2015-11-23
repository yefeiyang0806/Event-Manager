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

    <title>My Diet Tasks</title>

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
      .table {
      	width: 80%;
      	margin-left: 5%;
      }
      .table tbody>tr>td {
    	vertical-align: middle;
    	font-size: 16px;
      }
      .table tbody>tr>td a {
      	width: 100%;
      }
      .task_title {
      	margin-left: 5%;
      }
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
<!--                 <li><a href="">Add Food</a></li> -->
                <li><a href="/project/food/comparison/">Visualized Data</a></li>
            	<li><h5>Select a Date:</h5>
            	  <form action="/project/food/intake_calorie/" method="POST">
            	  <div class="date_pick_display"><input type="text" id="datepicker" name="datepicker" /></div>
            	  <div style="width: 50%;">
            		<button type="submit" class="btn btn-sm btn-primary btn-block" id="activate_date">Go Check</button>
            	  </div>
            	  </form>
            	</li>
            	<li>
				  <div style="width: 50%;">
				  	<a role="button" class="btn btn-sm btn-primary btn-block" href="/project/food/add_diet/">Add Diet Task</a>
				  </div>
				  
				</li>
              </ul>
            </li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="/project/food/home/"><strong>Food Home Page</strong><span class="sr-only">(current)</span></a></li>
            <li><a href="/project/food/intake_calorie/">Calorie Intake</a></li>
            <li><a href="/project/food/comparison">Compare With Others</a></li>
            <li><a href="/project/food/add_diet/">Set Diet Tasks</a></li>
            <li class="active"><a href="/project/food/diet_tasks/">My Diet Tasks</a></li>
            <li><a href="/project/food/summary/">Food Summary</a></li>
            <li><a href="/project/user/update/">Update Profile</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h1 class="page-header">Personal Diet Tasks</h1>
          <br />
          <div class="table-responsive">
          	<c:if test="${ empty diet_tasks }">
			  <div class="panel panel-warning">
            	<div class="panel-heading">
              	  <h2 class="panel-title">No diet tasks records yet.</h2>
              	</div>
              	<div class="panel-body">
              	  You can <a href="/project/food/add_diet/">create diet tasks here</a>.<br />
              	  More actions are available on the left-hand side navigator bar.
              	</div>
          	  </div>
		  	</c:if>
          	<c:if test="${ not empty diet_tasks }">
          	  <c:forEach var="i" begin="1" end="${length}">
          	    <h3 class="task_title text-muted">Diet Task ${ i }, 
          	      <small><a href="/project/food/modify_diet_task?id=${ diet_tasks[i-1].id }">[Modify]</a></small>
          	    </h3>
          	    <h4 class="task_title text-success">Daily Calorie: <strong>${ diet_tasks[i-1].dailyTargetCalorie } kcal</strong></h4>
          	    <table class="table">
          	      <tbody>
          	      	<tr>
          	      	  <td>Target Weight Loss: ${ diet_tasks[i-1].weightLoss } kg</td>
          	      	  <td>Task State: ${ diet_tasks[i-1].state }</td>
          	      	  <td>Task Duration: ${ diet_tasks[i-1].duration } days</td>
          	      	  <c:if test="${ diet_tasks[i-1].state != 'Not Started'}">
          	      	    <td><a class="btn btn-info" role="button" href="/project/food/diet_tasks/performance?id=${ diet_tasks[i-1].id }">Performance</a></td>
          	      	  </c:if>
          	      	  <c:if test="${ diet_tasks[i-1].state == 'Not Started'}">
          	      	    <td><a class="btn btn-info disabled" role="button" href="/project/food/modify_diet_task?id=${ diet_tasks[i-1].id }">Performance</a></td>
          	      	  </c:if>
          	      	</tr>
          	      	<tr>
          	      	  <td>Start Date: ${ diet_tasks[i-1].start }</td>
          	      	  <c:if test="${ diet_tasks[i-1].state != 'Expired'}">
          	      	  	<td colspan="2">Estimated Finish Date: ${ diet_tasks[i-1].finish }</td>
          	      	  </c:if>
          	      	  <c:if test="${ diet_tasks[i-1].state == 'Expired'}">
          	      	  	<td>Finished at: ${ diet_tasks[i-1].finish }</td>
          	      	  	<td>Total Calorie: ${ totalCalories[i-1] }</td>
          	      	  </c:if>
          	      	  <td><a class="btn btn-info" role="button" href="/project/food/delete_diet_task?id=${ diet_tasks[i-1].id }">Delete</a></td>
          	      	</tr>
          	      </tbody>
          	    </table>
          	    <br />
          	    
          	  </c:forEach>
          	</c:if>
          </div>
        </div>
      </div>
    </div>
    
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script>
      $(function() {
	    $( "#datepicker" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
      });
	</script>
  </body>
          
          
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

    <title>Intake Calorie Summary</title>

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
            	<li><form action="/project/food/add_food/" method="POST">
				  <input type="hidden" name="date" value="${ date }"/>
				  <div style="width: 50%;">
				  	<button type="submit" class="btn btn-sm btn-primary btn-block">Add Food</button>
				  </div>
				  </form>
				</li>
              </ul>
            </li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="/project/food/home/"><strong>Food Home Page</strong><span class="sr-only">(current)</span></a></li>
            <li class="active"><a href="#">Calorie Intake</a></li>
            <li><a href="/project/food/comparison/">Compare With Others</a></li>
            <li><a href="/project/food/add_diet/">Set Diet Tasks</a></li>
            <li><a href="/project/food/diet_tasks/">My Diet Tasks</a></li>
            <li><a href="/project/food/summary/">Food Summary</a></li>
            <li><a href="/project/user/update/">Update Profile</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <c:if test="${ not empty date }">
			<h1 class="page-header">Calorie Intake of Date: ${ date }</h1>
		  </c:if>
		  <c:if test="${ empty date }">
			<h1 class="page-header">Today's Calorie Intakes</h1>
		  </c:if>
		  <br />
		  <h3 class="sub-header">Healthy Intake: 2100 kcal</h3>
          <div class="table-responsive">
          	<c:if test="${ empty food_list }">
			  <div class="panel panel-warning">
            	<div class="panel-heading">
              	  <h2 class="panel-title">Oops, no food record found this day.</h2>
              	</div>
              	<div class="panel-body">
              	  You can either <a href="/project/food/add_food/">add food records</a> or change a date to display.<br />
              	  More actions are available on the left-hand side navigator bar.
              	</div>
          	  </div>
		  	</c:if>
		  	<c:if test="${ not empty food_list }">
		  	  <c:if test="${ total le 2100 }">
		  		<div style="width:60%;margin:auto;"><h4><p class="bg-success text-center" style="padding:1em;"><strong>Well done! Your intake-calorie is under the boundary of healthy diet.</strong></p></h4></div>
		  	  </c:if>
		  	  <c:if test="${ total gt 2100 }">
		  		<div style="width:60%;margin:auto;"><h4><p class="bg-danger text-center" style="padding:1em;"><strong>Oops, maybe one less bit of hamburger tomorrow.</strong></p></h4></div>
		  	  </c:if>
              <table class="table table-striped">
            	<thead>
                  <tr>
<!--                 	<th>#</th> -->
                  	<th><h4>Food Name</h4></th>
                  	<th><h4>Calorie Amount (in kcal)</h4></th>
             	  </tr>
              	</thead>
              	<tbody>
              	  <c:forEach var="i" begin="1" end="${length}">
					<tr><td width="60%" id="food_name">${food_list[i-1].food }</td>
					  <td width="40%" id="calo">${food_list[i-1].calorie }
					  </td>
					</tr>
				  </c:forEach>
				  <c:if test="${ total le 2100 }">
				  	<tr class="success">
				  </c:if>
				  <c:if test="${ total gt 2100 }">
				  	<tr class="danger">
				  </c:if>
				  	  <td id="food_name"><h4><strong>Total Calorie</strong></h4></td>
                	  <td id="calo"><h4><strong>${total} kcal</strong></h4></td>
                  	</tr>
              	</tbody>
              </table>
            </c:if>
          	<form action="/project/food/add_food/" method="POST">
			  <input type="hidden" name="date" value="${ date }"/>
			  <div style="width: 15%;margin:0 0 0 20%;display:inline-block;">
			    <button type="submit" class="btn btn-sm btn-primary btn-block">Add Food</button>
			  </div>
			  <div style="width: 15%;margin-left:5%;display:inline-block;">
		        <a role="button" class="btn btn-sm btn-primary btn-block" href="/project/food/comparison">Visualize Data</a>
		  	  </div>
			  <div style="width: 15%;margin-left:5%;display:inline-block;">
		        <a role="button" class="btn btn-sm btn-primary btn-block" href="/project/food/home">Go Home</a>
		  	  </div>
		    </form>
          </div>
        </div>
      </div>
    </div>
        
    <!-- Add script at last -->  
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>  
    <script>
  		$(function() {
  	    	$( "#datepicker" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
  	  	});
  	</script>
  </body>
</html>
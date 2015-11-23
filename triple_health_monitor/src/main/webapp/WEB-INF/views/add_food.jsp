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

    <title>Add Food</title>

    <!-- Bootstrap core CSS -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="<c:url value="/resources/template/css/dashboard.css" />" rel="stylesheet">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    
    <style>
      .list-unstyled li {margin: 1em 0 1em 0;}
      .date_pick_display {margin: 0.5em 0 0.5em 0;}
      .date_field {display: inline-block;}
      .date_label {display: inline-block;margin:0 10% 0 12%;}
      .food_field {display: inline-block;}
      .food_label {display: inline-block;margin:0 5% 0 12%;}
      .calo_field {display: inline-block;}
      .calo_label {display: inline-block;margin:0 5% 0 10%;}
      .submit_button {width: 30%;margin-top:2em;}
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
            <li><a href="/project/food/add_diet/">Set Diet Tasks</a></li>
            <li><a href="/project/food/diet_tasks/">My Diet Tasks</a></li>
            <li><a href="/project/food/summary/">Food Summary</a></li>
            <li><a href="/project/user/update/">Update Profile</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h1 class="page-header">Add Food &amp; Calorie</h1>
          <form action="/project/add_food/add/" method="post">
<!--         	<table class="table"> -->
<!-- 			<tr><td class="section_title" colspan=2>Add Food & Calorie</td></tr> -->
			<table class="table table-striped">
			  <tbody>
			  	<tr>
			  	  <td>
			  	  	<div class="date_label"><span class="label label-default">Select Date: </span></div>
			  		<div class="date_field"><input type="text" id="datepicker2" name="datepicker" value="${ date }" /></div>
			  	  </td>
			  	</tr>
			  	<c:forEach begin="1" end="8" varStatus="loop">
			  	<tr><td>
			  	  <div class="food_label"><span class="label label-default">Food ${loop.index}: </span></div>
			  	  <div class="food_field"><input type="text" name="food_${ loop.index }"/></div>
			  	  <div class="calo_label"><span class="label label-default">Calorie Amount: </span></div>
			  	  <div class="calo_field"><input type="number" name="calo_${ loop.index }"/></div>
			  	</td></tr>
			  	</c:forEach>
				<tr><td colspan=2 align="center">
					<div class="submit_button"><input class="btn btn-sm btn-primary btn-block" type="submit" value="Add"/></div>
			  </tbody>
			</table>
<!-- 		</table> -->
		  </form>
		</div>
	  </div>
	</div>
	
	<!-- Add script -->
	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
	<script>
  		$(function() {
  	    	$( "#datepicker" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
  	    	$( "#datepicker2" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
  	  	});
  	</script>
</body>
</html>
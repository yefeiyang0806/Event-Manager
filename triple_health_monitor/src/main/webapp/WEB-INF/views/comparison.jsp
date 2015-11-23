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

    <title>Food Intake Comparison</title>

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
      #chartContainer {
      	width: 60%;
      	margin-right: 30%;
      	margin-left: 10%;
      	display: inline-block;
      }
      #chartController {
      	width: 30%;
      	margin-right: 0%;
      	margin-left: 70%;
      }
      .date_pick_display input{
      	width: 60%;
      	margin: 0 auto;
      	display: block;
      	margin-top: 2em;
      }
      .submit_date input{
      	width: 40%;
      	margin: 0 auto;
      	display: block;
      	margin-top: 2em;
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
            <li class="active"><a href=""><strong>Overview</strong> <span class="sr-only">(current)</span></a></li>
            <li>
              <ul class="list-unstyled" style="margin-left: 15%;">
<!--                 <li><a href="">Add Food</a></li> -->
                <li><a href="/project/food/intake_calorie/">Return to Data Table</a></li>
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
            <li><a href="/project/food/intake_calorie/">Calorie Intake</a></li>
            <c:if test="${ not empty task}">
            <li><a href="/project/food/comparison/">Compare With Others</a></li>
            </c:if>
            <c:if test="${ empty task}">
            <li class="active"><a href="/project/food/comparison/">Compare With Others</a></li>
            </c:if>
            <li><a href="/project/food/add_diet/">Set Diet Tasks</a></li>
            <li><a href="/project/food/diet_tasks/">My Diet Tasks</a></li>
            <li><a href="/project/food/summary/">Food Summary</a></li>
            <li><a href="/project/user/update/">Update Profile</a></li>
          </ul>
        </div>
  		<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <c:if test="${ not empty start_date and not empty finish_date }">
			<h1 class="page-header">Performance during: ${ start_date } - ${ finish_date }</h1>
		  </c:if>
		  <c:if test="${ not empty task}">
			<h1 class="page-header">Performance of Task ${ task }:</h1>
		  </c:if>
		  <c:if test="${ empty start_date and empty task}">
			<h1 class="page-header">Performance of Last Week:</h1>
		  </c:if>
		  <br />
		  <div id="chartContainer"></div>
		  <div id="chartController">
		  <c:if test="${ empty task}">
		  	<form action="/project/food/comparison/" method="POST">
            <div class="date_pick_display"><input type="text" id="datepicker" name="start_date" placeholder="Start Date"/></div>
            <div class="date_pick_display"><input type="text" id="datepicker2" name="finish_date" placeholder="Finish Date"/></div>
            <div class="submit_date"><input type="submit" class="btn btn-sm btn-primary" id="activate_date" value="check"></div>
            </form>
          </c:if>
          <c:if test="${ not empty task}">
          	<div style="margin-left:20%;margin-top:20%;">
          	  <a role="button" class="btn btn-sm btn-primary" href="/project/food/diet_tasks/">Back To Diet Tasks</a>
          	</div>
         </c:if>
		  </div>
		</div>
	  </div>
	</div>
	<!-- Store daily data -->
	
	<form id="date">
		<c:forEach items="${weeklyCalorie}" var="entry">
			<input type="hidden" id="${entry.key}" value="${entry.value}">
		</c:forEach>
	</form>
	<input type="hidden" id="average_value" value="${allAverage}"/>
	
	<!-- Load Script at last -->
	
	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  	<script src="<c:url value="/resources/canvasjs-1.7.0/jquery.canvasjs.min.js" />"></script>
  	<script>
	$(function() {
	    $( "#datepicker" ).datepicker({
		    minDate: "-2M",
		    maxDate: "0",
		    dateFormat: "yy-mm-dd",
		    onSelect: function (date) {
                var date2 = $('#datepicker').datepicker('getDate');
                date2.setDate(date2.getDate() + 6);
                $('#datepicker2').datepicker('setDate', date2);
                //sets minDate to dt1 date + 1
                date2.setDate(date2.getDate() - 5);
                $('#datepicker2').datepicker('option', 'minDate', date2);
		    }
		});
	    $( "#datepicker2" ).datepicker({
		    minDate: "-2M",
		    maxDate: "0",
		    dateFormat: "yy-mm-dd",
		    onClose: function () {
                var dt1 = $('#datepicker').datepicker('getDate');
                console.log(dt1);
                var dt2 = $('#datepicker2').datepicker('getDate');
                if (dt2 <= dt1) {
                    var minDate = $('#datepicker2').datepicker('option', 'minDate');
                    $('#datepicker2').datepicker('setDate', minDate);
                }
            }
		});
		var data = [];
		var average = [];
		var recommend = [];
		$("#date").find("input").each(function(){
			calorie_value = parseInt(this.value);
			var single_data = {
				label: this.id,
				y: calorie_value
			};
			var each_average = {
				label: this.id,
				y: parseInt($("#average_value").val())
			};
			var each_recommend = {
				label: this.id,
				y: 2100
				};
			data.push(single_data);
			average.push(each_average);
			recommend.push(each_recommend);
		});
		//data = [{x:3, y:4}];
		$("#chartContainer").CanvasJSChart({
			theme: "theme2",
		    title:{
		    	text: "Performance Comparison"
		    },
			data: [
			{
				type: "line", //change it to column, spline, line, pie, etc
				showInLegend: true, 
		        name: "series1",
		        legendText: "Your Performance",
				dataPoints: data
			},
			{
				type: "line",
				showInLegend: true, 
		        name: "series2",
		        legendText: "Average Performance",
				dataPoints: average
			},
			{
				type: "line",
				showInLegend: true, 
		        name: "series3",
		        legendText: "Recommended Intake",
				dataPoints: recommend
			}]
		});
	});
	
	</script>
  </body>
</html>
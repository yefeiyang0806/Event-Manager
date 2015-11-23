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

    <title>Food Module Summary</title>

    <!-- Bootstrap core CSS -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="<c:url value="/resources/template/css/dashboard.css" />" rel="stylesheet">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    
    <style>
      .list-unstyled li {margin: 1em 0 1em 0;}
      .date_pick_display {margin: 0.5em 0 0.5em 0;}
      .flag {width:23%;margin:0 1% 0 1%;}
      .flag_img {float:left;margin:15% 5% 10% 5%;}
      .img_wrapper {width:100px;height:100px;background-size:cover;}
      .flag_content {float:right;margin:10% 0 10% 0;text-align:right;}
      #chartContainer {
      	width: 60%;
      	margin-right: 35%;
      	margin-left: 5%;
      	display: inline-block;
      }
      #doughnutActiveRatio {width:33%;display:inline-block;}
      #doughnutTaskRatio {width:33%;display:inline-block;}
      #doughnutCalorieRatio {width:33%;display:inline-block;}
      #dietTasks {
      	width: 30%;
      	margin-right: 0%;
      	margin-left: 70%;
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
            <li><a href="/project/food/intake_calorie/">Calorie Intake</a></li>
            <li><a href="/project/food/comparison/">Compare With Others</a></li>
            <li><a href="/project/food/add_diet/">Set Diet Tasks</a></li>
            <li><a href="/project/food/diet_tasks/">My Diet Tasks</a></li>
            <li class="active"><a href="/project/food/summary/">Food Summary</a></li>
            <li><a href="/project/user/update/">Update Profile</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <c:if test="${ not empty displayName }">
			<h1 class="page-header">${displayName}'s Food Module Summary</h1>
		  </c:if>
		  <c:if test="${ empty displayName }">
			<h1 class="page-header">Today's Calorie Intakes</h1>
		  </c:if>
		  
		  <div class="row placeholders">
            <div class="col-xs-6 col-sm-3 bg-danger flag">
              <div class="flag_img">
<%--                 <div class="img_wrapper" style="background-image: url('<c:url value="/resources/img/active_days_flag.png"/>')"></div> --%>
              	<span style="font-size:5em;" class="glyphicon glyphicon-glass" aria-hidden="true"></span>
              </div>
              <c:if test="${ not empty active_days }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">${ active_days }</font></div><div class="text-muted">active days</div></div>
              </c:if>
              <c:if test="${ empty active_days }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">N/A</font></div><div class="text-muted">active days</div></div>
              </c:if>  
            </div>
            
            <div class="col-xs-6 col-sm-3 bg-info flag">
              <div class="flag_img">
<%--                 <div class="img_wrapper" style="background-image: url('<c:url value="/resources/img/total_food_flag.png"/>')"></div> --%>
              	<span style="font-size:5em;" class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
              </div>
              <c:if test="${ not empty total_days }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">${ total_days }</font></div><div class="text-muted">total days</div></div>
              </c:if>
              <c:if test="${ empty total_days }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">N/A</font></div><div class="text-muted">total days</div></div>
              </c:if>  
            </div>

            <div class="col-xs-6 col-sm-3 bg-success flag">
              <div class="flag_img">
<%--                 <div class="img_wrapper" style="background-image: url('<c:url value="/resources/img/task_flag.png"/>')"></div> --%>
              	<span style="font-size:5em;" class="glyphicon glyphicon-cutlery" aria-hidden="true"></span>
              </div>
              <c:if test="${ not empty personal_average }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">${ personal_average }</font></div><div class="text-muted">average calorie</div></div>
              </c:if>
              <c:if test="${ empty personal_average }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">N/A</font></div><div class="text-muted">average calorie</div></div>
              </c:if>
            </div>
            <div class="col-xs-6 col-sm-3 bg-warning flag">
              <div class="flag_img">
                <!--div class="img_wrapper" style="background-image: url('<c:url value="/resources/img/task_flag.png"/>')"></div-->
                <span style="font-size:5em;" class="glyphicon glyphicon-stats" aria-hidden="true"></span>
              </div>
              <c:if test="${ not empty active_ratio }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">${ active_ratio }%</font></div><div class="text-muted">active ratio</div></div>
              </c:if>
              <c:if test="${ empty active_ratio }">
                <div class="flag_content"><div style="margin:0 0 0 0;"><font size="12" class="text-primary">N/A%</font></div><div class="text-muted">active ratio</div></div>
              </c:if>
            </div>
          </div>
          <div class="row">
            <div id="chartContainer"></div>
          	<div class="panel panel-info" id="dietTasks">
  			  <div class="panel-heading">
    		  	<h3 class="panel-title">Active Tasks:</h3>
  			  </div>
  		  	  <div class="panel-body" style="height:350px;overflow:scroll;">
    		  	<c:if test="${ not empty active_dts }">
          	  	  <c:forEach var="i" begin="1" end="${length}">
          	    	<h4 class="task_title text-muted"><b>Diet Task ${ i }:</b> <small>Estimated finish at: ${ active_dts[i-1].finish }</small></h4>
          	    	<h5>Target Weight Loss: ${ active_dts[i-1].weightLoss }
          	    	  &nbsp;&nbsp;<small><a href="/project/food/modify_diet_task?id=${ active_dts[i-1].id }">[Modify]</a></small>
          	    	</h5>
          	    	<c:if test="${ i != length }">
          	    	  <br/>
          	    	</c:if>
          	      </c:forEach>
          	    </c:if>
          	    <c:if test="${ empty active_dts }">
          	      <h4>No Active Diet Tasks</h4>
          	    </c:if>
  		  	  </div>
		  	</div>
          </div>
          <br/><br/>
          <div class="row">
          	<div id="doughnutActiveRatio"></div>
          	<div id="doughnutCalorieRatio"></div>
          	<div id="doughnutTaskRatio"></div>
          </div>
      	</div>
      </div>
      <form id="date">
		<c:forEach items="${monthly_calorie}" var="entry">
			<input type="hidden" id="${entry.key}" value="${entry.value}">
		</c:forEach>
	  </form>
	  <input type="hidden" id="active_days" value="${ active_days }"/>
	  <input type="hidden" id="total_days" value="${ total_days }"/>
	  <input type="hidden" id="average_value" value="${allAverage}"/>
	  <input type="hidden" id="eat_too_much" value="${ eat_too_much }"/>
	  <input type="hidden" id="active_tasks" value="${ length }"/>
	  <input type="hidden" id="expired_tasks" value="${ expired_tasks }"/>
	  <input type="hidden" id="not_start_tasks" value="${ not_start_tasks }"/>
    </div>
    
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  	<script src="<c:url value="/resources/canvasjs-1.7.0/jquery.canvasjs.min.js" />"></script>
    <script>
    $(function() {
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
		    	text: "Monthly Performance"
		    },
			data: [
			{
				type: "line", //change it to column, spline, line, pie, etc
				showInLegend: true, 
		        name: "series1",
		        legendText: "You",
				dataPoints: data
			},
			{
				type: "line",
				showInLegend: true, 
		        name: "series2",
		        legendText: "Average",
				dataPoints: average
			},
			{
				type: "line",
				showInLegend: true, 
		        name: "series3",
		        legendText: "Recommended",
				dataPoints: recommend
			}]
		});
		
		$("#doughnutActiveRatio").CanvasJSChart({
			theme: "theme1",
		    title:{
		    	text: "Active Ratio"
		    },
		    //animationEnabled: true,
			data: [
			{
				type: "doughnut", //change it to column, spline, line, pie, etc
				startAngle:20, 
				toolTipContent: "{label}: {y}",
				indexLabel: "{label} {y}",
				dataPoints: [
					{y: $("#active_days").val(), label: "Active days"},
					{y: ($("#total_days").val()-$("#active_days").val()), label: "Inactive days"}
				]
			}]
		});

		$("#doughnutCalorieRatio").CanvasJSChart({
			theme: "theme1",
		    title:{
		    	text: "Eating Too Much Ratio"
		    },
		    //animationEnabled: true,
			data: [
			{
				type: "doughnut", //change it to column, spline, line, pie, etc
				startAngle:20, 
				toolTipContent: "{label}: {y}",
				indexLabel: "{label} {y}",
				dataPoints: [
					{y: $("#eat_too_much").val(), label: "Days over diet"},
					{y: ($("#active_days").val()-$("#eat_too_much").val()), label: "Days under diet"}
				]
			}]
		});

		$("#doughnutTaskRatio").CanvasJSChart({
			theme: "theme1",
		    title:{
		    	text: "Task Statistics"
		    },
		    //animationEnabled: true,
			data: [
			{
				type: "doughnut", //change it to column, spline, line, pie, etc
				startAngle:20, 
				toolTipContent: "{label}: {y} - <strong>#percent%</strong>",
				indexLabel: "{label} {y}",
				dataPoints: [
					{y: $("#active_tasks").val(), label: "Active tasks"},
					{y: $("#expired_tasks").val(), label: "Expired tasks"},
					{y: $("#not_start_tasks").val(), label: "Not started tasks"}
				]
			}]
		});
	});
	
	</script>
  </body>
  
          
          
          
          
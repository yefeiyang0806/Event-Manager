<html>
<head>
	<%@ include file="/WEB-INF/views/css/header_style.jsp" %>
	<%@ include file="/WEB-INF/views/css/mw_style.jsp" %>
	<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
	<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
	<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
	<title>Sleep Time Track</title>
	<link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">
	<link href="<c:url value="/resources/template/css/dashboard.css" />" rel="stylesheet">
	<link rel="stylesheet" href="resources/css/nv.d3.css" />
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
	<style>
		.form-control {
			display: inline-block;
		}
	</style>
</head>
<body>
	<%@ include file="/resources/template/jsp/sleep_nav_bar.jsp" %>
	<div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li class="active"><a href="#">Overview</a></li>
            <li><a href="#">Settings</a></li>
          </ul>
        </div>
  		<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
  			<div class="panel panel-primary">
          <div class="panel-heading">
            <h3 class="panel-title">Sleep Time
            </h3>
          </div>
          <div class="panel-body" id="overview" style="height:700px">
          	<div>
          		<form id="form">
          			<input type="text" class="form form-control" style="width:150px" id="from" name="from" /> to 
            		<input type="text" class="form form-control" style="width:150px" id="to" name="to" /> 
            		<input type="submit" class="btn btn-default" value="Go" />
            	</form>
            </div>
            <div style="height:20px"></div>
            <svg></svg>
          </div>
        </div>
		</div>
	  </div>
	</div>
	
	<script src="resources/js/jquery.min.js"></script>
	<script src="resources/js/d3.min.js"></script>
    <script src="resources/js/nv.d3.min.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
	<script>
		$(function() {
			$("#from").datepicker({
				dateFormat: "yy-mm-dd",
				firstDay: 1
			});
			
			$("#to").datepicker({
				dateFormat: "yy-mm-dd",
				firstDay: 1
			});
			
			$.ajax({
				type: "get",
				url: "/project/sleeptime/getdata?from=&to=",
				success: function(response) {
					nv.addGraph(function() {
						var data = [{key:"Sleep time", values:response}];
				    	var chart;
				    	chart = nv.models.multiBarChart()
				    		.x(function(d) { return d.date })
			       			.y(function(d) { return d.duration });
				    
				    	chart.xAxis
				    	.showMaxMin(false)
				    	.tickFormat(function(d) {
				     		return d3.time.format('%x')(new Date(d))
				    	});

				    	chart.yAxis
				      		.tickFormat(d3.format(',f'));
				    
				    	d3.select('#overview svg')
				      		.datum(data)
				      		.transition().duration(500)
				      		.call(chart);
				   	 nv.utils.windowResize(chart.update);
	    		    	return chart;
	    			});		 
				}
			});
			
			$('#form').submit(function() {
				$.ajax({
					type: "get",
					url: "/project/sleeptime/getdata?from="+$("#from").val()+"&to="+$("#to").val(),
					success: function(response) {
						nv.addGraph(function() {
							var data = [{key:"Sleep time", values:response}];
					    	var chart;
					    	chart = nv.models.multiBarChart()
					    		.x(function(d) { return d.date })
				       			.y(function(d) { return d.duration });
					    
					    	chart.xAxis
					    	.showMaxMin(false)
					    	.tickFormat(function(d) {
					     		return d3.time.format('%x')(new Date(d))
					    	});

					    	chart.yAxis
					      		.tickFormat(d3.format(',f'));
					    
					    	d3.select('#overview svg')
					      		.datum(data)
					      		.transition().duration(500)
					      		.call(chart);
					   	 	nv.utils.windowResize(chart.update);
		    		    	return chart;
		    			});		 
					}
				});
				return false;
			});
		});
	</script>
</body>
</html>
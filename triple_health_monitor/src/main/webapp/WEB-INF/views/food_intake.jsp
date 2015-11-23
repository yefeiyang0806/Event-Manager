<%@page session="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
	<%@ include file="/WEB-INF/views/css/header_style.jsp" %>
	<%@ include file="/WEB-INF/views/css/mw_style.jsp" %>
	<%@ include file="/WEB-INF/views/css/intake_calorie_style.jsp" %>
	<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
  	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
  	<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
<!--   	<link rel="stylesheet" href="/resources/demos/style.css"> -->
  	<script>
  		$(function() {
  	    	$( "#datepicker" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
  	  	});
  	</script>
	<style>
		body {
			margin: 0;
		}
		
		#datePicker {
			height: 25%;
		}
		
		#suggestion {
			height: 75%;
		}
		
		.date_pick_display {
			margin: 20px;
		}
		
	</style>
</head>
<body>
	<%@ include file="/WEB-INF/views/headers/header_navigate.jsp" %>
	<%@ include file="/WEB-INF/views/headers/food_navigate.jsp" %>
	<div id="mw_food">
		<table id="mw_intake">
			<tr>
				<c:if test="${ not empty date }">
					<td colspan=3 class="section_title"> Calorie Intake of Date: ${ date }</td>
				</c:if>
				<c:if test="${ empty date }">
					<td colspan=3 class="section_title">Today's Calorie Intakes</td>
				</c:if>
			</tr>
			<tr>
				<td width="20%" rowspan=2>&nbsp;</td>
				<td id="table_intake" align="center" rowspan=2>
					<div align="center" style="width:80%;">
						<table id="data_header" border="1" width="100%">
							<tr><td width="60%" id="food_name">Food Name</td><td width="40%" id="calo">Calorie</td></tr>
						</table>
					</div>
					<div align="center" style="width:80%; height:65%; overflow:auto;">
						<table id="data" border="1" width="100%" >
							<c:if test="${ empty food_list }">
								<tr><td>Oops, no food record found this day.</td></tr>
							</c:if>
							<c:if test="${ not empty food_list }">
								<c:forEach var="i" begin="1" end="${length}">
									<tr><td width="60%" id="food_name">${food_list[i-1].food }</td>
										<td width="40%" id="calo">${food_list[i-1].calorie }
									</td></tr>
								</c:forEach>
							</c:if>
						</table>
						
					</div>
					
					<div align="center" style="width:80%;">
						<table id="data_footer" border="1" width="100%">
							<tr><td width="60%" id="food_name">Total Calorie</td><td width="40%" id="calo">${total}</td></tr>
						</table>
					</div>
					<div style="margin-top:20px;">
						<form action="/project/food/add_food/" method="POST">
							<input type="hidden" name="date" value="${ date }"/>
							<input type="submit" value="Add Food"/>
						</form>
						</div>
					
				</td>
				<td id="datePicker">Pick Up a Date:<br/>
				<form action="/project/food/intake_calorie/" method="POST">
				<div class="date_pick_display"><input type="text" id="datepicker" name="datepicker" /></div>
				<div class="date_pick_display"><input type="submit" value="Go"/></div>
				</form>
				</td>
			</tr>
			<tr>
				<td id="suggestion">Suggestion:<br />Suggestion Frame</td>
			</tr>
		</table>
		<br>
    		<a href="<c:url value="/activity"/>">Back to Activity</a>
    	<br>
	</div>
</body>
</html>
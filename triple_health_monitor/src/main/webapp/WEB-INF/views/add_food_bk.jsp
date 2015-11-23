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
	<style>
		body {
			margin: 0;
		}
	</style>
	
	<script>
	$(function() {
	    	$( "#datepicker" ).datepicker({ minDate: "-2M", maxDate: "0", dateFormat: "yy-mm-dd"});
	});
	</script>
	
</head>

<body>
	<%@ include file="/WEB-INF/views/headers/header_navigate.jsp" %>
	<%@ include file="/WEB-INF/views/headers/food_navigate.jsp" %>
	<div id="mw_food">
		<h2>Add Food & Calorie</h2>
		<form action="/project/add_food/add/" method="post">
		Date: <input type="text" id="datepicker" name="datepicker" value="${ date }" />
		
		<table id="add_food">
<!-- 			<tr><td class="section_title" colspan=2>Add Food & Calorie</td></tr> -->
			<tr class="food_input"><td>Food 1: <input type="text" name="food_1"/></td>
			<td>Calorie Amount: <input type="text" name="calo_1"/></td></tr>
			<tr class="food_input"><td>Food 2: <input type="text" name="food_2"/></td>
			<td>Calorie Amount: <input type="text" name="calo_2"/></td></tr>
			<tr class="food_input"><td>Food 3: <input type="text" name="food_3"/></td>
			<td>Calorie Amount: <input type="text" name="calo_3"/></td></tr>
			<tr class="food_input"><td>Food 4: <input type="text" name="food_4"/></td>
			<td>Calorie Amount: <input type="text" name="calo_4"/></td></tr>
			<tr class="food_input"><td>Food 5: <input type="text" name="food_5"/></td>
			<td>Calorie Amount: <input type="text" name="calo_5"/></td></tr>
			<tr class="food_input"><td>Food 6: <input type="text" name="food_6"/></td>
			<td>Calorie Amount: <input type="text" name="calo_6"/></td></tr>
			<tr class="food_input"><td>Food 7: <input type="text" name="food_7"/></td>
			<td>Calorie Amount: <input type="text" name="calo_7"/></td></tr>
			<tr class="food_input"><td>Food 8: <input type="text" name="food_8"/></td>
			<td>Calorie Amount: <input type="text" name="calo_8"/></td></tr>
			<tr><td class="submit_button" colspan=2><input type="submit" value="Add"/>
			</td></tr>
		</table>
		</form>
	</div>
	
</body>
</html>
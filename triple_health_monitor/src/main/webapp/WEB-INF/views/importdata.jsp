<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="sf" uri="http://www.springframework.org/tags/form"%> 
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Set a personal activity goal</title>
</head>
<body>
	<h1>You can import spme actvity data here</h1>
	<%-- <form:form method="post" commandName="activity" >
	<table width="95%" bacolor="f8f8ff" border="0" cellspacing="0" cellpadding="5">
		<tr>
			<td align="right" width="20%">Calories</td>
				<td width="20%">
					<form:input path="calories"/>
				</td>
		</tr>
		<tr>
			<td align="right" width="20%">CaloriesOut</td>
				<td width="20%">
					<form:input path="caloriesOut"/>
				</td>
		</tr>
		<tr>
			<td align="right" width="20%">Distance (%)</td>
				<td width="20%">
					<form:input path="distance"/>
				</td>
		</tr>	
	</table>
	<br>
	<input type="submit" align="center" value="Execute">

</form:form> --%>

<sf:form method="POST" commandName="activity">
		<fieldset>
			<table>
				<%-- <tr>
					<th><label for="goal_caloriesOut">CaloriesOut:</label></th>
					<td><sf:input path="caloriesOut"/></td>
				</tr> --%>
				<tr>
					<th><label for="goal_distance">Distance:</label></th>
					<td><sf:input path="distance"/></td>
				</tr>
				<tr>
					<th><label for="goal_floors">Floors:</label></th>
					<td><sf:input path="floors"/></td>
				</tr>
				<tr>
					<th><label for="goal_steps">Steps:</label></th>
					<td><sf:input path="steps"/></td>
				</tr>
			<%-- 	<tr>
					<th><label for="goal_date">Date:</label></th>
					<td><sf:input path="date"/></td>
				</tr> --%>

				
				<tr>
					<th><a href="activity_home"><button>Cancel</button></a></th>
					<td><sf:hidden path="id"/>
					<td><input type="submit" value="Update"/></td>
				</tr>
			</table>
		</fieldset>
	</sf:form>


</body>
</html>	
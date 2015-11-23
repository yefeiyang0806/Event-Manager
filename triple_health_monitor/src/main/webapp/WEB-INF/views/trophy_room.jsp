<%@ page session="false"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %> 
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html lang="en">
  <head>
  <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
     <title>Activity</title>

    <!-- Bootstrap -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">
    <link href="<c:url value="/resources/template/css/carousel.css" />" rel="stylesheet">
    <link href="<c:url value="/resources/template/css/dashboard.css" />" rel="stylesheet"> 
  
    
  </head>
  <body>
  		<%@ include file="/resources/template/jsp/activity_nar_bar.jsp" %>  
  		<div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar" id="wow">
            <li><a href="/project/activity/">Overview <span class="sr-only">(current)</span></a></li>
            <li><a href="/project/activity/goal">Set Goal</a></li>
            <li><a href="/project/activity/activity">Check Activity</a></li>
            <li class="active"><a href="/project/activity/trophy_room">Trophy Room</a></li>
          </ul>
          
</div>	
    
  	 <%@ include file="/WEB-INF/views/headers/footer.jsp" %> 	
  </body>
</html>

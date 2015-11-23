<%@ page session="false"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %> 
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

<html>
  <head><title></title></head>
  <body>

    <h3>User profile</h3>
    
        <c:out value="${now}"/>
    	<table>
    	<c:if test="${ empty user }">
								<tr><td>Oops, there seems is no user.</td></tr>
		</c:if>
		<c:if test="${not empty user }">
			<c:out value="${user.username}"/> <i><c:out value="${user.email}"></c:out></i>
			
		</c:if>
		</table>>
    
    	<a href="<c:url value="/activity"/>">Back to Activity</a>
    	<br>
    	
  </body>
</html>
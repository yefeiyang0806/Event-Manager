<html>
<head>
	<%@ include file="/WEB-INF/views/css/header_style.jsp" %>
	<%@ include file="/WEB-INF/views/css/mw_style.jsp" %>
	<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
	<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
	<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
	<style>
		body {
			margin: 0;
		}
	</style>
</head>
<body>
	<%@ include file="/WEB-INF/views/headers/header_navigate.jsp" %>
	<div id="mw">
		<table>
		<c:if test="${(empty error) and (empty msg)}">
			<tr><td id="login">Please Login</td></tr>
		</c:if>
		<c:if test="${(empty error) and (not empty msg)}">
			<tr><td id="logout">${msg}</td></tr>
		</c:if>
		<c:if test="${(not empty error) and (empty msg)}">
			<tr><td id="login_error">${error}</td></tr>
		</c:if>
			<tr>
				<td>
					<form class="login_table" action="<c:url value='j_spring_security_check'/>" method='POST'>
						<input type="text" name="username" placeholder="Username Here"><br />
						<input type="password" name="password" placeholder="Password Here"><br />
						<input type="submit" value="Login"><br />
						<div id="status"></div><br />
					</form>
				</td></tr>
				<tr><td>
					<div class="panel panel-default">
        				<div class="panel-body">
            				<h2>Social Sign IN:</h2>
            				<div class="row social-button-row">
                				<div class="col-lg-4">
                    				<!-- Add Facebook sign in button -->
                    				<a href="${pageContext.request.contextPath}/auth/facebook"><button class="btn btn-facebook"><i class="icon-facebook"></i>|Sign in with FB</button></a>
                				</div>
            				</div>
        				</div>
        				<div><a href="/project/login/new_page">New Page</a></div>
    				</div>
    			</td></tr>
		</table>
	</div>	
</body>
</html>
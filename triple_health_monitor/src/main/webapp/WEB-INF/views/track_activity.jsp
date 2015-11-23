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
  
    <script type="text/javascript"
          src="https://www.google.com/jsapi?autoload={
            'modules':[{
              'name':'visualization',
              'version':'1',
              'packages':['corechart']
            }]
          }"></script>

    <script type="text/javascript">
      google.setOnLoadCallback(drawChart);

      function drawChart() {
    	  var data = google.visualization.arrayToDataTable([
                                                            ['Date', 'Distance','Floors'],
                                                            <c:forEach items="${activities}" var="entry">
                                                                [ '${entry.date}', ${entry.distance},${entry.floors}],
                                                            </c:forEach>
                                                      ]);

        var options = {
          title: 'Acitivity Performance',
          curveType: 'function',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
  		<%@ include file="/resources/template/jsp/activity_nar_bar.jsp" %>
  		<div class="container-fluid">
		<div class="row">
			<div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar" id="wow">
            <li><a href="/project/activity/">Overview <span class="sr-only">(current)</span></a></li>
            <li><a href="/project/activity/goal">Set Goal</a></li>
            <li class="active"><a href="/project/activity/activity">Check Activity</a></li>
            <li><a href="/project/activity/trophy_room">Trophy Room</a></li>
          </ul>
          
			</div>
			<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">	
   		 		<div id="curve_chart" style="width: 900px; height: 500px; margin-top: 200px; margin-bottom: 200px;">
   		 		</div>
   		 	</div>
   		 </div>
   		</div> 	
  	 <%@ include file="/WEB-INF/views/headers/footer.jsp" %> 	
  </body>
</html>

<%-- 
<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">

      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
                  <c:forEach items="${activities}" var="entry">
                      [ "floor", ${entry.floors}],
                  </c:forEach>
        ]);
        
/*         var data = google.visualization.arrayToDataTable([
                                                          ['Country', 'Area(square km)'],
                                                          <c:forEach items="${pieDataList}" var="entry">
                                                              [ '${entry.key}', ${entry.value} ],
                                                          </c:forEach>
                                                    ]);
 */        

        // Set chart options
        var options = {'title':'How you activities look like',
                       'width':400,
                       'is3D':true,
                       'height':300};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="chart_div"></div>
  </body>
</html> --%>





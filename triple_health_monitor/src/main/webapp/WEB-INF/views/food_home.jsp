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

    <title>Food Homepage</title>

    <!-- Bootstrap core CSS -->
    <link href="<c:url value="/resources/bootstrap-3.3.5-dist/css/bootstrap.min.css" />" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="<c:url value="/resources/template/css/offcanvas.css" />" rel="stylesheet">
    
    <style>
    	.jumbotron {
    		height: 300px;
    		background-size: cover;
    		background-position: 50% 50%;
    		background-repeat: no-repeat;
    	}
    </style>

  </head>

  <body>
  	<c:import url='/resources/template/jsp/food_nav_bar.jsp' />
    <div class="container">

      <div class="row row-offcanvas row-offcanvas-right">

        <div class="col-xs-12 col-sm-9">
          <p class="pull-right visible-xs">
            <button type="button" class="btn btn-primary btn-xs" data-toggle="offcanvas">Toggle nav</button>
          </p>
          <div class="jumbotron" style="background-image: url('<c:url value="/resources/img/diet.jpg"/>')">
            <h1>Eat Healthier</h1>
<!--             <p>This is an example to show the potential of an offcanvas layout pattern in Bootstrap. Try some responsive-range viewport sizes to see it in action.</p> -->
          </div>
          <div class="row">
            <div class="col-xs-9 col-lg-6">
              <h2>Track Easily</h2>
              <p>With the help of <strong>Food Intake</strong> feature, it would be a easy job to record your daily calorie intake. Forget to recode sometimes? No worries. Choose the date and fix it up~</p>
              <p><a class="btn btn-default" href="/project/food/intake_calorie/" role="button">View details &raquo;</a></p>
            </div><!--/.col-xs-6.col-lg-4-->
            <div class="col-xs-9 col-lg-6">
              <h2>Present Vividly</h2>
              <p>Numbers are boring! Have a try on <strong>Compare with others</strong> and view your performance by diagrams. Baselines of average performance of all other users and recommendations would also be provided.</p>
              <p><a class="btn btn-default" href="/project/food/comparison/" role="button">View details &raquo;</a></p>
            </div><!--/.col-xs-6.col-lg-4-->
            <div class="col-xs-9 col-lg-6">
              <h2>Improve Everyday</h2>
              <p>Once a <strong>Diet Task</strong> had been set up, a daily plan would be generated. Perfect for getting better everyday.</p>
              <p><a class="btn btn-default" href="/project/food/diet_tasks/" role="button">View details &raquo;</a></p>
            </div><!--/.col-xs-6.col-lg-4-->
            <div class="col-xs-9 col-lg-6">
              <h2>Keep In-touch</h2>
              <p>Come and have a look at <strong>Food Module Summary</strong> to view the overall performance in Diet Health. Don't be nervous. Your date is kept private.</p>
              <p><a class="btn btn-default" href="/project/food/summary/" role="button">View details &raquo;</a></p>
            </div><!--/.col-xs-6.col-lg-4-->
            
          </div><!--/row-->
        </div><!--/.col-xs-12.col-sm-9-->

        <div class="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar">
          <div class="list-group">
            <a href="#" class="list-group-item active">Food Home Page</a>
            <a href="/project/food/intake_calorie/" class="list-group-item">Calorie Intake</a>
            <a href="/project/food/comparison/" class="list-group-item">Compare With Others</a>
            <a href="/project/food/add_diet/" class="list-group-item">Set Diet Tasks</a>
            <a href="/project/food/diet_tasks/" class="list-group-item">My Diet Tasks</a>
            <a href="/project/food/summary/" class="list-group-item">Food Summary</a>
            <a href="/project/user/update/" class="list-group-item">Update Profile</a>
<!--             <a href="#" class="list-group-item">Link</a> -->
<!--             <a href="#" class="list-group-item">Link</a> -->
<!--             <a href="#" class="list-group-item">Link</a> -->
          </div>
        </div><!--/.sidebar-offcanvas-->
      </div><!--/row-->

      <hr>

      <footer>
        <p>&copy; Company 2014</p>
      </footer>

    </div><!--/.container-->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="<c:url value="/resources/bootstrap-3.3.5-dist/js/bootstrap.min.js" />"></script>

    <script src="<c:url value="/resources/template/js/offcanvas.js" />"></script>
  </body>
</html>

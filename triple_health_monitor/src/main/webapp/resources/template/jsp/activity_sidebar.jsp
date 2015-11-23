<div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar" id="wow">
            <li class="active"><a href="#">Overview <span class="sr-only">(current)</span></a></li>
            <li><a href="/project/activity/set_goal">Set Goal</a></li>
            <li><a href="/project/activity/track_activity">Check Activity</a></li>
            <li><a href="/project/activity/trophy_room">Trophy Room</a></li>
          </ul>
          
</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

<script type="text/javascript" >

	
	$('.nav-sidebar li').click(function(e) {
	    $('.nav-sidebar li.active').removeClass('active');
	    
	    var $this = $(this);
	    if (!$this.hasClass('active')) {
	        $this.addClass('active');
	    }
	   
	    e.preventDefault();
	    window.location = $(this).find('a').attr('href');
	});





</script>
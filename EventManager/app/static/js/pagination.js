    $(document).ready(function() {

      var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
          sURLVariables = sPageURL.split('&'),
          sParameterName,
          i;

        for (i = 0; i < sURLVariables.length; i++) {
          sParameterName = sURLVariables[i].split('=');
          if (sParameterName[0] === sParam) {
              return sParameterName[1] === undefined ? true : sParameterName[1];
          }
        }
      };

      var suffix = '';
      if (getUrlParameter('content')!=null){
        suffix += '&content=' + getUrlParameter('content');
      }
      if (getUrlParameter('format')!=null){
        suffix += '&format=' + getUrlParameter('format');
      }
      if (getUrlParameter('location')!=null){
        suffix += '&location=' + getUrlParameter('location');
      }

      var current_page;
      if (getUrlParameter('page')==null){
        current_page = 1;
      }
      else {
        current_page = parseInt(getUrlParameter('page'));
      }
      var page_count = $('#page_count').val();
      var group = Math.floor(current_page/8);
      if (current_page % 8 == 0){
        group --;
      }
      for (var i=Math.min(group*8+8, page_count); i>=group*8+1; i--){
        if (i != current_page){
          $('#add_page_number').after('<li><a href="?page=' + i + suffix + '">' + i+ '</a></li>');
        }
        else {
          $('#add_page_number').after('<li class="active"><a href="?page=' + i + suffix + '">' + i+ '</a></li>');
        }
      }

      $('#previous_page').click(function(){
        if (current_page > 1){
          var previous_page = current_page-1;
          window.location.href = '?page=' + previous_page + suffix;
        }
      });

      $('#next_page').click(function(){
        var current_page = parseInt(getUrlParameter('page'));
        if (current_page < page_count){
          var next_page = current_page+1;
          window.location.href = '?page=' + next_page + suffix;
        }
      });

      $('#first_page').click(function(){
        if (current_page != 1){
          window.location.href = '?page=1' + suffix;
        }
      });

      $('#last_page').click(function(){
        if (current_page != page_count){
          window.location.href = '?page=' + page_count + suffix;
        }
      });

    });
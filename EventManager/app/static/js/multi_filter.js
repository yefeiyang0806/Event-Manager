    $(document).ready(function() {

      $('.dropdown-content ul').css('display', 'none');

      //Set the selected option based on the URL
      var url_location = getUrlParameter('location');
      var url_keyword = getUrlParameter('keyword');
      var url_content = getUrlParameter('content');
      var url_format = getUrlParameter('format');
      // $("#location-filter").find("option").each(function(){
        // if ($(this).text() == url_location){
          // $(this).prop('selected', true);
        // }
      // });
      var multi_contents = url_content.split(',');
      // console.log(multi_contents);
      var multi_formats = url_format.split(',');
      $("#content-filter").find('input[type="checkbox"]').each(function(){
        if ($.inArray($(this).attr('id'), multi_contents) != -1){
          $(this).prop('checked', true);
        }
        else {
          $(this).prop('checked', false);
        }
      });
      $("#format-filter").find('input[type="checkbox"]').each(function(){
        if ($.inArray($(this).attr('id'), multi_formats) != -1){
          $(this).prop('checked', true);
        }
        else {
          $(this).prop('checked', false);
        }
        // console.log($(this).attr('id'));
      });
      $('#keyword').val(url_keyword);

      //show the checked checboxes on span.
      $('input[type="checkbox"]').each(function(){
        if ($(this).is(':checked')) {
          if ($(this).closest('.dropdown-checkbox').find('.hida').length){
            $(this).closest('.dropdown-checkbox').find(".hida").remove();
          }
          var clicked = $(this).val();
          clicked = $.trim(clicked) + ', ';
          var html = '<span title="' + clicked + '">' + clicked + '</span>';
          $(this).closest('.dropdown-checkbox').find('.multiSel').append(html);
        }
      });
  
      $('.dropdown-trigger').click(function(){
        $(this).next().children('ul').slideToggle('fast');
      });

      $('.dropdown-content input[type="checkbox"]').click(function(){
        var clicked = $(this).val();
        clicked = $.trim(clicked) + ', ';
        if ($(this).is(':checked')) {
          var html = '<span title="' + clicked + '">' + clicked + '</span>';
          $(this).closest('.dropdown-checkbox').find('.multiSel').append(html);
          // console.log($(this).closest('.dropdown-checkbox').children('.multiSel'));
          $(this).closest('.dropdown-checkbox').find(".hida").remove();
        }
        else{
          $('span[title="' + clicked + '"]').remove();
          if ($(this).closest('.dropdown-checkbox').find('.multiSel').children().length==0){
            $(this).closest('.dropdown-checkbox').find('a').prepend('<span class="hida">Select Content</span>');
          }
        }
      });

      $(document).bind('click', function(e) {
        var $clicked = $(e.target);
        if (!$clicked.parents().hasClass("dropdown-checkbox") && !$clicked.parents().hasClass("dropdown-content")){
          $(".dropdown-content ul").hide();
        }
      });

      function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1));
        var sURLVariables = sPageURL.split('&');

        for (i = 0; i < sURLVariables.length; i++) {
          var sParameterName = sURLVariables[i].split('=');
          if (sParameterName[0] === sParam) {
            return sParameterName[1];
          }
        }
        return '';
      }

    });
    $(document).ready(function() {

      var appointments = new Array();
      var csrftoken = $('meta[name=csrf-token]').attr('content');
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });

      // create color legends for different contents
      var red = 200;
      var green = 80;
      var blue = 125;
      $('.color-box').each(function(){
        red += 37;
        green -= 47;
        blue += 59;
        if (red > 255){
          red -= 255;
        }
        if (green < 0){
          green += 255;
        }
        if (blue > 255){
          blue -= 255;
        }
        var color_str = 'rgb(' + red + ',' + green + ',' + blue + ')';
        // console.log(color_str)
        $(this).css('background-color', color_str);
      });

      // initialize the filter related values
      var modified_list = [];
      var current_content = '';
      var current_format = '';
      $(".format-checkbox:checked").each(function(){
        current_format += $(this).val() + ',';
      });
      // console.log(current_format);
      $(".content-checkbox:checked").each(function(){
        current_content += $(this).val() + ',';
      });
      // console.log(current_content);
      var current_location = $("#location-filter").find(":selected").text();

      $("#reset_schedule").click(function(){
        var reset_url = "/topic/reset_schedule";

        $("#dialog_reset").dialog({
          width:400,
          height:240,
          modal: true,
          buttons: {
            Confirm: function() {
              $( this ).dialog( "close" );
              remove_schedule_records();
              recreate_scheduler();
            },
            Cancel: function() {
              $( this ).dialog( "close" );
            }
          }
        });
      });

      $('#scheduler_wrapper').on('appointmentChange', '#scheduler', function (event) {
        var default_duration = 20;
        var args = event.args;
        var appointment = args.appointment;
        var format = appointment['location'].split(' (')[0];
        // console.log(format);
        var set_default = $('.default-text:contains("'+format+'")').find('input').val();
        if ($.inArray(appointment['id'], modified_list) == -1){
          modified_list.push(appointment['id']);
        }
        var from = $("#scheduler").jqxScheduler('getAppointmentProperty', appointment['id'], 'from');
        // console.log(set_default);
        if (set_default == null || set_default == ''){
          $("#scheduler").jqxScheduler('setAppointmentProperty', appointment['id'], 'to', from.addMinutes(default_duration));
        }
        else {
          $("#scheduler").jqxScheduler('setAppointmentProperty', appointment['id'], 'to', from.addMinutes(set_default));
        }
        
        // $("#scheduler").jqxScheduler('setAppointmentProperty', appointment['id'], 'background', 'yellow');
        // $("#scheduler").jqxScheduler('beginAppointmentsUpdate');
        // $("#scheduler").jqxScheduler('endAppointmentsUpdate');
      });

      $('#scheduler_update').click(function(){
        var data = [];
        $.each(modified_list, function(key, value){
          var scheduler_ele = $("#scheduler_wrapper").find('#scheduler');
          var res = scheduler_ele.jqxScheduler('getAppointmentProperty', value, 'resourceId');
          var from = scheduler_ele.jqxScheduler('getAppointmentProperty', value, 'from').toString('HH:mm:ss');
          var to = scheduler_ele.jqxScheduler('getAppointmentProperty', value, 'to').toString('HH:mm:ss');
          var date = scheduler_ele.jqxScheduler('getAppointmentProperty', value, 'to').toString('yyyy-MM-dd');
          var record = {'topic_id': value, 'resource': res, 'time_from': from, 'time_to': to, 'date': date};
          // if (res != 'TBD'){
          data.push(record);  
          // }
          // Get modified date and resource ---- Done!
          // Generate json with id, from, to and resource ---- Done!
          // Send back to the validation function to do validation ---- Done!
          // Get response from topic/views.py ---- Done!
          // Reset modified_list to empty ---- Done!
        });
        // console.log(data);
        $.ajax({
          type: "POST",
          contentType: "application/json",
          dataType: "json",
          url: "/topic/validate_arrangement",
          data: JSON.stringify({ "schedule": data }),
          success: function(data){
            if (data['status']){
              alert("Topic schedule updating status: " + data['status']);
              modified_list = [];
            }
            else if (data['ErrorMessage']){
              err_msg = data['ErrorMessage'];
              $('#err_msgs').empty();
              $('#err_msgs').append('<ul>');
              $.each(err_msg, function(key, value){
                $('#err_msgs').append("<li><b>'"+value['title']+"'</b>: "+value['message']+'</li>');
              });
              $('#err_msgs').append('</ul>');
              $('#err_msgs').append('<br /><div><font style="text-decoration:underline;">Please fix the conflicts before updating the schedule.</font></div>');
              $('#err_msgs').dialog({
                width:480,
                height:240,
                modal: true
              });
            }
          }
        });
      });

      $("#set_filter").click(function(){
        $('.scheduler-hide').each(function(){
          $(this).show();
        });
        if (modified_list.length>0){
          $('#scheduler_update').click();
        }
        // else {
        recreate_scheduler();
        // }
        // $("#filter_notice").remove();
      });

      // $("#excelExport").jqxButton();
      $("#icalExport").jqxButton();

      // $("#excelExport").click(function () {
        // $("#scheduler").jqxScheduler('exportData', 'xls');
      // });

      $("#icalExport").click(function () {
        $("#scheduler").jqxScheduler('exportData', 'ics');
      });

     // $("#set_filter").trigger('click');
      // extractContentColor('DFSD (S/4HANA)');

      function remove_schedule_records(){
        var remove_conditions = [];
        if (current_content != "any"){
          remove_conditions.push({'type': 'content', 'value': current_content});
        }
        if (current_format != "any"){
          remove_conditions.push({'type': 'format', 'value': current_format});
        }
        if (current_location != "------Any------"){
          remove_conditions.push({'type': 'location', 'value': current_location});
        }
        $.ajax({
          type: "POST",
          contentType: "application/json",
          dataType: "json",
          url: "/topic/reset_schedule",
          data: JSON.stringify({ "remove_conditions": remove_conditions }),
        });
      }

      function extractContentColor(app_location){
        var content_str = app_location.match(/\((.*?)\)/);
        var content = content_str[1];
        var colorbox = $('.legend-text:contains("' + content + '")').next('.color-box').css('background-color');
        var rgb_color = colorbox.match(/\((.*?)\)/)[1].split(',');
        // console.log(rgb_color);
        var color_str = '#' + componentToHex(parseInt(rgb_color[0])) + componentToHex(parseInt(rgb_color[1])) + componentToHex(parseInt(rgb_color[2]));
        return color_str;
      }

      function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
      }

      function recreate_scheduler(){
        var filter_data = [];
        var content_id = '';
        var format_id = '';
        var location = $("#location-filter").find(":selected").text();
        var keyword = $("#keyword").val();
        $(".format-checkbox:checked").each(function(){
          format_id += $(this).val() + ',';
        });
        // console.log(format_id);
        $(".content-checkbox:checked").each(function(){
          content_id += $(this).val() + ',';
        });
        // console.log(content_id);
        current_content = content_id;
        current_format = format_id;
        current_location = location;
        if (content_id != "any"){
          filter_data.push({'type': 'content', 'value': content_id});
        }
        if (format_id != "any"){
          filter_data.push({'type': 'format', 'value': format_id});
        }
        if (location != "------Any------"){
          filter_data.push({'type': 'location', 'value': location});
        }
        if (keyword != ''){
          filter_data.push({'type': 'keyword', 'value': keyword});
        }
        $.ajax({
          type: "POST",
          contentType: "application/json",
          dataType: "json",
          url: "/topic/ajax_schedule",
          data: JSON.stringify({ "filters": filter_data }),
          success: function(data){
            var source =
              {
                dataType: "json",
                dataFields: [
                  { name: 'topic_id', type: 'string' },
                  { name: 'contentFormat', type: 'string'},
                  { name: 'description', type: 'string' },
                  { name: 'year', type: 'string' },
                  { name: 'topic_title', type: 'string' },
                  { name: 'resource', type: 'string' },
                  { name: 'from', type: 'date' },
                  { name: 'to', type: 'date' }
                ],
                id: 'topic_id',
                localData: data
              };
            var resource_url = '/topic/ajax_resources';
            if (format_id != 'any'){
              resource_url += '/' + format_id;
            }
            var data_of_resources = 
              {
                dataType: "json",
                dataFields: [
                  { name: 'resource', type: 'string' },
                ],
                id: 'topic_id',
                url: resource_url,
              };

            var adapter = new $.jqx.dataAdapter(source);
            $("#scheduler").jqxScheduler('destroy');
            $("#scheduler_wrapper").append('<div id="scheduler" width="100%"></div>');
            $("#scheduler").jqxScheduler({
              date: new $.jqx.date(2015, 12, 28),
              width: '90%',
              height: 800,
              rowsHeight: 30,
              dayNameFormat: "abbr",
              source: adapter,
              // showLegend: true,
              legendHeight: 100,
              ready: function () {
                    
              },
              renderAppointment: function(data){
                var color = extractContentColor(data.appointment.location);
                data.background = color;
                return data;
              },
              editDialogCreate: function (dialog, fields, editAppointment) {
                var assigned_content_format = null;
                if (editAppointment != null){
                  assigned_content_format = editAppointment.location;
                }
                var format_field = "<div><div class='jqx-scheduler-edit-dialog-label'>Format</div><div class='jqx-scheduler-edit-dialog-field'><input class='jqx-widget-content jqx-input jqx-widget jqx-rc-all' style='width:100%;height:25px;' value='" + assigned_content_format + "' disabled /></div></div>";
                fields.repeatContainer.hide();
                fields.statusContainer.hide();
                fields.allDayContainer.hide();
                fields.colorContainer.hide();
                fields.timeZoneContainer.hide();
                fields.locationContainer.hide();
                fields.resourceLabel.html('Resource');
                fields.subject.prop('disabled', true);
                fields.description.prop('disabled', true);
                fields.description.attr('rows', '8');
                fields.subject.parent().after(format_field);
              },
              editDialogOpen: function (dialog, fields, editAppointment) {
                if (editAppointment != null){
                  fields.subject.parent().next().find('input').val(editAppointment.location);
                }
                else {
                  fields.subject.parent().next().find('input').val('');
                }
              },
              resources:
              {
                colorScheme: "scheme05",
                dataField: "resource",
                orientation: "horizontal",
                resourceColumnWidth: 120,
                source:  new $.jqx.dataAdapter(data_of_resources)
              },
              appointmentDataFields:
              {
                from: "from",
                to: "to",
                id: "topic_id",
                description: "description",
                location: "contentFormat",
                // location: "resource",
                subject: "topic_title",
                resourceId: "resource",
              },
              view: 'dayView',
              views:
              [
                { type: 'dayView', showWeekends: false, timeRuler: { scaleStartHour: 10, scaleEndHour: 21, scale: "tenMinutes", formatString: "HH:mm" }, appointmentsRenderMode: "exactTime" },
                // { type: 'agendaView' }
              ]
            });
          }
        });
      }

    });
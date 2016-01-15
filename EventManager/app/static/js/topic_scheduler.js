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

      var modified_list = [];
      var current_content = $("#content-filter").find(":selected").val();
      var current_format = $("#format-filter").find(":selected").val();
      var current_location = $("#location-filter").find(":selected").text();

      $("#set_filter").click(function(){
        if (modified_list.length>0){
          $('#dialog').dialog({
            width:400,
            height:240,
            modal: true,
            buttons: {
              Confirm: function() {
                $( this ).dialog( "close" );
                recreate_scheduler();
              },
              Cancel: function() {
                $( this ).dialog( "close" );
              }
            }
          });
        }
        else {
          recreate_scheduler();
        }
      });

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
        var args = event.args;
        var appointment = args.appointment;
        if ($.inArray(appointment['id'], modified_list) == -1){
          modified_list.push(appointment['id']);
        }
        
        $("#scheduler").jqxScheduler('beginAppointmentsUpdate');
        // $("#scheduler").jqxScheduler('setAppointmentProperty', appointment['id'], 'borderColor', 'red');
        $("#scheduler").jqxScheduler('endAppointmentsUpdate');
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
          if (res != 'TBD'){
            data.push(record);  
          }
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

     // $("#set_filter").trigger('click');

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

      function recreate_scheduler(){
        var filter_data = [];
        var content_id = $("#content-filter").find(":selected").val();
        var format_id = $("#format-filter").find(":selected").val();
        var location = $("#location-filter").find(":selected").text();
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
              showLegend: true,
              legendHeight: 100,
              ready: function () {
                    
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
                subject: "topic_title",
                resourceId: "resource",
              },
              view: 'dayView',
              views:
              [
                { type: 'dayView', showWeekends: false, timeRuler: { scaleStartHour: 8, scaleEndHour: 21, scale: "tenMinutes", formatString: "HH:mm" }, appointmentsRenderMode: "exactTime" },
                { type: 'weekView', showWeekends: false }
              ]
            });
          }
        });
      }

    });
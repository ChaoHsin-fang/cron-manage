
// 创建定时按钮
$('#addBtn').click(function(){
  // $('#myModalLabel').html(returni18('newly.build')+returni18('timing.task'));
  // $('#crontab-time-modal').modal('hide');
  // $('#crontabName').val(null);
  // // 监控input字段长度 start
  // $('#crontabName').on('input onpropertychange', function (){
  //   var val = $(this).val();
  //   if(val.length== 25){
  //     $(this).popover({"viewport":false})
  //            .popover('show')
  //   }else{
  //     $(this).popover('hide');
  //   }
  // });
  // // 监控input字段长度 end
  // $('#crontabDes').val(null);
  // $('#cronExpression').val(null);
  // $('#crontabTaskId').val(null)
  // $('#taskId').empty();
  // $('#taskId').parent().parent().show();
  // $('#taskName').val(null).parent().parent().addClass('none');
  // $.ajax({
  //   type : 'POST',
  //   url : basePath+'nm/jobs/jobsAction!getTaskList.action',
  //   dataType : 'json',
  //   success : function(result) {
  //     var rdata = result.data;
  //     if(rdata){
  //       var html =''; 
  //       $.each(rdata,function(i,opt){
  //         if(opt.id == cacheTaskId){
  //           html += '<option value="'+opt.id+'" selected>'+opt.name+'</option>'
  //         }else{
  //           html += '<option value="'+opt.id+'">'+opt.name+'</option>'
  //         }
  //       })
  //       $('#taskId').append(html);
  //       $('#taskId').chosen({no_results_text:returni18('nothing'),width:'400px'});
  //     }
  //   }
  // });
  // CronTab({
  //   cronMode : 0,
  //   expression : '0 0/5 * * * ?'
  // })
  $('#crontab-time-modal').modal('show').draggable({
    cursor: "pointer",
    handle: "div.modal-header"
  });
});
/**
 * 
 */
var CronTab = (function(_config){
	var _default = {
			cronMode : 0,
			expression : '0 0/5 * * * ?'
		},
		config  = $.extend({},_default,_config),
		nodeObj = {
			_cronMode :  $('input[name=cronMode]:radio'),
			_cronBox  :  $('#cron-box'),
			_cronDefine : $('#cron-define'),
			
			_minMode : $('input[name=minMode]:radio'),
			_minFrom : $('input[name="min-from"]'),
			_minSpace : $('input[name="min-space"]'),
			_minCheck : $('input[name="min-checkbox"]:checkbox'),
			
			_hourMode : $('input[name=hourMode]:radio'),
			_hourCheck : $('input[name="hour-checkbox"]:checkbox'),
			
			_dayMode : $('input[name=dayMode]:radio'),
			_dayCheck : $('input[name="day-checkbox"]:checkbox'),
			
			_monthMode : $('input[name=monthMode]:radio'),
			_monthCheck : $('input[name="month-checkbox"]:checkbox'),
			
			_weekEnable : $('input[name=weekEnable]:checkbox'),
			_weekMode : $('input[name=weekMode]:radio'),
			_weekCheck : $('input[name="week-checkbox"]:checkbox'),
			
			_cronExpression_0 : $('#cron-box').find('input[name=cronExpression]'),
			_cronExpression_1 : $('#cron-define').find('input[name=cronExpression]')
		},
		my = {
			
			second : '0',
			min :'',
			hour : '',
			day : '',
			month : '',
			week : '',
			
			_explainExpression : function(_value){
				var value = $.trim(_value);
				if(value){
					var array = value.split(' ');
					my.second = array[0];
					my.min = array[1];
					my.hour = array[2];
					my.day = array[3];
					my.month = array[4];
					my.week = array[5];
				}
			},
			_getExpression : function(){
				var value = [my.second,my.min,my.hour,my.day,my.month,my.week];
				return value.join(' ');
			}
		},
		that = {
		};

	//定时规则选择模式切换
	nodeObj._cronMode.on('change',function(){
		var _this = $(this);
		if(_this.hasClass('cron-sel')){
			nodeObj._cronBox.removeClass('none');
			nodeObj._cronDefine.addClass('none');
		}else if(_this.hasClass('cron-def')){
			nodeObj._cronBox.addClass('none');
			nodeObj._cronDefine.removeClass('none');
			nodeObj._cronExpression_1.val(nodeObj._cronExpression_0.val());
		}
		nodeObj._cronMode.removeClass('active');
		_this.addClass('active');
	});
	
	//分钟模式切换
	nodeObj._minMode.on('change',function(){
		var _this = $(this);
		if(_this.hasClass('min-loop')){
			nodeObj._minFrom.prop('disabled',false);
			nodeObj._minSpace.prop('disabled',false);
			nodeObj._minCheck.prop('disabled',true);
			my.min = nodeObj._minFrom.val()+'/'+nodeObj._minSpace.val();
		}else if(_this.hasClass('min-designated')){
			nodeObj._minFrom.prop('disabled' , true);
			nodeObj._minSpace.prop('disabled', true);
			nodeObj._minCheck.prop('disabled', false);
			var checkValues = [];
			$.each(nodeObj._minCheck,function(i , opt){
				if($(opt).prop('checked')){
					checkValues.push($(opt).val());
				}
			});
			if(checkValues.length>0){
				my.min = checkValues.join(',');
			}
		}
		nodeObj._cronExpression_0.val(my._getExpression());
		nodeObj._minMode.removeClass('active');
		_this.addClass('active');
	});
	//分钟开始时间blur事件
	nodeObj._minFrom.on('change',function(){
		// debugger
		var _this = $(this) , value = _this.val();
		if(value === "" ||  value < 0 || value.indexOf('-')!= -1){
			_this.val(0);
			return;
		}
		value = parseInt(value,10);
		if(value>=60){
			value = 59;
		}
		if(value< 0){
			value = 0;
		}
		_this.val(value); 
		my.min = value+'/'+parseInt(nodeObj._minSpace.val(),10);
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	//分钟开始时间blur事件
	nodeObj._minSpace.on('change',function(){
		var _this = $(this) , value = _this.val();
		if(value === "" || value <= 0  || value.indexOf('-')!= -1){
			_this.val(1);
			return;
		}
		value = parseInt(value,10);
		// if(value>50){
		// 	value = 50;
		// }
		if(value>=60){
			value = 59;
		}
		_this.val(value); 
		my.min = parseInt(nodeObj._minFrom.val(),10)+'/'+value;
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	
	//指定分钟click事件
	nodeObj._minCheck.on('click',function(){
		var checkValues = [];
		$.each(nodeObj._minCheck,function(i , opt){
			if($(opt).prop('checked')){
				checkValues.push($(opt).val());
			}
		});
		if(checkValues.length>0){
			my.min = checkValues.join(',');
		}else{
			my.min = nodeObj._minFrom.val()+'/'+nodeObj._minSpace.val();
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	
	//小时模式切换
	nodeObj._hourMode.on('change',function(){
		var _this = $(this);
		if(_this.hasClass('hour-loop')){
			nodeObj._hourCheck.prop('disabled',true);
			my.hour = '*';
		}else if(_this.hasClass('hour-designated')){
			nodeObj._hourCheck.prop('disabled',false);
			var checkValues = [];
			$.each(nodeObj._hourCheck,function(i , opt){
				if($(opt).prop('checked')){
					checkValues.push($(opt).val());
				}
			});
			if(checkValues.length>0){
				my.hour = checkValues.join(',');
			}
		}
		nodeObj._cronExpression_0.val(my._getExpression());
		nodeObj._hourMode.removeClass('active');
		_this.addClass('active');
	});
	//指定小时click事件
	nodeObj._hourCheck.on('click',function(){
		var checkValues = [];
		$.each(nodeObj._hourCheck,function(i , opt){
			if($(opt).prop('checked')){
				checkValues.push($(opt).val());
			}
		});
		if(checkValues.length>0){
			my.hour = checkValues.join(',');
		}else{
			my.hour = '*';
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	
	
	//天数模式切换
	nodeObj._dayMode.on('change',function(){
		var _this = $(this);
		if(_this.hasClass('day-loop')){
			nodeObj._dayCheck.prop('disabled',true);
			my.day = '*';
		}else if(_this.hasClass('day-designated')){
			nodeObj._dayCheck.prop('disabled',false);
			var checkValues = [];
			$.each(nodeObj._dayCheck,function(i , opt){
				if($(opt).prop('checked')){
					checkValues.push($(opt).val());
				}
			});
			if(checkValues.length>0){
				my.day = checkValues.join(',');
			}
		}
		my.week = '?';
		nodeObj._weekEnable.prop('checked',false);
		nodeObj._weekMode.prop('disabled',true);
		nodeObj._weekCheck.prop('disabled',true);
		
		nodeObj._cronExpression_0.val(my._getExpression());
		nodeObj._dayMode.removeClass('active');
		_this.addClass('active');
	});
	//指定天数click事件
	nodeObj._dayCheck.on('click',function(){
		var checkValues = [];
		$.each(nodeObj._dayCheck,function(i , opt){
			if($(opt).prop('checked')){
				checkValues.push($(opt).val());
			}
		});
		if(checkValues.length>0){
			my.day = checkValues.join(',');
		}else{
			my.day = '*';
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	
	//月模式切换
	nodeObj._monthMode.on('change',function(){
		var _this = $(this);
		if(_this.hasClass('month-loop')){
			nodeObj._monthCheck.prop('disabled',true);
			my.month = '*';
		}else if(_this.hasClass('month-designated')){
			nodeObj._monthCheck.prop('disabled',false);
			var checkValues = [];
			$.each(nodeObj._monthCheck,function(i , opt){
				if($(opt).prop('checked')){
					checkValues.push($(opt).val());
				}
			});
			if(checkValues.length>0){
				my.month = checkValues.join(',');
			}
		}
		nodeObj._cronExpression_0.val(my._getExpression());
		nodeObj._monthMode.removeClass('active');
		_this.addClass('active');
	});
	
	//指定月click事件
	nodeObj._monthCheck.on('click',function(){
		var checkValues = [];
		$.each(nodeObj._monthCheck,function(i , opt){
			if($(opt).prop('checked')){
				checkValues.push($(opt).val());
			}
		});
		if(checkValues.length>0){
			my.month = checkValues.join(',');
		}else{
			my.month = '*';
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	
	//周模式生效
	nodeObj._weekEnable.on('change',function(){
		var _this = $(this);
		if(_this.prop('checked')){
			_this.addClass('active');
			nodeObj._weekMode.prop('disabled',false);
			nodeObj._weekCheck.prop('disabled',false);
			$.each(nodeObj._weekMode,function(){
				var modeNode = $(this); 
				if(modeNode.prop('checked')){
					modeNode.trigger('change');
				}
			});
			nodeObj._dayCheck.prop('disabled',true);
			my.day = '?';
		}else{
			nodeObj._weekMode.prop('disabled',true);
			_this.removeClass('active');
			my.week = '?';
			nodeObj._dayCheck.prop('disabled',false);
			nodeObj._dayMode.prop('disabled',false);
			$.each(nodeObj._dayMode,function(){
				var dayNode = $(this); 
				if(dayNode.prop('checked')){
					dayNode.trigger('change');
				}
			});
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	//周模式切换
	nodeObj._weekMode.on('change',function(){
		var _this = $(this);
		if(_this.hasClass('week-loop')){
			nodeObj._weekCheck.prop('disabled',true);
			my.week = '*';
		}else if(_this.hasClass('week-designated')){
			nodeObj._weekCheck.prop('disabled',false);
			var checkValues = [];
			$.each(nodeObj._weekCheck,function(i , opt){
				if($(opt).prop('checked')){
					checkValues.push($(opt).val());
				}
			});
			if(checkValues.length>0){
				my.week = checkValues.join(',');
			}
		}
		nodeObj._cronExpression_0.val(my._getExpression());
		nodeObj._dayMode.removeClass('active');
		_this.addClass('active');
	});
	//指定周click事件
	nodeObj._weekCheck.on('click',function(){
		var checkValues = [];
		$.each(nodeObj._weekCheck,function(i , opt){
			if($(opt).prop('checked')){
				checkValues.push($(opt).val());
			}
		});
		if(checkValues.length>0){
			my.week = checkValues.join(',');
		}else{
			my.week = '*';
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	});
	
	function init(){
		// 国际化
		if(lang == 'zh_CN'){
			$('#cron-file').attr('src', basePath+ 'img/cron-d.png')
		}else{
			$('#cron-file').attr('src', basePath+ 'img/cron-e.png')
		}
		if(config.cronMode==1){
			nodeObj._cronMode.eq(1).trigger('click');
			nodeObj._cronExpression_1.val(config.expression);
			my._explainExpression(_default.expression);
		}else{
			nodeObj._cronMode.eq(0).trigger('click');
			my._explainExpression(config.expression);
			if(my.min){
				if(/^\d{1,2}\/\d{1,2}$/.test(my.min)){
					var arr = my.min.split('\/');
					nodeObj._minFrom.val(arr[0]);
					nodeObj._minSpace.val(arr[1]);
					nodeObj._minMode.eq(0).prop('checked',true);
					nodeObj._minFrom.prop('disabled',false);
					nodeObj._minSpace.prop('disabled',false);
					nodeObj._minCheck.prop('checked',false);
					nodeObj._minCheck.prop('disabled',true);
				}else if(/^(\d{1,2},)*\d{1,2}$/g.test(my.min)){
					var arr = my.min.split(',');
					$.each(arr, function(i, n){
						if(nodeObj._minCheck.eq(n)){
							nodeObj._minCheck.eq(n).prop('checked',true);
						}
					})
					nodeObj._minMode.eq(1).prop('checked',true);
					nodeObj._minFrom.prop('disabled',true);
					nodeObj._minSpace.prop('disabled',true);
					nodeObj._minCheck.prop('disabled',false);
				}else{
					nodeObj._minFrom.val(0);
					nodeObj._minSpace.val(5);
					nodeObj._minMode.eq(0).prop('checked',true);
					nodeObj._minFrom.prop('disabled',false);
					nodeObj._minSpace.prop('disabled',false);
					nodeObj._minCheck.prop('checked',false);
					nodeObj._minCheck.prop('disabled',true);
				}
			}
			if(my.hour){
				if(/^(\d{1,2},)*\d{1,2}$/g.test(my.hour)){
					var arr = my.hour.split(',');
					$.each(arr, function(i, n){
						if(nodeObj._hourCheck.eq(n)){
							nodeObj._hourCheck.eq(n).prop('checked',true);
						}
					})
					nodeObj._hourMode.eq(1).prop('checked',true);
					nodeObj._hourCheck.prop('disabled',false);
				}else{
					nodeObj._hourMode.eq(0).prop('checked',true);
					nodeObj._hourCheck.prop('checked',false);
					nodeObj._hourCheck.prop('disabled',true);
				}
			}
			if(my.day){
				if(/^(\d{1,2},)*\d{1,2}$/g.test(my.day)){
					var arr = my.day.split(',');
					$.each(arr, function(i, n){
						if(nodeObj._dayCheck.eq(n-1)){
							nodeObj._dayCheck.eq(n-1).prop('checked',true);
						}
					})
					nodeObj._dayMode.eq(1).prop('checked',true);
					nodeObj._dayCheck.prop('disabled',false);
				}else{
					nodeObj._dayMode.eq(0).prop('checked',true);
					nodeObj._dayCheck.prop('checked',false);
					nodeObj._dayCheck.prop('disabled',true);
				}
			}
			if(my.month){
				if(/^(\d{1,2},)*\d{1,2}$/g.test(my.month)){
					var arr = my.month.split(',');
					$.each(arr, function(i, n){
						if(nodeObj._monthCheck.eq(n-1)){
							nodeObj._monthCheck.eq(n-1).prop('checked',true);
						}
					})
					nodeObj._monthMode.eq(1).prop('checked',true);
					nodeObj._monthCheck.prop('disabled',false);
				}else{
					nodeObj._monthMode.eq(0).prop('checked',true);
					nodeObj._monthCheck.prop('checked',false);
					nodeObj._monthCheck.prop('disabled',true);
				}
			}
			if(my.week){
				if(/^\?$/.test(my.week)){
					nodeObj._weekEnable.prop('checked',false);
					nodeObj._weekMode.prop('disabled',true);
					nodeObj._weekCheck.prop('checked',false);
					nodeObj._weekCheck.prop('disabled',true);
				}else if(/^(\d{1,2},)*\d{1,2}$/g.test(my.week)){
					var arr = my.week.split(',');
					$.each(arr, function(i, n){
						if(nodeObj._weekCheck.eq(n-1)){
							nodeObj._weekCheck.eq(n-1).prop('checked',true);
						}
					});
					nodeObj._weekEnable.prop('checked',true);
					nodeObj._weekMode.prop('disabled',false);
					nodeObj._weekMode.eq(1).prop('checked',true);
					nodeObj._weekCheck.prop('disabled',false);
					nodeObj._dayCheck.prop('disabled',true);
					my.day = '?';
					
				}else if(/^\*$/.test(my.week)){
					nodeObj._weekEnable.prop('checked',true);
					nodeObj._weekMode.prop('disabled',false);
					nodeObj._weekMode.eq(0).prop('checked',true);
					nodeObj._weekCheck.prop('checked',false);
					nodeObj._weekCheck.prop('disabled',true);
					nodeObj._dayCheck.prop('disabled',true);
					my.day = '?';
				}
			}
		}
		nodeObj._cronExpression_0.val(my._getExpression());
	}
	init();
	return that;
});
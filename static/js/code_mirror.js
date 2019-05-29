$(function($){
  var codeText = $('#code_box').html();
  var editor = CodeMirror.fromTextArea(document.getElementById("editor2_demo"), {
    lineNumbers: true,
    mode: "shell",
		matchBrackets: true,
		theme:'monokai', //编辑器主题
		readOnly:true
  });
  editor.setValue(codeText);
})

// 脚本来源
$('input[name=scriptFrom]:radio').click(function(){
	var type = this.value;		 
	if(type == 1){
		$('#commonScript').hide(400);
		$('#inspectionTemplate').show(400);
	}
	else if(type == 2 ){
		$('#commonScript').show(400);
		$('#inspectionTemplate').hide(400);
	}
});
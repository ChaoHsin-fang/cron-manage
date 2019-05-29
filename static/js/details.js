var codeText = $('#code_box').text();
var editor = CodeMirror.fromTextArea(document.getElementById("editor2_demo"), {
  lineNumbers: true,
  mode: "shell",
  matchBrackets: true,
  theme:'monokai', //编辑器主题
  autoFocus:true,
  readOnly:true
});
editor.setValue(codeText);

// $(function($){
  

// })

function ScriptContent(ScriptId) {
//   var d_content = '<textarea class="form-control" style="height:60px;">' + ScriptId +'</textarea>'
//   var d = dialog({
//     width: 260,
//     title: '脚本内容',
//     content: d_content,
//     // okValue: '确定',
//     // ok: function() {
//     //     // do something
//     // },
//     cancelValue: '关闭',
//     cancel: function() {
//         // do something
//     }
// });
// d.showModal();
// $('#code-info-modal').modal('show').draggable({
//   cursor: "pointer",
//   handle: "div.modal-header"
// });
$('#code-info-modal').modal('show');

}
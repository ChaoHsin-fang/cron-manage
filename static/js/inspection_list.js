$(function () {
  //普通对话框
  $(".dome-box").click(function() {
    var d = dialog({
        width: 260,
        title: '确定删除?',
        quickClose: true,
        content: '确定删除?',
        ok: function() {
            console.log(this)
            // do something
        },
        cancelValue: '取消',
        cancel: function() {
            console.log(this)
            // do something
        },
        onshow: function() {
            console.log(this)
            // do something
        }
    });
    d.show();
  });
  
});
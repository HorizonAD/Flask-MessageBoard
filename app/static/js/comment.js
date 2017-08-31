//默认加载时id=-1
window.onload = function(){
    $('#follow').val(-1);
}
//撤销回复时
function undo_reply() {
    $('#follow').val(-1);
}
//回复函数
function go_to_reply(id, author) {
    $('html, body').animate({scrollTop:$('#submit-comment').offset().top}, 800);
    //回滚到评论框
    $('#follow').val(id);
    //重新赋给id
    $("#submit-comment").prepend(
    	'<div class="alert alert-info alert-dismissable" id="reply-dialog-box">' +
        '<button type="button" class="close" data-dismiss="alert" onclick="undo_reply()">&times;</button>' +
        '回复给<strong><i>' + author +'</i></strong> </div>');
    //在id=submit-comment前面加
}
//搜索跳转函数
function return_post(url) {
    window.location.href=url;
}
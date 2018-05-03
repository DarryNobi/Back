
var data=[];
for(var i in d_users){

data.push(d_users[i])

}

window.onload=function(){
    //默认获取当前日期
    showList();
};
function showList(){

    var resultTab = $("#resultTab");
    var pubText="";
//    data.forEach(function(item){
//     if(item.is_active)
//          pubText="正常";
//        else
//          pubText="禁用"
//        $(
//            '<tr/>', {
//                'style' : 'font-size:18px'
//            }).append($('<td/>', {
//                text : item.id
//            }))
//            .append($('<td/>',{
//                text : item.username
//            }))
//            .append($('<td/>',{
//                text : item.enterprise_name
//            }))
//            .append($('<td/>',{
//                text : item.phone
//            }))
//            .append($('<td/>',{
//                text : item.contact_usr
//            }))
//            .append($('<td/>',{
//                text : item.usr_type
//            }))
//            .append($('<td/>',{
//                text : pubText
//            }))
//             .append($('<td/>',{
//                text : item.user_permissions
//            }))
//            .append($('<td/>')
//            .append($('<p/>')
//            .append($('<button/>',{
//                'class' : 'operate',
//                'id' : 'modify' + item.id,
//                text : '修改'
//            }))
//            ))
//            .appendTo(resultTab);
//
//        button_modify=$("#modify"+ item.id);
//        button_modify.on("click",{"username":item.username},modify_information);
//    });
      resultTab.bootstrapTable({
          locale:'zh-CN',//中文支持
          pagination: true,//是否开启分页（*）
          pageNumber:1,//初始化加载第一页，默认第一页
          pageSize: 3,//每页的记录行数（*）
          pageList: [10, 25, 50, 100],//可供选择的每页的行数（*）
          sidePagination: "client", //分页方式：client客户端分页，server服务端分页（*）
          showRefresh:true,//刷新按钮
          search: true,
          columns: [
              {field: 'id'},
              {field: 'username'},
              {field: 'enterprise_name'},
          ],
          data:data,
      })
};
function modify_information(data)
{
var username=data.data.username;
location.href="/info_revise/?txt="+username;//发送txt里面的内容
}


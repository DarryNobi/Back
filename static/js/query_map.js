
var data=[];
for(var i in d_maps){

data.push(d_maps[i])

}

window.onload=function(){
    //默认获取当前日期
    showList();
};

function showList(){

    var resultTab = $("#resultTab");
    var pubText="";
    data.forEach(function(item){
        $(
        '<tr/>', {
            'style' : 'font-size:18px'
        }).append($('<td/>', {
            text : item.id
        }))
        .append($('<td/>',{
            text : item.map_name
        }))
        .append($('<td/>',{
            text : item.create_time
        }))
        .append($('<td/>',{
            text : item.satelite
        }))
        .append($('<td/>',{
            text : item.desc
        }))
        .append($('<td/>',{
            text : item.download_times
        }))
        .append($('<td/>')
        .append($('<p/>')
        .append($('<button/>',{
            'class' : 'operate',
            'id' : 'delete' + item.id,
            text : '删除'
        }))
        ))
        .appendTo(resultTab);

        button=$("#delete"+ item.id);
        button.on("click",{"num":item.id},changeStatus);
    });
};

function changeStatus(data){
    num=data.data.num
    $.ajax({
      url: '/_delete_map/',
      data: {id:num},
      success: location.reload()
    });
}
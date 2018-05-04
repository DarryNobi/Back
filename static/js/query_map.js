
var data=[];
for(var i in d_maps){

data.push(d_maps[i])

}

window.onload=function(){
    //默认获取当前日期
    showList();
};

var resultTab = $("#resultTab");

function showList(){

      $("#resultTab").bootstrapTable({
              locale:'zh-CN',//中文支持
              pagination: true,//是否开启分页（*）
              pageNumber:1,//初始化加载第一页，默认第一页
              pageSize: 3,//每页的记录行数（*）
              pageList: [10, 25, 50, 100],//可供选择的每页的行数（*）
              sidePagination: "client", //分页方式：client客户端分页，server服务端分页（*）
              showRefresh:true,//刷新按钮
              search: true,
              data:data,
              columns: [
                  {field: 'id', title:'序号', width:'10%', align:'center'},
                  {field: 'map_name', title:'名称', width:'10%', align:'center'},
                  {field: 'create_time', title:'入库时间', width:'15%', align:'center'},
                  {field: 'satelite', title:'卫星类别', width:'10%', align:'center'},
                  {field: 'desc', title:'地图描述', width:'20%', align:'center'},
                  {field: 'download_times', title:'下载次数', width:'10%', align:'center'},
                  {field: 'tool',title: '操作', align: 'center',
                          formatter: function (value,row,index){
                              var data = row;
                              var element = "<button class='operate' id='delete"+row.id +"' data-id='"+row.id +"' onclick='changeStatus(\" "+row.id+" \")'>删除</button>";
                              return element;
                          },
                  }
              ],

          })
      };

function changeStatus(data){
    $.ajax({
      url: '/_delete_map/',
      data: {id:data},
      success: function () {
          resultTab.bootstrapTable('remove',
          {
              field: 'id',
              values: [parseInt(data)],
          })
      }
    });
}


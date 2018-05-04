
var data=[];
for(var i in d_modules){

data.push(d_modules[i])

}

window.onload=function(){
    //默认获取当前日期
    showList();
};

var module_tab = $("#module_tab");

function showList(){

      $("#module_tab").bootstrapTable({
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
                  {field: 'id', title:'序号', width:'8%', align:'center'},
                  {field: 'module_name', title:'模块名称', width:'8%', align:'center'},
                  {field: 'image', title:'图标', width:'8%', align:'center'},
                  {field: 'purpose', title:'用途', width:'15%', align:'center'},
                  {field: 'create_time', title:'创建时间', width:'15%', align:'center'},
                  {field: 'modify_time', title:'修改时间', width:'15%', align:'center'},
                  {field: 'tool', title:'状态', width:'8%', align:'center',
                      formatter:function(value,row,index){
                              var pubText='';
                              if (row.is_active) {
                                  pubText='正常';
                              } else {
                                  pubText='禁用';
                              }
                              return pubText;
                          }
                  },
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
        url: '/_delete_module/',
        data: {id:data},
        success: function () {
            module_tab.bootstrapTable('remove',{
                field: 'id',
                values: [parseInt(data)],
            })
        }
    });
}


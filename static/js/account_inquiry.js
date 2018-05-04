
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
					  {field: 'id', title:'序号', width:'8%', align:'center'},
					  {field: 'username', title:'用户名', width:'8%', align:'center'},
					  {field: 'enterprise_name', title:'单位名称', width:'8%', align:'center'},
					  {field: 'phone', title:'联系电话', width:'10%', align:'center'},
					  {field: 'contact_usr', title:'联系人', width:'8%', align:'center'},
					  {field: 'usr_type', title:'用户类型', width:'8%', align:'center'},
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
					  {field: 'user_permissions', title:'权限', width:'30%', align:'center'},
					  {field: 'tool',title: '操作', align: 'center',
						  	  formatter: function (value,row,index){
						  	  	  var data = row;
						  	      var element = "<button class='operate' id='modify"+row.id +"' data-id='"+row.id +"' onclick='modify_information(\" "+row.username+" \")'>修改</button>";
								  return element;
						  	  },
					  }
				  ],

			  })
		};
function modify_information(data){
    location.href="/info_revise/?txt="+data;//发送txt里面的内容
}


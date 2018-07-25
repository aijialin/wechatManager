function updateUsersState() {
    $.ajax({
        type: "GET",
        url: URL + "itchatGo_updateUsersState.request",
        //data: $.cookie('userName'),
        datatype: "json",
        success: function(retData) {
            var ret = JSON.parse(retData);
        	updataUserInfoBatch(ret)
            
            console.log(ret);
        }
    });
}

function updataUserInfoBatch(userKeyArray) {
    $.ajax({
        type: "POST",
        url: URL + "itchatGo_checkUserInfoBatch.request",
        data: JSON.stringify(userKeyArray),
        datatype: "json",
        success: function(retData) {
            var ret = JSON.parse(retData);
            if (UPDATEUSERSTABLELOCK) {
            	UPDATEUSERSTABLELOCK = false
            	updateUsersTable(ret)
            }
            // console.log(ret);
        }
    });
}

function isSameArray(arr1, arr2) {
	if (arr1.length == arr2.length) {
		var i = arr1.length;
		while (i--) {
			if (arr1[i] === arr2[i]) {
			 	continue;
			} else {
				return false;
			}
		}
		return true
	} else {
		return false;
	}
}
function getUserReplySwich(userName) {
    $.ajax({
        type: "POST",
        url: URL + "itchatGo_getUserAutoReplySwitch.request",
        data: userName,
        datatype: "json",
        success: function(retData) {
            var ret = JSON.parse(retData);
            if (ret.msg == "open") {
                REPLYSWITCH = true;
            } else {
                REPLYSWITCH = false;
            }
            
        }  
    });
   return REPLYSWITCH;
}
function updateUsersTable(usersInfoObject) {
	// console.log(usersInfoObject);
	var usersarray = [];
    var thead =
        '<thead><tr>' +
        '<td>昵称</td>' +
        '<td>微信好友</td>' +
        '<td>收到消息(条)</td>' +
        '<td>发出消息(条)</td>' +
        '<td>添加好友(个)</td>' +
        '<td>登录时间</td>' +
        '<td>自动回复</td>' +
        '</tr></thead><tbody>';
    var end = "</tbody>";
    
    for (var i in usersInfoObject) {
    	var nickName = (usersInfoObject[i]["nickName"] == undefined) ? "正在登陆" : usersInfoObject[i]["nickName"];
    	var friendsCount = (usersInfoObject[i]["friendsCount"] == undefined) ? "0" : usersInfoObject[i]["friendsCount"];
    	var recMsgCount = (usersInfoObject[i]["recMsgCount"] == undefined) ? "0" : usersInfoObject[i]["recMsgCount"];
    	var sendMsgCount = (usersInfoObject[i]["sendMsgCount"] == undefined) ? "0" : usersInfoObject[i]["sendMsgCount"];
    	var addFriendsCount = (usersInfoObject[i]["addFriendsCount"] == undefined) ? "0" : usersInfoObject[i]["addFriendsCount"];
    	var isAutoReply = (getUserReplySwich(nickName) == false) ? "否" : "是";
        var row = '<tr>' +
            '<td>' + nickName + '</td>' +
            '<td>' + friendsCount + '</td>' +
            '<td>' + recMsgCount  + '</td>' +
            '<td>' + sendMsgCount  + '</td>' +
            '<td>' + addFriendsCount  + '</td>' +
            '<td>' + usersInfoObject[i]["createtime"] + '</td>' +
            '<td>' + isAutoReply + '</td>' +
            '</tr>';
        usersarray.push(row);
    }

    var Count = usersarray.length; //记录条数  
    var PageSize = 10; //设置每页示数目  
    var PageCount = Math.ceil(Count / PageSize); //计算总页数  
    var currentPage = 1; //当前页，默认为1

    //构造分页 <li><a href="#">1</a></li>
    $('#fenye').html('');
    var fenye_head = '<li><a href = "#addFriendsTable" aria - label = "Previous" ><span aria-hidden = "true" >&laquo;</span></a></li>';
    var fenye_end = '<li><a href = "#addFriendsTable" aria - label = "Next" ><span aria-hidden = "true" >&raquo;</span></a></li>';

    $('#fenye').append(fenye_head);
    for (var i = 1; i <= PageCount; i++) {
        var pageN = '<li><a class="fenye_a" href="#addFriendsTable" selectPage="' + i + '" >' + i + '</a></li>';
        $('#fenye').append(pageN);
    }
    $('#fenye').append(fenye_end);

    //显示默认页（第一页）  
    $('#usersInfoTable').empty().append(thead);
    for (i = (currentPage - 1) * PageSize; i < PageSize * currentPage; i++) {
        $('#usersInfoTable').append(usersarray[i]);
    }
    $('#usersInfoTable').append(end);
    

    //显示选择页的内容  
    $('.fenye_a').click(function() {
        var selectPage = $(this).attr('selectPage');
        $('#usersInfoTable').html('');
        $('#usersInfoTable').append(thead);
        for (i = (selectPage - 1) * PageSize; i < PageSize * selectPage; i++) {
            $('#usersInfoTable').append(usersarray[i]);
        }
        $('#usersInfoTable').append(end);
    });
    UPDATEUSERSTABLELOCK = true //解锁
}

var URL = "http://weixin.aijialin.cn/";

var UPDATEUSERSTABLELOCK = true;
var REPLYSWITCH = false;
$(function() {
    updateUsersState();
    var interval = setInterval("updateUsersState()", 2000);
});
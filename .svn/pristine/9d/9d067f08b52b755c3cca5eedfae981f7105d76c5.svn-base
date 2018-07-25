document.write("<script src='html/js/jquery.cookie.js'></script>");

$("button[type='button']").click(function(){
    if ($(this).html() == "点击修改") {
        $(this).prev().removeAttr("disabled");
        $(this).html("确定修改");
        $(this).css({ backgroundColor: "green" });
        return;
    }
    if ($(this).html() == "确定修改") {
        $(this).prev().attr("disabled", "disabled");
        $(this).html("点击修改");
        $(this).css({ backgroundColor: "#f0ad4e" });
        var content = $(this).prev().val();
        changeUserConfig(this.id, content);
        return;
    }
});

$("input[type='checkbox']").change(function() {
    if (this.checked) {
        changeUserConfig(this.id, true)
    } else {
        changeUserConfig(this.id, false)
    }
});

$("input[type='radio']").change(function() {
    toUser = ""
    if (this.checked) {
        if (this.value == "myself") {
            toUser = $.cookie("userName")
        } else if (this.value == "himself"){
            toUser = ""
        } else toUser = this.value
        changeUserConfig(this.name, toUser)
    }
});



/**/
function changeUserConfig(key, content) {
    transdata = {}
    transdata[key] = content
    transdata["nickName"] = $.cookie('nickName')
    transdata = JSON.stringify(transdata)
    console.log(transdata)
    $.ajax({
        type: "POST",
        url: $.cookie('URL') + "wechat_changeUserConfig.request",
        data: transdata,
        datatype: "json",
        success: function(retData) {
            var ret = JSON.parse(retData);
            console.log(ret);
            getUserConfig()
        }
    });
}

function praseIntroduce(introduce) {
    introduceArray = introduce.split("|");
    introduceJson = JSON.stringify(introduceArray);
    return introduceJson;
}

function clearCookie(){ 
    for (key in $.cookie()) {
        console.log(key, $.cookie(key));
        $.removeCookie(key);
    }
    /*
    var keys=document.cookie.match(/[^ =;]+(?=\=)/g); 
    if (keys) { 
        for (var i = keys.length; i--;) 
        document.cookie = keys[i] + '=0;expires=' + new Date(0).toUTCString() 
    }
    */
} 


function getUserConfig() {
    $.ajax({
        type: "POST",
        url: $.cookie('URL') + "wechat_getUserConfig.request",
        data: $.cookie('nickName'),
        datatype: "json",
        success: function(retData) {
            var ret = JSON.parse(retData);
            if ($.cookie('userName') == undefined) $.cookie('userName', ret.userName)
            $("#textareaBusyContent").html(ret.busyContent);
            $("#textareaVerifyContent").html(ret.verifyContent);
            $("#friendsCount").html(ret.friendsCount)
            $("#recMsgCount").html(ret.recMsgCount)
            $("#sendMsgCount").html(ret.sendMsgCount)
            $("#newFriendsCount").html(ret.newFriendsCount)
            $("#loginTime").html(ret.loginTime);

            if (ret.jokeSwitch) {
                $("#joke_reply").html("<span style='color:green;'>自动闲聊已开启</span>");
            } else {
                $("#joke_reply").html("<span style='color:red;'>自动闲聊已关闭</span>");
                document.getElementById('jokeSwitch').checked = false;
            }
            if (ret.busySwitch) {
                $("#busy_reply").html("<span style='color:green;'>忙碌状态已开启</span>");
            } else {
                $("#busy_reply").html("<span style='color:red;'>忙碌状态已关闭</span>");
                document.getElementById('busySwitch').checked = false;
            }
            if (ret.banRevokeSwitch) {
                $("#ban_revoke").html("<span style='color:green;'>禁止撤回消息已开启</span>");
            } else {
                $("#ban_revoke").html("<span style='color:red;'>禁止撤回消息已关闭</span>");
                document.getElementById('banRevokeSwitch').checked = false;
            }
            if (ret.verifySwitch) {
                $("#auto_verify").html("<span style='color:green;'>自动验证好友请求已开启</span>");
            } else {
                $("#auto_verify").html("<span style='color:red;'>自动验证好友请求已关闭</span>");
                document.getElementById('verifySwitch').checked = false;
            }
            if (ret.revokeMsgToUser == "") {
                $("#himself").attr("checked","checked")
            } else if (ret.revokeMsgToUser == "filehelper") {
                $("#filehelper").attr("checked","checked")
            } else $("#myself").attr("checked","checked")
            
            if (ret.loginStatus == "exited") {
                clearCookie()
                alert("用户已退出, 请重新登陆")
                location.replace("/");
            }
            console.log(ret);
        }
    });
}

interval = null
function initUserInfo() {
    var nickName = $.cookie('nickName');
    $("#nickName").html(nickName);
    getUserConfig();
    interval = setInterval("getUserConfig()", 2000);
}


$(function() {
    initUserInfo();
});

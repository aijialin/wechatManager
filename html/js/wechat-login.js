document.write("<script src='html/js/jquery.cookie.js'></script>");

var URL = document.URL;
var userKey = '';
var interval = null;

$("button[type='submit']").click(function() {
    //让按钮禁止
    $("button[type='submit']").attr("disabled","disabled");
    $.ajax({
        type: "POST",
        url: URL + "wechat_start.request",
        success: function(retData) { //".attr("src");
            var ret = JSON.parse(retData);
            console.log(ret);
            if (ret.ret == 0) {
                //$('#qrcode').attr({ src: ret.qrcode });
                $('#loginStatus').html(ret.loginStatus);
                userKey = ret.userKey;
                interval = setInterval("updataLoginState()", 200);
            } else {
                $('#loginStatus').html(ret.msg);
            }
            
            
        }
    });
});

function getToday() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    if (month < 10) {
        month = "0" + month;
    }
    if (day < 10) {
        day = "0" + day;
    }
    loginDate = year + "-" + month + "-" + day;
    return loginDate;
}
//successfully
function updataLoginState() {
    $.ajax({
        type: "POST",
        url: URL + "wechat_checkStatus.request",
        data: userKey,
        datatype: "json",
        success: function(retData) {
            var ret = JSON.parse(retData);
            console.log(ret);
            $('#loginStatus').html(ret.loginStatus);
            if (ret.loginStatus.indexOf('scan') != -1) {
                if ($('#qrcode').attr("src") != ret.qrcode) {
                    $('#qrcode').attr({ src: ret.qrcode });
                }
                return
            }
            if (ret.loginStatus.indexOf('confirm') != -1) {
                if ($('#qrcode').attr("src") != ret.headImg) {
                    $('#qrcode').attr({ src: ret.headImg });
                }
                return
            }
            if (ret.loginStatus.indexOf('successfully') != -1) {
                var s = ret.loginStatus.indexOf('as');
                var nickName = ret.loginStatus.substr(s+3);
                var loginData = getToday();
                $.cookie('nickName', nickName);
                $.cookie('userKey', userKey);
                $.cookie('loginDate', loginData);
                $.cookie('URL', URL);
                clearInterval(interval);
                $('#loginStatus').html("登录成功, 正在跳转管理界面...");
                location.replace("index.html");
                return
            }
            if (ret.loginStatus.indexOf('time out') != -1) {
                $('#qrcode').attr({ src: ret.qrcode });
                return
            } 
            if (ret.loginStatus.indexOf('refresh') != -1) {
                clearInterval(interval);
                $('#qrcode').attr({src: "html/img/reload.jpg"});
                $("button[type='submit']").removeAttr("disabled");
                return
            } 
            
        }
    });
}


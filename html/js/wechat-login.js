document.write("<script src='html/js/jquery.cookie.js'></script>");

var URL = document.URL;
var userKey = '';
var interval = null;
var loginCode = 1
var SENDREQ = true

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
                $('#loginStatus').html("正在生成登陆二维码...");
                userKey = ret.userKey;
                SENDREQ = true
                updataLoginState();
                
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
    if ( !SENDREQ ) return;
    transdata = {}
    transdata["loginCode"] = loginCode
    transdata["userKey"] = userKey
    transdata = JSON.stringify(transdata)
    $.ajax({
        type: "POST",
        url: URL + "wechat_checkStatus.request",
        data: transdata,
        datatype: "json",
        //async:false,
        success: function(retData) {
            var ret = JSON.parse(retData);
            console.log(ret);
            if (ret.loginCode < 0) { //出错后停止请求
                SENDREQ = false;
                loginCode = 1
                $('#qrcode').attr({src: "html/img/reload.jpg"});
                $("button[type='submit']").removeAttr("disabled");
            } else if (ret.loginCode == 1) { //正在生成二维码
                $('#loginStatus').html("正在生成登陆二维码...");
                loginCode = ret.loginCode;
            } else if (ret.loginCode == 2) { //请扫描
                $('#loginStatus').html("请使用手机微信扫码登陆");
                if ($('#qrcode').attr("src") != ret.qrcode) {
                    $('#qrcode').attr({ src: ret.qrcode });
                }
                loginCode = ret.loginCode;
            } else if (ret.loginCode == 3) { //请确认
                $('#loginStatus').html("请在手机微信上点击确认");
                if ($('#qrcode').attr("src") != ret.headImg) {
                    $('#qrcode').attr({ src: ret.headImg });
                }
                loginCode = ret.loginCode;
            } else if (ret.loginCode == 4) { //加载联系人
                $('#loginStatus').html("正在加载联系人, 请稍后");
                loginCode = ret.loginCode;
            } else if (ret.loginCode == 5) { //登陆成功
                $('#loginStatus').html("登陆成功, 正在跳转管理界面");
                var loginData = getToday();
                $.cookie('nickName', ret.nickName);
                $.cookie('userKey', userKey);
                $.cookie('loginDate', loginData);
                $.cookie('URL', URL);
                loginCode = ret.loginCode;
                SENDREQ = false;
                location.replace("index.html");
            } else if (ret.loginCode == 100) { //登陆超时
                $('#loginStatus').html("登陆超时, 正在重试");
                $('#qrcode').attr({ src: ret.qrcode });
                loginCode = ret.loginCode

            } else if (ret.loginCode == 101) { //登陆失败
                $('#loginStatus').html("登陆失败, 请重新获取二维码");
                $('#qrcode').attr({src: "html/img/reload.jpg"});
                $("button[type='submit']").removeAttr("disabled");
                SENDREQ = false
                loginCode = 1
            }
            updataLoginState();
        },
    });
}


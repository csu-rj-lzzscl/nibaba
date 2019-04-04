var xmlHttpRequest;
function createXMLHttpRequest () {
    if(window.XMLHttpRequest)
    {
        xmlHttpRequest=new XMLHttpRequest();
    }
    else if(window.ActiveXObject)
    {
        xmlHttpRequest=new ActiveXObject("Msxml2.XMLHTTP");
    }
    else
    {
        xmlHttpRequest=new ActiveXObject("Microsoft.XMLHTTP");
    }
}

function usernameIsExist() {
    var username=document.registerForm.username.value;
    if(username.trim()!="")
    {
        sendRequest("usernameIsExist?username="+username);
    }
}

function sendRequest(url) {
    createXMLHttpRequest();
    xmlHttpRequest.open("GET",url,true);
    xmlHttpRequest.onreadystatechange=processResponse;
    xmlHttpRequest.send(null);
}

function processResponse() {
    if (xmlHttpRequest.readyState == 4) {
        if (xmlHttpRequest.status == 200) {
            var responseInfo = xmlHttpRequest.responseXML.getElementsByTagName("msg")[0].firstChild.data;

            var div1 = document.getElementById("usernameMsg");
            if (responseInfo == "Exist") {
                div1.innerHTML = "<font color='red'>This username has been used!</font>";
            }
            else {
                div1.innerHTML = "<font color='green'>This username can be used</font>";
            }
        }
    }
}

function passwordIsValid() {
    var pass=document.registerForm.password.value;

    var div =document.getElementById("passwordMsg");

    if(pass.trim().length>0&&pass.trim().length<6)
    {
        div.innerHTML="<font color='red'>密码强度太低</font>";
        return false;
    }
    else if(pass.trim().length>=6) {
        div.innerHTML = "<font color='green'>密码可以使用</font>";
        return true;
    }
}

function passwordIsSame(){
    var pass1=document.registerForm.password.value;
    var pass2=document.registerForm.repeatedPassword.value;

    var div=document.getElementById("repeatedPasswordMsg");

    if(pass1!=pass2&&pass2.trim().length>0){
        div.innerHTML="<font color='red'>两次密码输入不一致</font>";
        return false;
    }
    else if(pass1==pass2&&pass1.trim().length>0)
    {
        div.innerHTML="<font color='green'>√</font>";
        return true;
    }
}

function emailIsValid(){
    var email=document.registerForm.email.value;
    console.log(email);
    var div=document.getElementById("emailMsg");

    if(email.trim().length>0) {
        var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
        var isok= reg.test(email);
        if(!isok) {
            div.innerHTML="<font color='red'>邮箱格式错误</font>";
            return false;
        }
        else
        {
            div.innerHTML="<font color='green'>邮箱可以使用</font>";
            return true;
        }
    }
}

function checkAllRegisterForm()
{
    var username=document.registerForm.username.value;
    var pass1=document.registerForm.password.value;
    var pass2=document.registerForm.repeatedPassword.value;
    var email=document.registerForm.email.value;

    var div=document.getElementById("usernameMsg").innerText;

    if(username.trim().length==0||pass1.trim().length==0||pass2.trim().length==0||email.trim().length==0)
    {
        alert("Please fill in the information.");
        return false;
    }
    else if(div=="This username has been used!"||!passwordIsValid()||!passwordIsSame()||!emailIsValid())
    {
        alert("Please fill in the correct information.")
        return false;
    }
    else
        return true;
}


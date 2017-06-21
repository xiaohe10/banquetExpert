window.Login = {token: "null"};
//
// var LoginApp = angular.module('LoginApp', []);
// LoginApp.controller('LoginCtrl', function ($scope, $http) {
//     $scope.option = {
//         username: "beijingyan",
//         password: "beijingyan"
//     };
//     $scope.login = function () {
//         var data = {
//             username: $scope.option.username,
//             password: hex_md5($scope.option.password)
//         };
//         alert(JSON.stringify(data));
//         var url = "/webApp/admin/login/";
//         $http.post(url, data).success(function (data) {
//             var obj = eval(data);
//             if (obj.status === "true") {
//                 window.Login.token = obj.data.token;
//                 location.href = "index.html";
//             } else {
//                 alert("登录失败");
//             }
//         })
//     }
// });

$("#login").click(function () {
    var username, password;
    username = $("#username").val();
    password = $('#password').val();
    password = hex_md5(password);
    $.ajax({
        url: "/webApp/admin/login/",
        method: "POST",
        data: {
            username: username,
            password: password
        },
        success: function (data, status) {
            var obj = eval(data);
            alert(JSON.stringify(data));
            if (obj.status === "true") {
                window.Login.token = obj.data.token;
                location.href = "index.html";
            } else {
                alert("登录失败：" + password);
            }
        },
        fail: function (message) {
            alert("登录失败:" + message)
        }
    });
});
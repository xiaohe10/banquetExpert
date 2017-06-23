window.Login = {token: "null"};

var LoginApp = angular.module('LoginApp', []);
LoginApp.controller('LoginCtrl', function ($scope, $http) {
    $scope.option = {
        username: "beijingyan",
        password: "beijingyan"
    };
    $scope.login = function () {
        var data = {
            username: $scope.option.username,
            password: hex_md5($scope.option.password)
        };
        var url = "/webApp/admin/login/";
        $http.post(url, JSON.stringify(data)).success(function (data) {
            var obj = eval(data);
            if (obj.status === "true") {
                window.Login.token = obj.data.token;
                location.href = "index.html";
            } else {
                alert("登录失败");
            }
        })
    }
});
var LoginApp = angular.module('LoginApp', []);
LoginApp.controller('LoginCtrl', function ($scope, $http) {
    $scope.form = {
        username: "admin",
        password: "admin",
        option_selected: "超级管理员"
    };
    $scope.groups = {
        "超级管理员": "/webApp/super_admin/login/",
        "管理员": "/webApp/admin/login/",
        "员工": "/webApp/staff/login/"
    };
    $scope.hrefs = {
        "超级管理员": "admin.html",
        "管理员": "admin.html",
        "员工": "staff.html"
    };
    $scope.login = function () {
        var data = {
            username: $scope.form.username,
            password: hex_md5($scope.form.password)
        };
        var key = $scope.form.option_selected;
        $http.post($scope.groups[key], JSON.stringify(data)).success(function (data) {
            var obj = eval(data);
            if (obj.status === "true") {
                location.href = $scope.hrefs[key];
            } else {
                alert("登录失败");
            }
        });
    }
});
var LoginApp = angular.module('LoginApp', []);
LoginApp.controller('LoginCtrl', function ($scope, $http) {

    // 用户组
    $scope.groups = [
        {
            name: "超级管理员",
            url: "/webApp/super_admin/login/",
            href: "admin.html"
        },
        {
            name: "管理员",
            url: "/webApp/admin/login/",
            href: "manager.html"
        },
        {
            name: "员工",
            url: "/webApp/staff/login/",
            href: "staff.html"
        }
    ];

    // 登录表单
    $scope.form = {
        username: "admin",
        password: "admin",
        group_id: 0
    };

    // 登录账号
    $scope.login = function () {
        var param = {
            username: $scope.form.username,
            password: hex_md5($scope.form.password)
        };
        var group_id = $scope.form.group_id;
        var group = $scope.groups[group_id];
        $http.post(group.url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                location.href = group.href;
            } else {
                alert("登录失败：" + obj.description);
            }
        });
    }
});
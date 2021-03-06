/**
 * Created by 本山 on 2017/7/6.
 */
// 子页面模板
Templates = {
    // 路径导航
    Breadcrumb: "Drawer/Breadcrumb.html",
    // 超级管理后台
    SuperAdmin: {
        HotelAdmin: "SuperAdmin/HotelAdmin.html", // 酒店列表
        ManagerAdmin: "SuperAdmin/ManagerAdmin.html" // 管理员列表
    }
};

// 对话框模板
Dialog = {
    SuperAdmin: {
        HotelAdmin: {
            HotelDialog: "SuperAdmin/HotelAdmin/HotelDialog.html"
        },
        ManagerAdmin: {
            ManagerDialog: "SuperAdmin/ManagerAdmin/ManagerDialog.html"
        }
    }
};

// 自定义日志工具
var Log = {
    i: function (tag, msg) {
        console.log("BanquetExpert: " + tag + ": " + msg);
    },
    w: function (tag, msg) {
        console.warn("BanquetExpert: " + tag + ": " + msg);
    },
    e: function (tag, msg) {
        console.error("BanquetExpert: " + tag + ": " + msg);
    },
    d: function (tag, msg) {
        console.debug("BanquetExpert: " + tag + ": " + msg);
    }
};

var AdminApp = angular.module('AdminApp', [
    'ngRoute',
    'ui.bootstrap'
]);

AdminApp.filter("admin_type", function () {
    return function (admin_type) {
        var TAG = ["管理员", "超级管理员"];
        return TAG[admin_type];
    }
});

// 侧边导航栏控制器
AdminApp.controller('drawerCtrl', function ($rootScope, $scope, $http) {

    var TAG = 'drawerCtrl';

    // 侧边栏
    $scope.menus = [
        {
            title: "超级管理后台",
            menu_id: "SuperAdmin",
            item: [
                {title: "酒店管理", item_id: "HotelAdmin"},
                {title: "管理员", item_id: "ManagerAdmin"}
            ]
        }
    ];
    // 路径导航
    $scope.Breadcrumb = [
        {title: "主页"},
        {title: "超级管理后台"},
        {title: "酒店管理"}
    ];
});

// Angular路由配置
AdminApp.config(['$routeProvider', function ($routeProvider) {

    // 超级管理员
    $routeProvider
        .when('/SuperAdmin/HotelAdmin', {
            templateUrl: "./template/" + Templates.SuperAdmin.HotelAdmin, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.SuperAdmin.HotelAdmin;
                // 酒店列表
                $scope.data = {count: 0, list: []};
                // 【超级管理员】获取酒店列表
                var url = "/webApp/super_admin/hotel/list/";
                var param = {};
                $http.post(url, JSON.stringify(param)).success(function (obj) {
                    if (obj.status === "true") {
                        $scope.data = obj.data;
                    } else {
                        alert(obj.description);
                    }
                });
                // 添加酒店
                $scope.addHotel = function () {
                    Log.i(TAG, "添加酒店");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.SuperAdmin.HotelAdmin.HotelDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.SuperAdmin.HotelAdmin.HotelDialog;
                            Log.i(TAG, "添加酒店");
                            $scope.option = "添加";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑酒店信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存酒店信息");
                                dlg.close(form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消");
                                dlg.dismiss();
                            }
                        },
                        resolve: {
                            form: function () {
                                return {
                                    name: "珍珠大酒店",
                                    owner_name: "赵强"
                                };
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/super_admin/hotel/register/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("添加酒店成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                // 编辑酒店信息
                $scope.editHotel = function (hotel) {
                    Log.i(TAG, "编辑酒店：" + hotel.name);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.SuperAdmin.HotelAdmin.HotelDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.SuperAdmin.HotelAdmin.HotelDialog;
                            Log.i(TAG, "编辑酒店控制器");
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑酒店信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存酒店信息");
                                dlg.close(form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消");
                            }
                        },
                        resolve: {
                            form: function () {
                                if (hotel.positions === "") {
                                    hotel.positions = [];
                                }
                                return hotel;
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/super_admin/hotel/modify/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("添加酒店成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                }
            }
        })
        .when('/SuperAdmin/ManagerAdmin', {
            templateUrl: "./template/" + Templates.SuperAdmin.ManagerAdmin, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.SuperAdmin.ManagerAdmin;
                // 管理员列表
                $scope.data = {count: 0, list: []};
                // 【超级管理员】获取管理员列表
                var url = "/webApp/super_admin/manager/list/";
                var param = {};
                $http.post(url, JSON.stringify(param)).success(function (obj) {
                    if (obj.status === "true") {
                        $scope.data = obj.data;
                    } else {
                        alert(obj.description);
                    }
                });
                // 添加管理员
                $scope.addManager = function () {
                    Log.i(TAG, "添加管理员");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.SuperAdmin.ManagerAdmin.ManagerDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.SuperAdmin.ManagerAdmin.ManagerDialog;
                            Log.i(TAG, "添加管理员");
                            $scope.option = "添加";
                            $scope.form = form;
                            // 【超级管理员】获取酒店列表
                            var url = "/webApp/super_admin/hotel/list/";
                            var param = {};
                            $http.post(url, JSON.stringify(param)).success(function (obj) {
                                if (obj.status === "true") {
                                    $scope.HotelList = obj.data;
                                } else {
                                    alert(obj.description);
                                    $scope.HotelList = {count: 0, list: []};
                                }
                            });
                            $scope.edit = function () {
                                Log.i(TAG, "编辑管理员信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存管理员信息");
                                dlg.close(form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消");
                                dlg.dismiss();
                            }
                        },
                        resolve: {
                            form: function () {
                                return {
                                    username: "17701092671",
                                    password: "123456",
                                    hotel_id: 0,
                                    type: 0
                                };
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/super_admin/manager/register/";
                        var param = angular.copy(result);
                        param.password = hex_md5(param.password);
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("注册管理员成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                // 编辑管理员信息
                $scope.editManager = function (manager) {
                    Log.i(TAG, "编辑管理员：" + manager.name);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.SuperAdmin.ManagerAdmin.ManagerDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.SuperAdmin.ManagerAdmin.ManagerDialog;
                            Log.i(TAG, "编辑管理员控制器");
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑管理员信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存管理员信息");
                                dlg.close(form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消");
                            }
                        },
                        resolve: {
                            form: function () {
                                manager.ack_password = "";
                                return manager;
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/super_admin/manager/modify/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("修改管理员成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                }
            }
        })
        .otherwise({redirectTo: "/SuperAdmin/HotelAdmin"});
}]);
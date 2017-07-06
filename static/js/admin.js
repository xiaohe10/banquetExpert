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

var BanquetExpertApp = angular.module('BanquetExpertApp', [
    'ngRoute',
    'ui.bootstrap'
]);

// 侧边导航栏控制器
BanquetExpertApp.controller('drawerCtrl', function ($rootScope, $scope, $http) {

    var TAG = 'drawerCtrl';

    // 获取酒店列表
    $rootScope.HotelList = [];
    // 获取管理员列表
    $rootScope.Managerlist = [];
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
        {title: "预订管理"},
        {title: "餐段设置"}
    ];

    // 【超级管理员】获取酒店列表
    var url = "/webApp/super_admin/hotel/list/";
    var param = {};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.HotelList = obj.data;
        } else {
            alert(obj.description);
        }
    });

    // 【超级管理员】获取管理员列表
    url = "/webApp/super_admin/manager/list/";
    param = {};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.Managerlist = obj.data;
        } else {
            alert(obj.description);
        }
    });
});


// Angular路由配置
BanquetExpertApp.config(['$routeProvider', function ($routeProvider) {

    // 超级管理员
    $routeProvider
        .when('/SuperAdmin/HotelAdmin', {
            templateUrl: "./template/" + Templates.SuperAdmin.HotelAdmin, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.SuperAdmin.HotelAdmin;
                // 酒店列表
                $scope.data = $rootScope.HotelList;
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
                                var hotel = {
                                    name: "珍珠大酒店",
                                    owner_name: "赵强"
                                };
                                return hotel;
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
                                return hotel;
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                }
                // ,
                //     service: {
                //         "customer_analysis": true,
                //         "order_statistics": true
                //     }
            }
        })
        .when('/SuperAdmin/ManagerAdmin', {
            templateUrl: "./template/" + Templates.SuperAdmin.ManagerAdmin, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.SuperAdmin.ManagerAdmin;
                // 管理员列表
                $scope.data = $rootScope.Managerlist;
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
                                    name: "珍珠大管理员",
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
                        var url = "/webApp/super_admin/register/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
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
                        var url = "/webApp/super_admin/modify/";
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
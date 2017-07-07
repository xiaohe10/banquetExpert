/**
 * Created by 本山 on 2017/7/6.
 */

// 子页面模板
Templates = {
    // 路径导航
    Breadcrumb: "Drawer/Breadcrumb.html",
    // 预定管理
    Reserve: {
        Reserve: "/Reserve/Reserve.html", // 预订管理
        AreaDesk: "Reserve/AreaDesk.html", // 桌位设置
        MealsTime: "Reserve/MealsTime.html", // 餐段管理
        MealsArea: "Reserve/MealsArea.html", // 餐位设置
        DeskRecommend: "Reserve/DeskRecommend.html",// 自动推荐桌位
        PersonalTailor: "Reserve/PersonalTailor.html"// 私人订制
    }
};

// 对话框模板
Dialog = {
    Reserve: {
        AreaDesk: {
            DeskDialog: "Reserve/AreaDesk/DeskDialog.html"
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

var BranchApp = angular.module('BranchApp', [
    'ngRoute',
    'ui.bootstrap'
]);

BranchApp.service('BranchService', function ($rootScope, $http) {

    // 【门店】获取门店信息
    this.getProfile = function ($scope, branch_id) {
        var url = "/webApp/admin/hotel_branch/profile/get/";
        var param = {branch_id: branch_id};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                $rootScope.$broadcast('branch-profile', obj.data);
            } else {
                alert(obj.description);
                return {};
            }
        });
    };

    // 【门店】获取门店区域列表area/list/";
    this.getAreaList = function ($rootScope, branch_id) {
        var url = "/webApp/admin/hotel_branch/area/list/";
        var param = {branch_id: branch_id};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                $rootScope.$broadcast('branch-area-list', obj.data);
            } else {
                alert(obj.description);
                return {count: '', list: []};
            }
        });
    }
});

// 侧边导航栏控制器
BranchApp.controller('drawerCtrl', function ($routeParams, $rootScope, $location, $scope, $http) {

    var TAG = "drawerCtrl";
    // 获取参数
    $rootScope.branch_id = $routeParams.branch_id;
    Log.i(TAG, $rootScope.branch_id);

    // 门店信息
    $rootScope.branch = {
        branch_id: -1,
        name: "未登录"
    };
    // 餐段列表
    $rootScope.MealsTime = {
        lunch: [
            "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:30", "15:00", "15:30", "16:00"
        ],
        dinner: [
            "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:15",
            "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:30",
            "21:00", "21:30", "21:45", "22:00", "22:30", "23:00", "23:30", "23:45"
        ],
        supper: [
            "22:00", "22:30", "23:00", "23:30", "00:00", "00:30", "01:00", "01:30",
            "02:00", "02:30", "03:00", "03:30", "04:00"
        ]
    };

    $scope.branch = $rootScope.branch;
    // 侧边栏
    $scope.menus = [{
        title: "预订管理",
        menu_id: "Reserve",
        item: [
            {title: "餐段设置", item_id: "MealsTime"},
            {title: "餐位设置", item_id: "MealsArea"},
            {title: "桌位设置", item_id: "AreaDesk"},
            {title: "自动推荐桌位", item_id: "DeskRecommend"},
            {title: "私人订制", item_id: "PersonalTailor"}
        ]
    }];
    // 路径导航
    $scope.Breadcrumb = [
        {title: "主页"},
        {title: "预订管理"},
        {title: "餐段设置"}
    ];
});

// Angular路由配置
BranchApp.config(['$routeProvider', function ($routeProvider) {

    // 【门店】预订管理
    $routeProvider
        .when('/Reserve/Reserve/:branch_id', {
            templateUrl: "./template/" + Templates.Reserve.Reserve, controller: function ($routeParams, $rootScope, $scope, $http) {
                var TAG = Templates.Reserve.Reserve;
                // 获取参数
                $rootScope.branch_id = $routeParams.branch_id;
                Log.i(TAG, $rootScope.branch_id);
                // 初始化门店店信息
                $scope.form = {
                    // 酒店ID
                    hotel_id: -1,
                    // 店长ID
                    staff_id: -1,
                    // 名称
                    name: "未登录",
                    // 省
                    province: "北京市",
                    // 市
                    city: "北京市",
                    // 区/县
                    county: "朝阳区",
                    // 详细地址
                    address: "无",
                    // 电话
                    phone: [],
                    // 设施
                    facility: [],
                    // 支付方式
                    pay_card: [],
                    // 其他可选项
                    icon: "/static/css/image/head.jpg"
                };
                // 初始化员工列表
                $scope.staff = $rootScope.staff;
                // 初始化手机号
                $scope.phone = "";
                // 初始化酒店设施
                $scope.facility = "";
                $scope.facilities = [
                    "万事达(Master)", "可以刷卡", "有停车位", "全场禁烟",
                    "区分烟区", "无线上网", "露天位", "有舞台",
                    "有表演", "下午茶", "夜宵", "四合院"
                ];
                // $scope.facilities.
                // 初始化支付方式
                $scope.pay_card = "";
                $scope.pay_cards = [
                    "支付宝", "微信", "VISA", "银联"
                ];
                // 初始化表单
                $scope.option = "编辑";
                // 【酒店】获取员工列表
                var getStaffList = function (hotel_id) {
                    // 【酒店】获取员工列表
                    var url = "/webApp/admin/hotel/staff/list/";
                    var param = {hotel_id: hotel_id};
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $rootScope.staff = obj.data;
                        } else {
                            alert(obj.description);
                        }
                    });
                };
                // 【门店】获取门店信息
                var getBranchProfile = function (branch_id) {
                    var url = "/webApp/admin/hotel_branch/profile/get/";
                    var param = {branch_id: $rootScope.branch_id};
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $scope.form = obj.data;
                            $rootScope.branch = obj.data;
                            getStaffList($rootScope.branch.hotel_id);
                        } else {
                            alert(obj.description);
                        }
                    });
                };
                // 【门店】保存门店信息
                var postBranchProfile = function (branch) {
                    var url = "/webApp/admin/hotel_branch/profile/modify/";
                    var param = branch;
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            alert("修改门店信息成功");
                        } else {
                            alert(obj.description);
                        }
                    });
                };
                // 获取门店信息
                getBranchProfile($rootScope.branch_id);
                $scope.save = function () {
                    Log.i(TAG, "保存门店信息");
                    postBranchProfile($scope.form);
                };
            }
        })
        .when('/Reserve/AreaDesk', {
            templateUrl: "./template/" + Templates.Reserve.AreaDesk, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Reserve.AreaDesk;
                $scope.area = {count: 0, list: []};
                $scope.desk = {};
                $scope.pages = [1, 2, 3, 4, 5, 6, 7];
                // 【门店】获取门店区域列表area/list/";
                var url = "/webApp/admin/hotel_branch/area/list/";
                var param = {branch_id: $rootScope.branch_id};
                $http.post(url, JSON.stringify(param)).success(function (obj) {
                    if (obj.status === "true") {
                        $scope.area = obj.data;
                    } else {
                        alert(obj.description);
                    }
                });
                // 事件处理
                $scope.addDesk = function () {
                    Log.i(TAG, "添加桌位");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Reserve.AreaDesk.DeskDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Reserve.AreaDesk.DeskDialog;
                            Log.i(TAG, "添加桌位");
                            $scope.option = "添加";
                            $scope.form = form;
                            $scope.type = [
                                '普通包间', '豪华包间', '大厅卡座', '大厅散台',
                                '宴会大厅', '多功能厅', '多桌包间', '隔断', '会场'
                            ];
                            // $scope.facilities = [
                            //     '靠窗', '会客区', '独立卫生间', '小型厨房',
                            //     '卡拉ok', '可棋牌', '海景房', '液晶电视'
                            // ];
                            $scope.edit = function () {
                                Log.i(TAG, "编辑桌位信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存桌位信息");
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
                                    area_id: $scope.area_id,
                                    number: "110",
                                    order: 1,
                                    min_guest_num: 10,
                                    max_guest_num: 15,
                                    expense: [
                                        {name: "最低消费", checked: false, value: 10.0},
                                        {name: "服务费", checked: false, value: 10.0},
                                        {name: "最低人均", checked: false, value: 10.0},
                                        {name: "场地费", checked: false, value: 10.0},
                                        {name: "包间费", checked: false, value: 10.0}
                                    ],
                                    type: 1,
                                    facility: ["电脑", "吸烟区"],
                                    picture: "/static/css/image/head.jpg",
                                    is_beside_window: "True",
                                    description: "赵总的小窝(⊙o⊙)哦"
                                };
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel_branch/desk/add/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("添加桌位成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                $scope.editDesk = function (desk) {
                    Log.i(TAG, "编辑桌位");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Reserve.AreaDesk.DeskDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Reserve.AreaDesk.DeskDialog;
                            Log.i(TAG, "添加桌位");
                            $scope.option = "添加";
                            $scope.form = form;
                            $scope.type = [
                                '普通包间', '豪华包间', '大厅卡座', '大厅散台',
                                '宴会大厅', '多功能厅', '多桌包间', '隔断', '会场'
                            ];
                            // $scope.facilities = [
                            //     '靠窗', '会客区', '独立卫生间', '小型厨房',
                            //     '卡拉ok', '可棋牌', '海景房', '液晶电视'
                            // ];
                            $scope.edit = function () {
                                Log.i(TAG, "编辑桌位信息：" + $scope.form);
                            };
                            $scope.save = function (form) {
                                Log.i(TAG, "保存桌位信息");
                                dlg.close(angular.copy(form));
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消");
                                dlg.dismiss();
                            }
                        },
                        resolve: {
                            form: function () {
                                // if (desk.facility === "") {
                                //     desk.facility = [];
                                // }
                                // if (desk.expense === "") {
                                //     desk.expense = [
                                //         {name: "最低消费", checked: false, value: 10.0},
                                //         {name: "服务费", checked: false, value: 10.0},
                                //         {name: "最低人均", checked: false, value: 10.0},
                                //         {name: "场地费", checked: false, value: 10.0},
                                //         {name: "包间费", checked: false, value: 10.0}
                                //     ];
                                // }
                                return desk;
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel_branch/desk/modify/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("编辑桌位成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                $scope.save = function () {
                    Log.i(TAG, "保存区域桌位信息：" + JSON.stringify($rootScope.area));
                };
                $scope.nav = function (area_id) {
                    Log.i(TAG, "选择区域：" + area_id);
                    var url = "/webApp/admin/hotel_branch/desk/list/";
                    var param = {area_id: area_id};
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $scope.area_id = area_id;
                            $scope.desk = obj.data;
                            $scope.desk.list.forEach(function (obj) {
                                if (obj.facility === "") {
                                    obj.facility = [];
                                }
                                if (obj.expense === "") {
                                    obj.expense = [
                                        {name: "最低消费", checked: false, value: 10.0},
                                        {name: "服务费", checked: false, value: 10.0},
                                        {name: "最低人均", checked: false, value: 10.0},
                                        {name: "场地费", checked: false, value: 10.0},
                                        {name: "包间费", checked: false, value: 10.0}
                                    ];
                                } else {
                                    obj.expense = eval(obj.expense);
                                }
                            });
                        } else {
                            $scope.desk = {};
                        }
                    });
                };
            }
        })
        .when('/Reserve/MealsTime', {
            templateUrl: "./template/" + Templates.Reserve.MealsTime, controller: function ($rootScope, $scope, $http) {
                var TAG = Templates.Reserve.MealsTime;
                $scope.MealsTime = $rootScope.MealsTime;
                $scope.Week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"];
                $scope.EnWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
                $scope.Meals = {hasLunch: false, hasSupper: false, hasDinner: false};
                // 餐段初始化
                if ($rootScope.branch.meal_period.length === 0) {
                    $scope.MealPeriod = [
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        },
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        },
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        },
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        },
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        },
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        },
                        {
                            lunch: {from: "08:30", to: "09:30"},
                            dinner: {from: "15:00", to: "15:30"},
                            supper: {from: "22:30", to: "23:30"}
                        }
                    ];
                } else {
                    $scope.MealPeriod = $rootScope.branch.meal_period;
                }
                $scope.save = function () {
                    // 修改餐段信息
                    var url = "/webApp/admin/hotel_branch/meal_period/modify/";
                    var param = {
                        branch_id: $rootScope.branch_id,
                        meal_period: $scope.MealPeriod
                    };
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            alert("修改餐段信息成功");
                        } else {
                            alert(obj.description);
                        }
                    });
                };
            }
        })
        .when('/Reserve/MealsArea', {
            templateUrl: "./template/" + Templates.Reserve.MealsArea, controller: function ($rootScope, $scope, $http, $q) {
                var TAG = Templates.Reserve.MealsArea;
                // 初始化门店区域列表
                $scope.data = {count: 0, list: []};
                // 【门店】获取门店区域列表area/list/";
                var url = "/webApp/admin/hotel_branch/area/list/";
                var param = {branch_id: $rootScope.branch_id};
                $http.post(url, JSON.stringify(param)).success(function (obj) {
                    if (obj.status === "true") {
                        $scope.data = obj.data;
                    } else {
                        alert(obj.description);
                    }
                });
                // 保存门店区域列表
                $scope.save = function () {
                    // 【添加】【修改】【删除】区域的请求
                    var request = {
                        // 批量增加门店的餐厅区域
                        add: {
                            url: "/webApp/admin/hotel_branch/area/add/",
                            param: {
                                branch_id: $rootScope.branch_id,
                                list: $scope.data.list.filter(function (item) {
                                    // 无id标记的是添加的数据
                                    return item.hasOwnProperty('area_id') === false;
                                })
                            }
                        },
                        // 批量修改门店的餐厅区域（包括删除）
                        modify: {
                            url: "/webApp/admin/hotel_branch/area/modify/",
                            param: {
                                list: $scope.data.list.filter(function (item) {
                                    // 有id标记的是原有的数据
                                    return item.hasOwnProperty('area_id') === true;
                                })
                            }
                        }
                    };
                    // 使用Angular的$q处理多个异步请求，在add和modify请求执行完毕时统一作出提示
                    $q.all({
                        add: $http.post(request.add.url, JSON.stringify(request.add.param)),
                        modify: $http.post(request.modify.url, JSON.stringify(request.modify.param))
                    }).then(function (array) {
                        var status = true;
                        // 输出执行结果
                        angular.forEach(array, function (item) {
                            if (item.status === "false") {
                                status = false;
                            }
                        });
                        if (status === true) {
                            // 【添加】和【修改】【删除】区域成功
                            alert("保存成功");
                        } else {
                            // 【添加】或【修改】【删除】区域失败
                            alert("添加失败");
                        }
                    });
                };
            }
        })
        .when('/Reserve/DeskRecommend', {
            templateUrl: "./template/" + Templates.Reserve.DeskRecommend, controller: function ($rootScope, $scope, $http) {

                var TAG = Templates.Reserve.DeskRecommend;

                $scope.numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21];
                $scope.selected_count = 1;
                $scope.desk = {count: 0, list: []};
                $scope.pages = [1, 2, 3, 4, 5, 6, 7];

                // 【管理员】获取桌位列表
                var getDeskList = function (selectCount) {
                    var url = "/webApp/admin/hotel_branch/desk/recommend/";
                    var param = {
                        branch_id: $rootScope.branch_id,
                        guest_number: selectCount
                    };
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $scope.desk = obj.data;
                        } else {
                            alert(obj.description);
                        }
                    });
                };

                getDeskList($scope.selected_count);

                $scope.change = function (selectCount) {
                    Log.i(TAG, "选择了：" + selectCount);
                    getDeskList(selectCount);
                };
                $scope.save = function () {
                    Log.i(TAG, JSON.stringify($scope.desk));
                }
            }
        })
        .when('/Reserve/PersonalTailor', {
            templateUrl: "./template/" + Templates.Reserve.PersonalTailor, controller: function ($rootScope, $scope, $http) {
                var TAG = Templates.Reserve.PersonalTailor;
                $scope.data = $rootScope.branch.personal_tailor;
                $scope.save = function () {
                    Log.i(TAG, JSON.stringify($scope.data));
                    // 【门店】保存私人订制列表
                    var url = "/webApp/admin/hotel_branch/personal_tailor/modify/";
                    var param = {
                        branch_id: $rootScope.branch_id,
                        personal_tailor: $scope.data
                    };
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            alert("保存成功");
                        } else {
                            alert(obj.description);
                        }
                    });
                }
            }
        })
        .otherwise({redirectTo: "/Reserve/:branch_id"});

}]);
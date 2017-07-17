/**
 * Created by 本山 on 2017/5/31.
 */

// 子页面模板
Templates = {
    // 路径导航
    Breadcrumb: "Drawer/Breadcrumb.html",
    // 员工管理
    Channel: {
        Channel: "Channel/Channel.html", // 获客渠道*** AddManager AddOuterChannel AddReserve
        Staff: "Channel/Staff.html", // 员工管理
        Privilege: "Channel/Privilege.html"// 权限管理
    },
    // 酒店管理
    Hotel: {
        Branch: "Hotel/Branch.html", // 门店管理
        Hotel: "Hotel/Hotel.html", // 酒店管理
        AccountManage: "Hotel/AccountManage.html" // 修改密码
    }
};

// 对话框模板
Dialog = {
    Channel: {
        Channel: {
            InternalChannelDialog: "Channel/Channel/InternalChannelDialog.html",
            ExternalChannelDialog: "Channel/Channel/ExternalChannelDialog.html"
        },
        Staff: {
            StaffDialog: "Channel/Staff/StaffDialog.html",
            ApproveDialog: "Channel/Staff/ApproveDialog.html"
        }
    },
    Hotel: {
        Branch: {
            BranchDialog: "Hotel/Branch/BranchDialog.html"
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

var ManagerApp = angular.module('ManagerApp', [
    'ngRoute',
    'ui.bootstrap'
]);

// 过滤器定义
ManagerApp.filter('gender', function () {
    return function (gender) {
        var TAG = ["保密", "先生", "女士"];
        return TAG[gender];
    }
});
ManagerApp.filter('surname', function () {
    return function (name) {
        return name.charAt(0);
    }
});
ManagerApp.filter('birthday_type', function () {
    return function (birthday_type) {
        var TAG = ["阳历", "农历"];
        return TAG[birthday_type];
    }
});
ManagerApp.filter('discount', function () {
    return function (discount) {
        var TAG = ["无折扣", "9.5折", "9.0折", "8.5折", "8.0折"];
        return TAG[discount];
    }
});
ManagerApp.filter('status', function () {
    return function (status) {
        var TAG = ["活跃", "沉睡", "流失", "无订单"];
        return TAG[status];
    }
});
ManagerApp.filter("channel", function () {
    return function (channel) {
        var TAG = ["无", "高层管理", "预定员和迎宾", "客户经理"];
        return TAG[channel];
    }
});
ManagerApp.filter("dinner_period", function () {
    return function (dinner_period) {
        var TAG = ['午餐', '晚餐', '夜宵'];
        return TAG[dinner_period];
    }
});
ManagerApp.filter("status", function () {
    return function (order_status) {
        var TAG = ["已订", "客到", "已完成", "已撤单"];
        return TAG[order_status];
    }
});

// 服务定义
ManagerApp.service('HotelService', function ($http) {

    // 【酒店】获取员工列表
    this.getProfile = function (hotel_id) {
        var url = "/webApp/admin/hotel/staff/list/";
        var param = {hotel_id: hotel_id};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                return obj.data;
            } else {
                alert(obj.description);
                return {count: '', list: []};
            }
        });
    };

    // 【酒店】获取渠道列表
    this.getChannelList = function (hotel_id) {
        url = "/webApp/admin/hotel/channel/list/";
        param = {hotel_id: hotel_id};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                return obj.data;
            } else {
                alert(obj.description);
                return {count: '', list: []};
            }
        });
    };
});
ManagerApp.service('BranchService', function ($http) {

    // 【门店】获取门店信息
    this.getProfile = function (branch_id) {
        var url = "/webApp/admin/hotel_branch/profile/get/";
        var param = {branch_id: branch_id};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                return obj.data;
            } else {
                alert(obj.description);
            }
        });
    };

    // 【门店】获取门店区域列表
    this.getAreaList = function (branch_id) {
        var url = "/webApp/admin/hotel_branch/area/list/";
        var param = {branch_id: branch_id};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                return obj.data;
            } else {
                alert(obj.description);
                return {count: '', list: []};
            }
        });
    }
});

// 侧边导航栏控制器
ManagerApp.controller('drawerCtrl', function ($rootScope, $scope, $http) {

    var TAG = 'drawerCtrl';

    // 酒店信息
    // $rootScope.Hotel = {
    //     hotel_id: 0,
    //     name: "未登录",
    //     icon: "/static/css/image/head1.jpg",
    //     mage: "http://fs.kebide.com/2016/07/12/eed874b7ac2b4f04b6d6d735f49dc373.jpg",
    //     branches_count: 10,
    //     owner_name: "杨秀荣",
    //     create_time: "创建时间"
    // };
    $rootScope.DeskType = [
        '普通包间', '豪华包间', '大厅卡座', '大厅散台',
        '宴会大厅', '多功能厅', '多桌包间', '隔断', '会场'
    ];
    // 餐段信息
    $rootScope.MealsTime = {
        lunch: [
            "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:30", "15:00", "15:30", "16:00"
        ],
        dinner: [
            "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:15",
            "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00", "20:30",
            "21:00", "21:30", "21:45", "22:00", "22:30", "23:00", "23:30", "23:45",
            "22:00", "22:30", "23:00", "23:30"
        ],
        supper: [
            "00:00", "00:30", "01:00", "01:30",
            "02:00", "02:30", "03:00", "03:30", "04:00"
        ]
    };
    // 权限信息
    $rootScope.Authority = [
        {
            name: "管理职能",
            checked: false,
            item: [
                {
                    name: "账户管理",
                    checked: false,
                    item: [
                        {name: "购买服务及续费", checked: false},
                        {name: "获客渠道管理", checked: false},
                        {name: "自定义Logo", checked: false},
                    ]
                }
            ]
        },
        {
            name: "营销职能",
            item: []
        },
        {
            name: "预订职能",
            item: []
        },
        {
            name: "销售职能",
            item: []
        },
        {
            name: "移动端管理",
            item: []
        }
    ];
    $scope.menus = [
        {
            title: "未登录",
            menu_id: "Login",
            item: []
        }
    ];
    $scope.Breadcrumb = [
        {title: "主页"},
        {title: "预订管理"},
        {title: "餐段设置"}
    ];


    var Hotel = {
        getProfile: function () {

        },
        getBranchList: function () {
            // 获取门店列表
            var url = "/webApp/admin/hotel_branch/list/";
            var param = {
                hotel_id: $rootScope.Hotel.hotel_id
            };
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $scope.Hotel.BranchList = obj.data;
                } else {
                    alert(obj.description);
                }
            });
        }
    };

    // 【酒店】获取酒店信息
    var url = "/webApp/admin/hotel/profile/get/";
    var param = {};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            Log.i(TAG, "获取酒店信息成功");
            $rootScope.Hotel = obj.data;
            // 侧边栏
            $scope.menus = [
                {
                    title: "员工管理",
                    menu_id: "Channel",
                    item: [
                        {title: "员工账户", item_id: "Staff"},
                        {title: "获客渠道", item_id: "Channel"}
                        // {title: "员工权限管理", item_id: "Privilege"}
                    ]
                },
                {
                    title: "酒店管理",
                    menu_id: "Hotel",
                    item: [
                        {title: "酒店基本信息", item_id: "Hotel"},
                        {title: "门店管理", item_id: "Branch"},
                        {title: "修改密码", item_id: "AccountManage"}
                    ]
                }
            ];
        } else {
            alert(obj.description);
            // 无该管理员，跳转到
            location.href = "login.html";
        }
    });

    $rootScope.$watch('Hotel', function (p1, p2, p3) {
        Hotel.getBranchList();
    });

    // // 【门店】获取门店信息
    // url = "/webApp/admin/hotel_branch/profile/get/";
    // param = {branch_id: $};
    // $http.post(url, JSON.stringify(param)).success(function (obj) {
    //     if (obj.status === "true") {
    //         $rootScope.branch = obj.data;
    //     } else {
    //         alert(obj.description);
    //     }
    // });

    // 【门店】获取门店区域列表
    // url = "/webApp/admin/hotel_branch/area/list/";
    // param = {branch_id: 1};
    // $http.post(url, JSON.stringify(param)).success(function (obj) {
    //     if (obj.status === "true") {
    //         $rootScope.area = obj.data;
    //     } else {
    //         alert(obj.description);
    //     }
    // });
});

// Angular路由配置
ManagerApp.config(['$routeProvider', function ($routeProvider) {

    // 【酒店】渠道管理
    $routeProvider
        .when('/Channel/Channel', {
            templateUrl: "./template/" + Templates.Channel.Channel, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Channel.Channel;
                // 初始化渠道列表
                // 初始化酒店信息
                $rootScope.$watch('Hotel', function () {
                    // 【酒店】获取渠道列表
                    var url = "/webApp/admin/hotel/channel/list/";
                    var param = {hotel_id: $rootScope.Hotel.hotel_id};
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $rootScope.Hotel.Channel = obj.data;
                            $scope.data = $rootScope.Hotel.Channel;
                        } else {
                            $rootScope.Hotel.Channel = {count: 0, list: []};
                            $scope.data = $rootScope.Hotel.Channel;
                            alert(obj.description);
                        }
                    });
                });
                /**
                 * 添加/编辑内部渠道
                 * @guest_channel 客户渠道：0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
                 */
                $scope.addInternalChannel = function (guest_channel) {
                    Log.i(TAG, "新增内部渠道");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.InternalChannelDialog,
                        resolve: {
                            form: function () {
                                var channel = {
                                    // 员工ID
                                    staff_id: -1,
                                    // 客户渠道
                                    guest_channel: guest_channel,
                                    // 职位
                                    position: "经理",
                                    // 电话隐私
                                    phone_private: true,
                                    // 职能权限
                                    privilege: [1, 3, 4, 6],
                                    // 销售职能
                                    sale_enabled: true,
                                    // 订单短信
                                    order_sms_inform: false,
                                    // 短信附加
                                    order_sms_attach: false,
                                    // 提成结算/接单提成
                                    order_bonus: {
                                        enabled: true,
                                        method: 1,
                                        value: 0.8
                                    },
                                    // 提成结算/开新客提成
                                    new_customer_bonus: {
                                        enabled: false,
                                        value: 0.8
                                    },
                                    // 管辖桌位
                                    manage_desks: [],
                                    // 管辖区域
                                    manage_areas: [0, 2, 3]
                                };
                                // 根据渠道类型不同，添加不同附加信息
                                switch (guest_channel) {
                                    case 0:
                                        break;
                                    case 1:
                                        // 【高层管理】
                                        angular.extend(channel, {
                                            //+管理渠道客户
                                            manage_channel: [1, 2, 3]
                                        });
                                        break;
                                    case 2:
                                        // 【预订员】 +沟通渠道
                                        angular.extend(channel, {
                                            communicate: {
                                                // 沟通渠道
                                                channel: "tel_box",
                                                // 电话盒子
                                                tel_box: [
                                                    "(来电盒子)线路1", "(来电盒子)线路2", "(来电盒子)线路3", "(来电盒子)线路4",
                                                    "(来电盒子)线路5", "(来电盒子)线路6", "(来电盒子)线路7", "(来电盒子)线路8"
                                                ],
                                                // 智能电话
                                                smart_tel: [
                                                    "(智能电话)线路1", "(智能电话)线路2", "(智能电话)线路3", "(智能电话)线路4",
                                                    "(智能电话)线路5", "(智能电话)线路6", "(智能电话)线路7"
                                                ]
                                            }
                                        });
                                        break;
                                    case 3:
                                        // 【客户经理】
                                        channel.sale_enabled = true;
                                        break;
                                    default:
                                        break;
                                }
                                return channel;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.InternalChannelDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.option = "新增";
                            $scope.form = form;
                            $scope.staffs = $rootScope.staff;
                            $scope.area = $rootScope.area;
                            $scope.box = [];
                            $scope.phone = [];
                            // 选择区域
                            $scope.checkArea = function (area_id) {
                                if ($scope.form.manage_areas.indexOf(area_id)) {
                                    var index = $scope.form.manage_areas.indexOf(area_id);
                                    $scope.form.manage_areas.splice(index, 1);
                                } else {
                                    $scope.form.manage_areas.push(x.area_id);
                                }
                            };
                            // 选择电话盒子
                            $scope.check_box = function (value) {
                                $scope.form.communicate.box[value] = true;
                            };
                            // 选择智能电话
                            $scope.check_phone = function (value) {
                                $scope.form.communicate.phone[value] = true;
                            };
                            $scope.save = function () {
                                dlg.close($scope.form);
                            };
                            $scope.fire = function () {

                            };
                            $scope.cancel = function () {
                                dlg.dismiss('取消操作');
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/internal_channel/add/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data.internal_channel.push(result);
                                alert("添加渠道成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                $scope.editInternalChannel = function (channel) {
                    Log.i(TAG, "编辑内部渠道");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.InternalChannelDialog,
                        resolve: {
                            form: function () {
                                return channel;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.InternalChannelDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.area = $rootScope.area;
                            $scope.staffs = $rootScope.staffs;
                            $scope.box = [];
                            $scope.phone = [];
                            // 选择区域
                            $scope.checkArea = function (area_id) {
                                if ($scope.form.manage_areas.indexOf(area_id)) {
                                    var index = $scope.form.manage_areas.indexOf(area_id);
                                    $scope.form.manage_areas.splice(index, 1);
                                } else {
                                    $scope.form.manage_areas.push(x.area_id);
                                }
                            };
                            // 选择电话盒子
                            $scope.check_box = function (value) {
                                $scope.form.communicate.box[value] = true;
                            };
                            // 选择智能电话
                            $scope.check_phone = function (value) {
                                $scope.form.communicate.phone[value] = true;
                            };
                            $scope.submit = function () {
                                dlg.close($scope.form);
                            };
                            $scope.cancel = function () {
                                dlg.dismiss('取消操作');
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/staff/modify/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data.external_channel.push(result);
                                alert("编辑内部渠道成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                // 添加/编辑外部渠道
                $scope.addExternalChannel = function () {
                    Log.i(TAG, "新增外部渠道");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.ExternalChannelDialog,
                        resolve: {
                            form: function () {
                                return {
                                    // 名称
                                    name: "118114",
                                    // 折扣
                                    discount: 2,
                                    // 合作起始时间
                                    begin_cooperate_time: "2017-07-01",
                                    // 合作结束时间
                                    end_cooperate_time: "2017-07-05",
                                    // 佣金核算方式
                                    commission_type: 0,
                                    // 佣金核算数值
                                    commission_value: 1,
                                    // 头像
                                    icon: "/static/css/image/head1.jpg",
                                    // 直属上级id
                                    staff_id: 1
                                };
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.ExternalChannelDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.option = "新增";
                            $scope.form = form;
                            $scope.staff = $rootScope.staff;
                            $scope.discount = ["无折扣", "9.5折", "9.0折", "8.5折", "8.0折"];
                            $scope.submit = function () {
                                dlg.close($scope.form);
                            };
                            $scope.cancel = function () {
                                dlg.dismiss('cancel');
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/external_channel/add/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data.external_channel.push(result);
                                alert("添加外部渠道成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                $scope.editExternalChannel = function (channel) {
                    Log.i(TAG, "编辑外部渠道");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.ExternalChannelDialog,
                        resolve: {
                            form: function () {
                                return channel;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.ExternalChannelDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.discount = ["无折扣", "9.5折", "9.0折", "8.5折", "8.0折"];
                            $scope.submit = function () {
                                dlg.close($scope.form);
                            };
                            $scope.cancel = function () {
                                dlg.dismiss('cancel');
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, "编辑" + JSON.stringify(result));
                        $scope.channel.outer.push(result);
                        var url = "/webApp/admin/hotel/external_channel/modify/";
                        $http.post(url, JSON.stringify(result)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data.external_channel.push(result);
                                alert("编辑外部渠道成功");
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
        .when('/Channel/Staff', {
            templateUrl: "./template/" + Templates.Channel.Staff, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Channel.Staff;
                // 初始化员工列表
                $rootScope.$watch('Hotel', function () {
                    // 【酒店】获取员工列表
                    var url = "/webApp/admin/hotel/staff/list/";
                    var param = {hotel_id: $rootScope.Hotel.hotel_id};
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $rootScope.Hotel.StaffList = obj.data;
                            $scope.data = $rootScope.Hotel.StaffList;
                        } else {
                            $rootScope.Hotel.StaffList = {count: 0, list: []};
                            $scope.data = $rootScope.Hotel.StaffList;
                            alert(obj.description);
                        }
                    });
                });
                // 审核员工
                $scope.approve = function (staff) {
                    Log.i(TAG, "审核员工：" + JSON.stringify(staff));
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Staff.StaffDialog,
                        controller: function ($scope, form) {
                            $scope.option = "审核";
                            $scope.form = form;
                            delete $scope.form["staff_number"];
                            $scope.submit = function () {
                                dlg.close($scope.form);
                            };
                            $scope.reject = function () {

                            };
                            $scope.cancel = function () {
                                dlg.dismiss({reason: "取消"});
                            }
                        },
                        resolve: {
                            form: function () {
                                return angular.copy(staff);
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/staff/profile/modify/";
                        var param = angular.copy(result);
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("审核通过");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                // 编辑员工信息
                $scope.edit = function (staff) {
                    Log.i(TAG, "编辑员工信息：" + JSON.stringify(staff));
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Staff.StaffDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.StaffDialog;
                            Log.i(TAG, "编辑员工控制器");
                            $scope.option = "编辑";
                            $scope.guest_channel = ["无", "高层管理", "预定员和迎宾", "客户经理"];
                            $scope.form = form;
                            $scope.submit = function () {
                                Log.i(TAG, "提交员工信息：" + $scope.form);
                                dlg.close($scope.form);
                            };
                            $scope.exit = function () {
                                Log.i(TAG, "员工离岗");
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消员工信息");
                                dlg.dismiss();
                            }
                        },
                        resolve: {
                            form: function () {
                                return angular.copy(staff);
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/staff/profile/modify/";
                        var param = result;
                        param.password = hex_md5(param.password);
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("编辑员工成功");
                                $scope.data.list.push(result);
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                // 添加员工
                $scope.add_staff = function () {
                    Log.i(TAG, "添加员工");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Staff.StaffDialog,
                        resolve: {
                            form: function () {
                                return {
                                    hotel_id: $rootScope.Hotel.hotel_id,
                                    branch_id: 0,
                                    phone: "",
                                    name: "",
                                    id_number: "",
                                    password: "",
                                    position: "经理",
                                    guest_channel: 0,
                                    gender: 1,
                                    status: 1
                                };
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.StaffDialog;
                            Log.i(TAG, "添加员工控制器");
                            $scope.option = "添加";
                            $scope.guest_channel = ["无", "高层管理", "预定员和迎宾", "客户经理"];
                            $scope.form = form;
                            // 提交
                            $scope.submit = function () {
                                Log.i(TAG, "提交员工信息：" + $scope.form);
                                dlg.close($scope.form);
                            };
                            // 离岗
                            $scope.exit = function () {
                                Log.i(TAG, "员工离岗");
                            };
                            // 取消
                            $scope.cancel = function () {
                                Log.i(TAG, "取消员工信息");
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/staff/add/";
                        var param = angular.copy(result);
                        param.password = hex_md5(param.password);
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("添加员工成功");
                                $scope.data.list.push(result);
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
        .when('/Channel/Privilege', {templateUrl: "./template/" + Templates.Channel.Privilege});

    // 【酒店】酒店管理
    $routeProvider
        .when('/Hotel/Branch', {
            templateUrl: "./template/" + Templates.Hotel.Branch, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Hotel.Branch;
                $scope.layouts = ["grid", "list"];
                $scope.layout = "list";
                $scope.data = {count: 0, list: []};
                // 获取门店列表
                var url = "/webApp/admin/hotel_branch/list/";
                var param = {
                    hotel_id: $rootScope.Hotel.hotel_id
                };
                $http.post(url, JSON.stringify(param)).success(function (obj) {
                    if (obj.status === "true") {
                        $scope.data = obj.data;
                    } else {
                        alert(obj.description);
                    }
                });
                // 切换布局
                $scope.changeLayout = function () {
                    if ($scope.layout === 'grid') {
                        $scope.layout = 'list';
                    } else if ($scope.layout === 'list') {
                        $scope.layout = 'grid';
                    } else {
                        $scope.layout = 'list';
                    }
                };
                // 添加门店
                $scope.addBranch = function () {
                    Log.i(TAG, "添加门店");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Hotel.Branch.BranchDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Hotel.Branch.BranchDialog;
                            Log.i(TAG, "添加门店");
                            // 初始化员工列表
                            $scope.staff = $rootScope.Hotel.StaffList;
                            // 初始化手机号
                            $scope.phone = "";
                            // 初始化酒店设施
                            $scope.facility = "";
                            $scope.facilities = [
                                "万事达(Master)", "可以刷卡", "有停车位", "全场禁烟",
                                "区分烟区", "无线上网", "露天位", "有舞台",
                                "有表演", "下午茶", "夜宵", "四合院"
                            ];
                            // 初始化支付方式
                            $scope.pay_card = "";
                            $scope.pay_cards = [
                                "支付宝", "微信", "VISA", "银联"
                            ];
                            // 初始化表单
                            $scope.option = "添加";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑门店信息");
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存门店信息");
                                dlg.close(form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消保存");
                            }
                        },
                        resolve: {
                            form: function () {
                                return {
                                    // 酒店ID
                                    hotel_id: $rootScope.Hotel.hotel_id,
                                    // 店长ID
                                    staff_id: 0,
                                    // 名称
                                    name: "北京宴总店",
                                    // 省
                                    province: "北京市",
                                    // 市
                                    city: "北京市",
                                    // 区/县
                                    county: "丰台区",
                                    // 详细地址
                                    address: "北京市丰台区靛厂路333号",
                                    // 电话
                                    phone: [],
                                    // 设施
                                    facility: [],
                                    // 支付方式
                                    pay_card: [],
                                    // 其他可选项
                                    icon: "/static/css/image/head.jpg"
                                };
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel_branch/register/";
                        var param = result;
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data.list.push(param);
                                alert("添加门店成功");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                // 编辑门店
                $scope.editBranch = function (branch) {
                    Log.i(TAG, "编辑门店：" + branch.name);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Hotel.Branch.BranchDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.BranchDialog;
                            Log.i(TAG, "编辑门店：" + branch.name);
                            // 初始化员工列表
                            $scope.staff = $rootScope.Hotel.StaffList;
                            // 初始化手机号
                            $scope.phone = "";
                            // 初始化门店设施
                            $scope.facility = "";
                            $scope.facilities = [
                                "万事达(Master)", "可以刷卡", "有停车位", "全场禁烟",
                                "区分烟区", "无线上网", "露天位", "有舞台",
                                "有表演", "下午茶", "夜宵", "四合院"
                            ].filter(function (p1, p2, p3) {
                                return form.facility.indexOf(p1) === -1;
                            });
                            // 初始化支付方式
                            $scope.pay_card = "";
                            $scope.pay_cards = [
                                "支付宝", "微信", "VISA", "银联"
                            ].filter(function (p1, p2, p3) {
                                return form.pay_card.indexOf(p1) === -1;
                            });
                            // 初始化表单
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑门店信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存门店信息");
                                dlg.close($scope.form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消保存");
                                dlg.dismiss({tag: "取消保存"});
                            }
                        },
                        resolve: {
                            form: function () {
                                return angular.copy(branch);
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel_branch/profile/modify/";
                        var param = result;
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("修改门店信息成功");
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
        .when('/Hotel/Hotel', {
            templateUrl: "./template/" + Templates.Hotel.Hotel, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Hotel.Hotel;
                $scope.form = $rootScope.Hotel;
                $scope.data = $rootScope.Hotel;
                $scope.submit = function () {
                    Log.i(TAG, "提交酒店信息：" + JSON.stringify($scope.form))
                }
            }
        })
        .when('/Hotel/AccountManage', {
            templateUrl: "./template/" + Templates.Hotel.AccountManage, controller: function ($rootScope, $scope, $http) {
                var TAG = Templates.Hotel.AccountManage;
                $scope.form = {
                    username: $rootScope.Hotel.name,
                    old_password: "",
                    new_password: "",
                    new_password_acc: ""
                };
                $scope.save = function () {
                    Log.i(TAG, JSON.stringify($scope.form));
                    var url = "/webApp/admin/pass_modify/";
                    var param = angular.copy($scope.form);
                    param.new_password = hex_md5(param.new_password);
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            alert("密码修改成功");
                        } else {
                            alert(obj.description);
                        }
                    });
                }
            }
        });

    // 【酒店】默认自动进入酒店管理
    $routeProvider
        .otherwise({redirectTo: "/Channel/Channel"});
}]);
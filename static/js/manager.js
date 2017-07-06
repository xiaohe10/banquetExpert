/**
 * Created by 本山 on 2017/5/31.
 */

// 子页面模板
Templates = {
    // 路径导航
    Breadcrumb: "Drawer/Breadcrumb.html",
    // 超级管理后台
    // SuperAdmin: {
    //     SuperAdmin: "SuperAdmin/SuperAdmin.html" // 超级管理后台
    // },
    // 后台用户管理
    Channel: {
        Channel: "Channel/Channel.html", // 获客渠道*** AddManager AddOuterChannel AddReserve
        Staff: "Channel/Staff.html", // 员工管理
        Privilege: "Channel/Privilege.html"// 权限管理
    },
    // 智能订餐台
    SmartOrder: {
        SmartOrder: "SmartOrder/SmartOrder.html"// 智能订餐台
    },
    // 预定管理
    Reserve: {
        AreaDesk: "Reserve/AreaDesk.html", // 桌位设置
        MealsTime: "Reserve/MealsTime.html", // 餐段管理
        MealsArea: "Reserve/MealsArea.html", // 餐位设置
        DeskRecommend: "Reserve/DeskRecommend.html",// 自动推荐桌位
        PersonalTailor: "Reserve/PersonalTailor.html"// 私人订制
    },
    // 订单管理
    Order: {
        InsertOrder: "Order/InsertOrder.html",// 订单金额录入
        OperationLog: "Order/OperationLog.html", // 操作日志
        OrderHistory: "Order/OrderHistory.html",// 历史订单
        OrderStatistics: "Order/OrderStatistics.html",// 订单统计
        PhoneReserve: "Order/PhoneReserve.html", // 来电记录
        ReserveNotice: "Order/ReserveNotice.html"// 预定通知单
    },
    // 客户管理
    Customer: {
        AnniversaryReport: "Customer/AnniversaryReport.html", // 纪念日查询报表
        CustomerAnalysis: "Customer/CustomerAnalysis.html", // 客源情况分析
        CustomerProfiles: "Customer/CustomerProfiles.html", // 客户档案列表*** AddCustomerProfiles BatchExport BatchImport
        CustomerRecycleBin: "Customer/CustomerRecycleBin.html", // 客户档案回收站
        MemberValue: "Customer/MemberValue.html"// 会员价值设置
    },
    // 账户管理
    Account: {
        FinanceManage: "Account/FinanceManage.html", // 财务报表
        SMSDetails: "Account/SMSDetails.html", // 短信详单
        Restaurant: "Account/Restaurant.html", // 餐厅基本信息
        AccountManage: "Account/AccountManage.html"
    },
    // 酒店管理
    Hotel: {
        Branch: "Hotel/Branch.html", // 门店管理
        Hotel: "Hotel/Hotel.html" // 酒店管理
    },
    // 评分审阅
    Review: {
        Rank: "Review/Rank.html", // 餐厅排名
        Tutorial: "Review/Tutorial.html"// 中国服务私人订制标准视频教程
    }
};

// 对话框模板
Dialog = {
    // SuperAdmin: {
    //     SuperAdmin: {
    //         HotelDialog: "SuperAdmin/SuperAdmin/HotelDialog.html"
    //     }
    // },
    Channel: {
        Channel: {
            ExternalChannelDialog: "Channel/Channel/ExternalChannelDialog.html",
            ManagerDialog: "Channel/Channel/ManagerDialog.html",
            ReserveDialog: "Channel/Channel/ReserveDialog.html",
        },
        Staff: {
            StaffDialog: "Channel/Staff/StaffDialog.html",
            ApproveDialog: "Channel/Staff/ApproveDialog.html"
        }
    },
    Customer: {
        CustomerProfiles: {
            AddCustomerProfiles: "Customer/CustomerProfiles/AddCustomerProfiles.html",
            BatchExport: "Customer/CustomerProfiles/BatchExport.html",
            BatchImport: "Customer/CustomerProfiles/BatchImport.html"
        }
    },
    Hotel: {
        Branch: {
            BranchDialog: "Hotel/Branch/BranchDialog.html"
        }
    },
    Order: {
        OrderHistory: {
            OrderAppend: "Order/OrderHistory/OrderAppend.html",
            OrderDetails: "Order/OrderHistory/OrderDetails.html"
        },
        ReserveNotice: {
            ReserveOrderDetails: "Order/ReserveNotice/ReserveOrderDetails.html"
        }
    },
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

var BanquetExpertApp = angular.module('BanquetExpertApp', [
    'ngRoute',
    'ui.bootstrap'
]);

// 过滤器定义
BanquetExpertApp.filter('gender', function () {
    return function (gender) {
        var TAG = ["保密", "先生", "女士"];
        return TAG[gender];
    }
});
BanquetExpertApp.filter('surname', function () {
    return function (name) {
        return name.charAt(0);
    }
});
BanquetExpertApp.filter('birthday_type', function () {
    return function (birthday_type) {
        var TAG = ["阳历", "农历"];
        return TAG[birthday_type];
    }
});
BanquetExpertApp.filter('discount', function () {
    return function (discount) {
        var TAG = ["无折扣", "9.5折", "9.0折", "8.5折", "8.0折"];
        return TAG[discount];
    }
});
BanquetExpertApp.filter('status', function () {
    return function (status) {
        var TAG = ["活跃", "沉睡", "流失", "无订单"];
        return TAG[status];
    }
});
BanquetExpertApp.filter("channel", function () {
    return function (channel) {
        var TAG = ["无", "高层管理", "预定员和迎宾", "客户经理"];
        return TAG[channel];
    }
});

// 侧边导航栏控制器
BanquetExpertApp.controller('drawerCtrl', function ($rootScope, $scope, $http) {

    var TAG = 'drawerCtrl';

    // 酒店信息
    $rootScope.Hotel = {
        hotel_id: 1,
        name: "未登录",
        icon: "/static/css/image/head1.jpg",
        mage: "http://fs.kebide.com/2016/07/12/eed874b7ac2b4f04b6d6d735f49dc373.jpg",
        branches_count: 10,
        owner_name: "杨秀荣",
        create_time: "创建时间"
    };
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
            "21:00", "21:30", "21:45", "22:00", "22:30", "23:00", "23:30", "23:45"
        ],
        supper: [
            "22:00", "22:30", "23:00", "23:30", "00:00", "00:30", "01:00", "01:30",
            "02:00", "02:30", "03:00", "03:30", "04:00"
        ]
    };
    $scope.hotel = $rootScope.Hotel;
    $scope.menus = [
        {
            title: "登录",
            menu_id: "Login",
            item: []
        }
    ];
    $scope.Breadcrumb = [
        {title: "主页"},
        {title: "预订管理"},
        {title: "餐段设置"}
    ];

    // 【酒店】获取酒店信息
    var url = "/webApp/admin/hotel/profile/get/";
    var param = {};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            Log.i(TAG, "获取酒店信息成功");
            $rootScope.Hotel = obj.data;
            $scope.hotel = $rootScope.Hotel;
            $scope.menus = [
                {
                    title: "员工管理",
                    menu_id: "Channel",
                    item: [
                        {title: "员工账户", item_id: "Staff"},
                        {title: "获客渠道", item_id: "Channel"},
                        {title: "员工权限管理", item_id: "Privilege"}
                    ]
                },
                {
                    title: "智能订餐台",
                    menu_id: "SmartOrder",
                    item: [
                        {title: "智能订餐台", item_id: "SmartOrder"}
                    ]
                },
                {
                    title: "预订管理",
                    menu_id: "Reserve",
                    item: [
                        {title: "餐段设置", item_id: "MealsTime"},
                        {title: "餐位设置", item_id: "MealsArea"},
                        {title: "桌位设置", item_id: "AreaDesk"},
                        {title: "自动推荐桌位", item_id: "DeskRecommend"},
                        {title: "私人订制", item_id: "PersonalTailor"}
                    ]
                },
                {
                    title: "订单管理",
                    menu_id: "Order",
                    item: [
                        {title: "预定通知单", item_id: "ReserveNotice"},
                        {title: "历史订单", item_id: "OrderHistory"},
                        {title: "订单金额录入", item_id: "InsertOrder"},
                        {title: "订单统计", item_id: "OrderStatistics"},
                        {title: "来电记录", item_id: "PhoneReserve"},
                        {title: "操作日志", item_id: "OperationLog"}
                    ]
                },
                {
                    title: "客户管理",
                    menu_id: "Customer",
                    item: [
                        {title: "客户档案列表", item_id: "CustomerProfiles"},
                        {title: "客源情况分析", item_id: "CustomerAnalysis"},
                        {title: "会员价值设置", item_id: "MemberValue"},
                        {title: "客户档案回收站", item_id: "CustomerRecycleBin"},
                        {title: "纪念日查询报表", item_id: "AnniversaryReport"}
                    ]
                },
                {
                    title: "账户管理",
                    menu_id: "Account",
                    item: [
                        {title: "财务报表", item_id: "FinanceManage"},
                        {title: "短信详单", item_id: "SMSDetails"},
                        {title: "酒店基本信息", item_id: "Restaurant"},
                        {title: "修改密码", item_id: "AccountManage"}
                    ]
                },
                {
                    title: "酒店管理",
                    menu_id: "Hotel",
                    item: [
                        {title: "酒店基本信息", item_id: "Hotel"},
                        {title: "门店管理", item_id: "Branch"}
                    ]
                },
                {
                    title: "评分审阅",
                    menu_id: "Review",
                    item: [
                        {title: "酒店排名", item_id: "Rank"},
                        {title: "中国服务私人订制标准视频教程", item_id: "Tutorial"}
                    ]
                }
            ];
        } else {
            alert(obj.description);
            location.href = "login.html";
        }
    });

    // 【酒店】获取员工列表
    url = "/webApp/admin/hotel/staff/list/";
    param = {hotel_id: $scope.hotel.hotel_id};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.staff = obj.data;
        } else {
            alert(obj.description);
        }
    });

    // 【酒店】获取渠道列表
    url = "/webApp/admin/hotel/channel/list/";
    param = {hotel_id: $scope.hotel.hotel_id};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.channel = obj.data;
        } else {
            alert(obj.description);
        }
    });

    // 【门店】获取门店信息
    url = "/webApp/admin/hotel_branch/profile/get/";
    param = {branch_id: 1};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.branch = obj.data;
        } else {
            alert(obj.description);
        }
    });

    // 【门店】获取门店区域列表
    url = "/webApp/admin/hotel_branch/area/list/";
    param = {branch_id: 1};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.area = obj.data;
        } else {
            alert(obj.description);
        }
    });

    // 获取餐段列表
    // url = "/data/meal_period.json";
    // $http.post(url, JSON.stringify(param)).success(function (obj) {
    //     if (obj.status === "true") {
    //         $rootScope.MealsTime = obj;
    //         Log.i(TAG, JSON.stringify($rootScope.MealsTime));
    //     } else {
    //         alert(obj.description);
    //     }
    // });
});

// Angular路由配置
BanquetExpertApp.config(['$routeProvider', function ($routeProvider) {

    // 账户管理
    $routeProvider
        .when('/Account/AccountManage', {
            templateUrl: "./template/" + Templates.Account.AccountManage, controller: function ($scope) {
                $scope.form = {
                    username: "",
                    password: "",
                    new_password: "",
                    new_password_acc: ""
                };
                $scope.save = function () {
                    Log.i(TAG, $scope.form);
                }
            }
        })
        .when('/Account/FinanceManage', {
            templateUrl: "./template/" + Templates.Account.FinanceManage, controller: function ($scope) {
                var TAG = Templates.Account.FinanceManage;
                $scope.option = {
                    selected_year: 1,
                    selected_month: 1
                };
                $scope.detail = {
                    rest: "636.96", recharge: "500.0000", sms_cost: "476.24", service_cost: "476.24"
                };
                $scope.year = [2011, 2012, 2013, 2014, 2015, 2016, 2017];
                $scope.month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
                $scope.table = [];
                for (var i = 0; i < 10; i++) {
                    $scope.table.push({
                        date: "2017年5月24日", recharge: "0.00", sms_cost: "8.00",
                        order_cost: "8.00", service_cost: "0.00", sum: "0.00", rest: "636.96"
                    });
                }
                $scope.query = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
            }
        })
        .when('/Account/SMSDetails', {templateUrl: "./template/" + Templates.Account.SMSDetails})
        .when('/Account/Restaurant', {
            templateUrl: "./template/" + Templates.Account.Restaurant, controller: function ($scope) {

            }
        });

    // 渠道管理
    $routeProvider
        .when('/Channel/Channel', {
            templateUrl: "./template/" + Templates.Channel.Channel, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Channel.Channel;
                // 初始化渠道列表
                $scope.data = $rootScope.channel;
                // 添加/编辑预订员和迎宾
                $scope.addReserve = function () {
                    Log.i(TAG, "新增预订员和迎宾");
                    var dlg = $modal.open({
                        size: 'lg',
                        templateUrl: "./template/" + Dialog.Channel.Channel.ReserveDialog,
                        controller: function ($scope) {
                            var TAG = Dialog.Channel.Channel.ReserveDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.form = {
                                // 操作
                                option: "edit",
                                // 姓名
                                name: "mbs",
                                // 性别
                                gender: "male",
                                // 电话
                                phone: "18800184976",
                                // 职位
                                job: "学生",
                                // 用户名
                                username: "mbs0221",
                                // 密码
                                password: "mbs0221",
                                // 职能权限
                                privilege: {
                                    // 管理职能
                                    manage: {},
                                    // 营销职能
                                    marketing: {},
                                    // 预定职能
                                    reserve: {},
                                    // 销售职能
                                    sale: {}
                                },
                                // 销售职能
                                sale: true,
                                // 订单短信
                                order_sms: false,
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
                                desk_manage: {
                                    // 管辖全部桌位
                                    all_desk: false,
                                    // 桌位信息
                                    area: $rootScope.area
                                },
                                // 管辖区域
                                select_area: [0, 2, 3],
                                // 沟通渠道
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
                            };
                            $scope.area = $rootScope.area;
                            $scope.box = [];
                            $scope.phone = [];
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
                        $scope.reserve.push(result);
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                $scope.editReserve = function (reserve) {
                    Log.i(TAG, "编辑预订员和迎宾");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.ReserveDialog,
                        resolve: {
                            form: function () {
                                return reserve;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.ReserveDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.form = form;
                            $scope.area = $rootScope.area;
                            $scope.box = [];
                            $scope.phone = [];
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
                };
                // 添加/编辑高层管理
                $scope.addManager = function () {
                    Log.i(TAG, "新增客户经理");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.ManagerDialog,
                        controller: function ($scope) {
                            var TAG = Dialog.Channel.Channel.ManagerDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.form = {
                                // 姓名
                                name: "赵强",
                                // 性别
                                gender: "female",
                                // 电话
                                phone: [18800184976, 10000000000],
                                // 生日
                                birthday: "2017-6-22",
                                // 单位
                                unit: "创业谷",
                                // 现住址
                                address: {
                                    province: "北京",
                                    city: "北京",
                                    county: "朝阳"
                                },
                                // 籍贯
                                native: {
                                    province: "北京",
                                    city: "朝阳"
                                },
                                // 营销短信
                                sms_marketing: "enabled",
                                // 分类方法
                                classification_method: 0,
                                // 病症
                                desease: ["A", "B", "C"],
                                // 喜好
                                hobby: ["A", "B", "C"],
                                // 忌口
                                dieting: ["A", "B", "C"],
                                // 不良记录
                                bad_records: "This is bad records"
                            };
                            $scope.submit = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                };
                $scope.editManager = function (manager) {
                    Log.i(TAG, "编辑客户经理");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.ManagerDialog,
                        resolve: {
                            form: function () {
                                return manager;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.ManagerDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.form = form;
                            $scope.submit = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                };
                // 添加/编辑外部渠道
                $scope.addExternalChannel = function () {
                    Log.i(TAG, "新增外部渠道");
                    var dlg = $modal.open({
                            templateUrl: "./template/" + Dialog.Channel.Channel.ExternalChannelDialog,
                            resolve: {
                                form: function () {
                                    var channel = {
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
                                        }
                                    ;
                                    return channel;
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
                        }
                    );
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/admin/hotel/external_channel/add/";
                        var param = result;
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
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
                        Log.i(TAG, "添加" + JSON.stringify(result));
                        $scope.channel.outer.push(result);
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
                $scope.data = $rootScope.staff;
                // 审核员工
                $scope.approve = function (staff) {
                    Log.i(TAG, "审核员工：" + JSON.stringify(staff));
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Staff.StaffDialog,
                        controller: function ($scope, form) {
                            $scope.option = "审核";
                            $scope.form = form;
                            $scope.admit = function () {

                            };
                            $scope.reject = function () {

                            };
                            $scope.cancel = function () {

                            }
                        },
                        resolve: {
                            form: function () {
                                return staff;
                            }
                        }
                    });
                };
                // 编辑员工信息
                $scope.edit = function (staff) {
                    Log.i(TAG, "编辑员工信息：" + JSON.stringify(staff));
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Staff.StaffDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.EditStaff;
                            Log.i(TAG, "编辑员工控制器");
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.submit = function () {
                                Log.i(TAG, "提交员工信息：" + $scope.form);
                            };
                            $scope.exit = function () {
                                Log.i(TAG, "员工离岗");
                                dlg.close(id);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消员工信息");
                            }
                        },
                        resolve: {
                            form: function () {
                                return staff;
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
                };
                // 添加员工
                $scope.add_staff = function () {
                    Log.i(TAG, "添加员工");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Staff.StaffDialog,
                        resolve: {
                            form: function () {
                                var staff = {
                                    hotel_id: $rootScope.Hotel.hotel_id,
                                    phone: "18800184976",
                                    name: "赵强",
                                    id_number: "100124100124100124",
                                    password: "sunny",
                                    position: "经理",
                                    gender: 1,
                                    status: 1
                                };
                                return staff;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.StaffDialog;
                            Log.i(TAG, "添加员工控制器");
                            $scope.option = "添加";
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
                        var param = result;
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

// 客户管理
    $routeProvider
        .when('/Customer/AnniversaryReport', {
            templateUrl: "./template/" + Templates.Customer.AnniversaryReport, controller: function ($scope) {
                var TAG = Templates.Customer.AnniversaryReport;
                $scope.option = {
                    date_from: "",
                    date_to: "",
                    selection: 0
                };
                $scope.classify = [
                    "生日", "满月", "百天", "过寿", "求婚日",
                    "订婚日", "结婚日", "周年庆"
                ];
                $scope.table = [];
                for (var i = 0; i < 7; i++) {
                    $scope.table.push({
                        anniversary: "纪念日", relation: "关系", date: "本年对应日期", days: "距离天数",
                        customer_summary: "客户信息", customer_phone: "联系电话", customer_type: "客户类别",
                        channel: "维护人"
                    });
                }
                $scope.query = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                }
            }
        })
        .when('/Customer/CustomerAnalysis', {
            templateUrl: "./template/" + Templates.Customer.CustomerAnalysis, controller: function ($scope) {
                var json = {
                    chart: {type: 'area'},
                    title: {text: 'US and USSR nuclear stockpiles'},
                    subtitle: {
                        text: 'Source: the bullet in</a>'
                    },
                    tooltip: {
                        pointFormat: '{series.name} produced <b>{point.y:,.0f}</b><br/>warheads in {point.x}'
                    },
                    xAxis: {
                        allowDecimals: false,
                        labels: {
                            formatter: function () {
                                return this.value; // clean, unformatted number for year
                            }
                        }
                    },
                    yAxis: {
                        title: {
                            text: 'Nuclear weapon states'
                        },
                        labels: {
                            formatter: function () {
                                return this.value / 1000 + 'k';
                            }
                        }
                    },
                    series: [
                        {
                            name: 'USA',
                            data: [
                                null, null, null, null, null, 6, 11, 32, 110, 235, 369, 640,
                                1005, 1436, 2063, 3057, 4618, 6444, 9822, 15468, 20434, 24126,
                                27387, 29459, 31056, 31982, 32040, 31233, 29224, 27342, 26662,
                                26956, 27912, 28999, 28965, 27826, 25579, 25722, 24826, 24605,
                                24304, 23464, 23708, 24099, 24357, 24237, 24401, 24344, 23586,
                                22380, 21004, 17287, 14747, 13076, 12555, 12144, 11009, 10950,
                                10871, 10824, 10577, 10527, 10475, 10421, 10358, 10295, 10104
                            ]
                        },
                        {
                            name: 'USSR/Russia',
                            data: [
                                null, null, null, null, null, null, null, null, null, null,
                                5, 25, 50, 120, 150, 200, 426, 660, 869, 1060, 1605, 2471, 3322,
                                4238, 5221, 6129, 7089, 8339, 9399, 10538, 11643, 13092, 14478,
                                15915, 17385, 19055, 21205, 23044, 25393, 27935, 30062, 32049,
                                33952, 35804, 37431, 39197, 45000, 43000, 41000, 39000, 37000,
                                35000, 33000, 31000, 29000, 27000, 25000, 24000, 23000, 22000,
                                21000, 20000, 19000, 18000, 18000, 17000, 16000
                            ]
                        }
                    ],
                    plotOptions: {
                        area: {
                            pointStart: 1940,
                            marker: {
                                enabled: false,
                                symbol: 'circle',
                                radius: 2,
                                states: {
                                    hover: {
                                        enabled: true
                                    }
                                }
                            }
                        }
                    }
                };
                $("#chart1").highcharts(json);
                $("#chart2").highcharts(json);
            }
        })
        .when('/Customer/CustomerProfiles', {
            templateUrl: "./template/" + Templates.Customer.CustomerProfiles, controller: function ($rootScope, $scope, $modal) {
                var TAG = Templates.Customer.CustomerProfiles;
                // 操作栏
                $scope.option = {
                    selected_type: 0,
                    selected_channel: "",
                    keyword: "",
                    we_chat: false,
                    no_phone_number: false,
                    no_marketing: false,
                    to_type: 0,
                    select_all: false
                };
                $scope.detail = {
                    selected_count: 0
                };
                $scope.channel = $rootScope.channel;
                $scope.type = ["VVIP", "vip", "常旅客", "董事", "流失"];
                // 表格数据
                $scope.data = {
                    count: 100,
                    list: [
                        {
                            guest_id: 1,
                            phone: "13111111111",
                            name: "习某某",
                            gender: 1,
                            guest_type: "vip",
                            birthday: "1992-02-15",
                            birthday_type: 0,
                            like: "吃辣",
                            dislike: "不吃香菜",
                            special_day: "",
                            personal_need: "",
                            status: 0,
                            desk_number: 10,
                            person_consumption: 400,
                            desk_per_month: 3.11,
                            last_consumption: "1993-02-25"
                        }
                    ]
                };
                // 事件处理
                $scope.query = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.member = function () {
                    Log.i(TAG, "会员价值设置");
                };
                $scope.filter = function (index) {
                    $scope.option.selected_type = index;
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.select = function () {
                    var count = 0;
                    $scope.data.forEach(function (item) {
                        if (item.selected) {
                            count++;
                        }
                    });
                    $scope.detail.selected_count = count;
                    $scope.option.select_all = count === $scope.data.list.length;
                    Log.i(TAG, JSON.stringify($scope.detail));
                };
                $scope.select_all = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    $scope.data.forEach(function (item) {
                        item.selected = $scope.option.select_all;
                    });
                    Log.i(TAG, JSON.stringify($scope.table));
                };
                $scope.move = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    $scope.data.forEach(function (item) {
                        if (item.selected) {
                            item.type = $scope.option.to_type;
                        }
                    });
                    Log.i(TAG, JSON.stringify($scope.table));
                };
                $scope.edit = function (guest) {
                    Log.i(TAG, JSON.stringify(guest));
                };
                // 对话框
                $scope.profiles_add = function () {
                    Log.i(TAG, "添加档案");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.AddCustomerProfiles,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                            $scope.form = {
                                token: "129ASDFIOJIO3RN23U12934INASDF",
                                phone: ["18813101211"],
                                name: "习某某",
                                gender: 1,
                                guest_type: "vip",
                                birthday: "1992-02-15",
                                birthday_type: 0,
                                disease: [],
                                like: ["吃辣"],
                                dislike: ["不吃香菜"],
                                special_day: "10-25",
                                personal_need: "生日宴"
                            };
                            $scope.submit = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                };
                $scope.profiles_import = function () {
                    Log.i(TAG, "批量导入档案");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.BatchImport,
                        controller: function ($scope) {
                            $scope.form = {
                                file: ""
                            };
                            $scope.import = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            };
                            $scope.export = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                };
                $scope.profiles_export = function () {
                    Log.i(TAG, "批量导出档案");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.BatchExport,
                        controller: function ($scope) {
                            $scope.form = {
                                by_time: {
                                    checked: true,
                                    interval: {from: "", to: ""}
                                },
                                by_amount: {
                                    checked: false,
                                    interval: {from: "", to: ""}
                                },
                                by_money: {
                                    checked: true,
                                    method: "total",
                                    interval: {from: "", to: ""}
                                },
                                by_channel: {
                                    checked: true
                                },
                                by_member_class: {
                                    checked: true,
                                    by: "rmf",
                                    selected: []
                                },
                                by_meal_period: {
                                    checked: true,
                                    period: "lunch"
                                },
                                by_gender: {
                                    checked: true,
                                    gender: "lunch"
                                }
                            };
                            $scope.channel = $rootScope.channel;
                            // 导出客户档案
                            $scope.export = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            };
                            // 导出全部客户档案
                            $scope.export_all = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                            }
                        }
                    });
                };
            }
        })
        .when('/Customer/CustomerRecycleBin', {
            templateUrl: "./template/" + Templates.Customer.CustomerRecycleBin, controller: function ($scope) {
                var TAG = Templates.Customer.CustomerRecycleBin;
                $scope.table = [];
                for (var i = 0; i < 7; i++) {
                    $scope.table.push({
                        name: "姓名", gender: "性别", phone: "手机", unit: "单位", cancel_rate: "撤单率",
                        last_meal_time: "最后就餐时间", type: "分类", channel: "维护渠道"
                    });
                }
            }
        })
        .when('/Customer/MemberValue', {
            templateUrl: "./template/" + Templates.Customer.MemberValue, controller: function ($scope) {

            }
        });

// 酒店管理
    $routeProvider
        .when('/Hotel/Branch', {
            templateUrl: "./template/" + Templates.Hotel.Branch, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Hotel.Branch;
                $scope.data = {count: 0, list: []};
                // var branch = {
                //     branch_id: 1,
                //     name: "北京宴总店",
                //     icon: "/static/css/image/head1.jpg",
                //     pictures: ["/static/css/image/head1.jpg", "/static/css/image/head1.jpg"],
                //     province: "北京市",
                //     city: "北京市",
                //     county: "丰台区",
                //     address: "靛厂路333号",
                //     facility: [],
                //     pay_card: [],
                //     phone: [],
                //     cuisine: {},
                //     hotel_name: "北京宴",
                //     manager_name: "陈总",
                //     create_time: "2017/07/04"
                // };
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
                $scope.addBranch = function () {
                    Log.i(TAG, "添加门店");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Hotel.Branch.BranchDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Hotel.Branch.BranchDialog;
                            Log.i(TAG, "添加门店");
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
                                var branch = {
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
                                return branch;
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
                $scope.editBranch = function (branch) {
                    Log.i(TAG, "编辑门店：" + branch.name);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Hotel.Branch.BranchDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.BranchDialog;
                            Log.i(TAG, "编辑门店：" + branch.name);
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
                            // 初始化支付方式
                            $scope.pay_card = "";
                            $scope.pay_cards = [
                                "支付宝", "微信", "VISA", "银联"
                            ];
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
                                branch.phone = [];
                                branch.facility = [];
                                branch.pay_card = [];
                                return branch;
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
            templateUrl: "./template/" + Templates.Hotel.Hotel, controller: function ($scope, $modal) {
                var TAG = Templates.Hotel.Hotel;
                $scope.form = {
                    hotel_id: 1,
                    // 餐厅名称
                    name: "北京宴总店",
                    // 餐厅标志
                    icon: "/static/css/image/head1.jpg",
                    // 详细地址
                    address: "丰台区靛厂路3号(永辉超市东侧)",
                    // 预订电话
                    phone: "01088177777",
                    // 餐厅设施
                    facility: [],
                    // 可以刷卡
                    VISA: false,
                    UnionPay: false,
                    // Logo
                    image: "/static/css/image/head2.jpg"
                };
                var url = "webApp/super_admin/hotel/profile/get/";
                $scope.submit = function () {
                    Log.i(TAG, "提交酒店信息：" + JSON.stringify($scope.form))
                }
            }
        });

// 订单管理
    $routeProvider
        .when('/Order/InsertOrder', {
            templateUrl: "./template/" + Templates.Order.InsertOrder, controller: function ($rootScope, $scope) {
                var TAG = Templates.Order.InsertOrder;// "#/Order/InsertOrder";
                $scope.option = {
                    date: "",
                    channel: "",
                    keyword: ""
                };
                $scope.order = [];
                for (var i = 0; i < 7; i++) {
                    $scope.order.push({value: i, title: "2017-06-19"});
                }
                $scope.channel = $rootScope.channel;
                $scope.table = [];
                for (i = 0; i < 10; i++) {
                    $scope.table.push({
                        id: i, name: "xxx", phone: "xxx", unit: "xxx", area: "xxx", desk: "xxx", count: 12,
                        meal_time: "2017-6-17 19:09:15", money: 18, operator: "xxx", channel: "xxx", status: "xxx"
                    });
                }
                $scope.search = function () {
                    Log.i(TAG, "保存" + JSON.stringify($scope.option));
                };
                $scope.save = function () {
                    Log.i(TAG, "保存" + JSON.stringify($scope.table));
                }
            }
        })
        .when('/Order/OperationLog', {
            templateUrl: "./template/" + Templates.Order.OperationLog, controller: function ($rootScope, $scope) {
                var TAG = Templates.Order.OperationLog;
                $scope.option = {
                    date_from: "2017/06/10",
                    date_to: "2017/06/09",
                    select_area: 1,
                    select_desk: 0,
                    select_channel: 1,
                    keyword: ""
                };
                $scope.staff = ["A", "B", "C", "D", "E", "F", "G"];
                $scope.area = $rootScope.area;
                $scope.desk = $scope.area[0].desk;
                $scope.table = [];
                for (var i = 0; i < 10; i++) {
                    $scope.table.push({
                        datetime: "6月13日 10:27:42", operator: "孙佳玥", operation: "预订单撤销",
                        content: "撤销时先生预订的2017-06-13午餐段518桌位", date: "6月13日", meal_type: "午餐",
                        time: "12:00", name: "时", gender: "先生", phone: "13501350028"
                    });
                }
                $scope.on_area_change = function () {
                    var index = $scope.option.select_area;
                    $scope.desk = $scope.area[index].desk;
                    $scope.option.select_desk = 1;
                };
                $scope.search = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                }
            }
        })
        .when('/Order/OrderHistory', {
            templateUrl: "./template/" + Templates.Order.OrderHistory, controller: function ($rootScope, $scope, $modal) {
                var TAG = Templates.Order.OrderHistory;
                // 操作栏
                $scope.option = {
                    date_from: "2017/06/10",
                    date_to: "2017/06/09",
                    select_area: 0,
                    select_desk: 0,
                    select_channel: 0,
                    keyword: ""
                };
                // 详细信息
                $scope.detail = {
                    order_count: 1,
                    customer_count: 2,
                    total: 3,
                    average: 4
                };
                $scope.area = $rootScope.area;
                $scope.desk = [];
                $scope.channel = $rootScope.channel;
                $scope.nav = ["有效订单", "撤单", "红包", "散客", "全部订单"];
                $scope.details = {order: 0, person: 0, total: 0, average: 0};
                // 表格数据
                $scope.table = [];
                for (var i = 0; i < 10; i++) {
                    $scope.table.push({
                        id: i, name: "王", gender: "先生", phone: "18050082265", order_time: "2017/6/23 19:04:48	",
                        meal_time: "06月08日晚餐18:00", order_channel: "预订台", area: "二楼", desk: "二楼", people: "6",
                        amount: "4135.00", order_status: "消费成功", operator: "张欢欢"
                    });
                }
                // 事件处理
                $scope.on_area_change = function () {
                    Log.i(TAG, "选择区域：" + $scope.option.select_area);
                    var url = "/webApp/admin/hotel_branch/desk/list/";
                    var param = {area_id: $scope.option.select_area};
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $scope.desk = obj.data;
                            $scope.option.select_desk = 1;
                        } else {
                            $scope.desk = {};
                            $scope.option.select_desk = 0;
                        }
                    });
                };
                $scope.query = function () {
                    Log.i(TAG, "查询订单数据：" + JSON.stringify($scope.option));
                };
                $scope.export = function () {
                    Log.i(TAG, "导出订单数据：" + JSON.stringify($scope.table));
                };
                $scope.filter = function (index) {
                    Log.i(TAG, "查看" + index + "：" + $scope.nav[index]);
                };
                $scope.sort = function (index) {
                    var tags = [
                        "客户姓名", "手机", "下单时间", "就餐时间", "接单渠道", "区域",
                        "桌位", "就餐人数", "消费金额", "订单状态", "操作人"
                    ];
                    Log.i(TAG, "根据 '" + tags[index] + "' 对列表排序");
                };
                // 对话框
                $scope.order_append = function () {
                    Log.i(TAG, "补录订单");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Order.OrderHistory.OrderAppend,
                        controller: function ($scope) {
                            var TAG = Dialog.Order.OrderHistory.OrderAppend;
                            Log.i(TAG, "对话框控制器");
                            $scope.order = {
                                // 电话
                                phone: "18800184976",
                                // 姓名
                                name: "赵强",
                                // 性别
                                gender: "female",
                                // 就餐人数
                                people: "12",
                                // 单位
                                unit: "创业谷",
                                // 接餐渠道
                                channel: 1,
                                // 定金
                                deposit: "12.0",
                                // 日期
                                date: "2017年6月21日",
                                // 餐段
                                meal_time: 1,
                                // 区域
                                desks: [
                                    {area: 0, desk: 2},
                                    {area: 1, desk: 2},
                                    {area: 2, desk: 2},
                                    {area: 3, desk: 2}
                                ]
                            };
                            // 接餐渠道
                            $scope.channel = $rootScope.channel;
                            $scope.date = [
                                "2017/6/6", "2017/6/7", "2017/6/8", "2017/6/9",
                                "2017/6/10", "2017/6/11", "2017/6/12", "2017/6/13"
                            ];
                            $scope.meals_time = ["午餐", "晚餐", "夜宵"];
                            $scope.areas = $rootScope.area;
                            $scope.desks = [];
                            $scope.removeDesk = function (desk) {
                                Log.i(TAG, "remove:" + index);
                                var index = $scope.order.desks.indexOf(desk);
                                $scope.order.desks.splice(index, 1);
                            };
                            $scope.addDesk = function () {
                                var item = {area: 1, desk: 1};
                                $scope.order.desks.push(item);
                                Log.i(TAG, "add desk:" + JSON.stringify(item));
                            };
                            $scope.submit = function () {
                                Log.i(TAG, JSON.stringify($scope.order));
                            };
                            $scope.cancel = function () {

                            }
                        }
                    });
                };
                $scope.order_details = function (index) {
                    Log.i(TAG, "订单详情：" + index);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Order.OrderHistory.OrderDetails,
                        controller: function ($scope) {
                            var TAG = Dialog.Order.OrderHistory.OrderDetails;
                            Log.i(TAG, "对话框控制器");
                            $scope.order = {
                                area: "三楼",
                                desk: "315",
                                name: "赵",
                                gender: "女士",
                                phone: "18800184976",
                                count: 6,
                                type: "未分类",
                                meal_time: "2017年6月7日 周三(晚餐) 14:57",
                                create_time: "2017年6月7日14:59",
                                operator: "赵强",
                                note: "给女朋友过生日，提前到店布置房间。",
                                images: ["IMG1", "IMG2", "IMG3", "IMG4", "IMG5"]
                            };
                            $scope.check = function (index) {
                                Log.i(TAG, "checked: " + JSON.stringify($scope.images[index]));
                            };
                            $scope.delete = function () {
                                Log.i(TAG, "delete images");
                            };
                            $scope.download = function () {
                                Log.i(TAG, "download images");
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, JSON.stringify($scope.order));
                                dlg.dismiss({code: "cancel"});
                            }
                        }
                    });
                }
            }
        })
        .when('/Order/OrderStatistics', {templateUrl: "./template/" + Templates.Order.OrderStatistics})
        .when('/Order/PhoneReserve', {
            templateUrl: "./template/" + Templates.Order.PhoneReserve, controller: function ($scope) {
                var TAG = Templates.Order.PhoneReserve;
                $scope.option = {
                    date_from: "",
                    date_to: "",
                    keyword: ""
                };
                $scope.table = [];
                for (var i = 0; i < 10; i++) {
                    $scope.table.push({
                        date: "2017-06-13", time: "14:24:15", phone: "100 0000 0000",
                        name: "凌乱了", status: "未处理"
                    });
                }
                $scope.pager = {
                    pagesize: 10
                };
                // TODO: 根据日期和关键字查找数据
                $scope.query = function () {
                    Log.i(TAG, "根据日期和关键字查找数据" + JSON.stringify($scope.option));
                };
            }
        })
        .when('/Order/ReserveNotice', {
            templateUrl: "./template/" + Templates.Order.ReserveNotice, controller: function ($rootScope, $scope, $modal) {
                var TAG = Templates.Order.ReserveNotice;
                // 操作栏
                $scope.option = {
                    date_from: "",
                    date_to: "",
                    select_area: 0,
                    select_channel: 0,
                    keyword: "18800184976",
                    daily_report: 0,
                    phone_mask: false,
                    desk_merge: true,
                    print_size: 0
                };
                $scope.detail = {
                    order_count: 0,
                    desk_count: 0,
                    customer_count: 0
                };
                $scope.area = $rootScope.area;
                $scope.channel = $rootScope.channel;
                $scope.daily_report = [
                    {value: 0, title: "2017-6-3报表"}, {value: 1, title: "2017-6-4报表"},
                    {value: 2, title: "2017-6-5报表"}, {value: 3, title: "2017-6-6报表"}
                ];
                $scope.print_size = [
                    "A4完整打印", "A4精简版打印", "58mm打印", "80mm打印"
                ];
                // 表格数据
                $scope.table = [];
                for (var i = 0; i < 10; i++) {
                    $scope.table.push({
                        id: i, meal_time: "06月08日晚餐18:00", area: "二楼", desk: "(CEIEC)215", name: "高", gender: "女士",
                        phone: "18510515888", count: "18", order_channel: "刘光艳", channel: "刘光艳",
                        order_time: "2017/6/8 10:57:33", type: "流失", unit: "单位", status: "已订", operator: "刘光艳"
                    });
                }
                // 事件处理
                $scope.query = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.export = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.print = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.sort = function (index) {
                    var tags = [
                        "就餐时间", "区域", "桌号", "姓名", "手机", "人数",
                        "接单渠道", "下单时间", "分类", "订单状态", "操作员",
                        "订单详情"
                    ];
                    Log.i(TAG, "根据 '" + tags[index] + "' 对列表排序");
                };
                $scope.today = function (index) {
                    var tags = [
                        "今日报表", "午餐", "晚餐", "已撤销订单", "散客订单"
                    ];
                    Log.i(TAG, "根据 '" + tags[index] + "' 过滤列表数据");
                };
                // 对话框
                $scope.order_details = function (index) {
                    Log.i(TAG, "订单详情：" + index);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Order.ReserveNotice.ReserveOrderDetails,
                        controller: function ($scope) {
                            var TAG = Dialog.Order.ReserveNotice.ReserveOrderDetails;
                            Log.i(TAG, "对话框控制器");
                            $scope.order = {
                                area: "三楼",
                                desk: "315",
                                name: "赵",
                                gender: "女士",
                                phone: "18800184976",
                                count: 6,
                                type: "未分类",
                                meal_time: "2017年6月7日 周三(晚餐) 14:57",
                                create_time: "2017年6月7日14:59",
                                operator: "赵强",
                                note: "给女朋友过生日，提前到店布置房间。",
                                images: ["IMG1", "IMG2", "IMG3", "IMG4", "IMG5"]
                            };
                            $scope.check = function (index) {
                                Log.i(TAG, "checked: " + JSON.stringify($scope.images[index]));
                            };
                            $scope.delete = function () {
                                Log.i(TAG, "delete images");
                            };
                            $scope.download = function () {
                                Log.i(TAG, "download images");
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, JSON.stringify($scope.order));
                                dlg.dismiss({code: "cancel"});
                            }
                        }
                    });
                }
            }
        });

// 预订管理
    $routeProvider
        .when('/Reserve/AreaDesk', {
            templateUrl: "./template/" + Templates.Reserve.AreaDesk, controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Reserve.AreaDesk;
                var index = 0;
                $scope.area = $rootScope.area;
                $scope.desk = {};
                $scope.pages = [1, 2, 3, 4, 5, 6, 7];
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
                $scope.Meals = {
                    hasLunch: false,
                    hasSupper: false,
                    hasDinner: false
                };
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
                $scope.save = function () {
                    // 修改餐段信息
                    var url = "/webApp/admin/hotel_branch/meal_period/modify/";
                    var param = {
                        branch_id: 1,
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
                $scope.data = $rootScope.area;
                // 保存门店区域列表
                $scope.save = function () {
                    // 【添加】【修改】【删除】区域的请求
                    var request = {
                        // 批量增加门店的餐厅区域
                        add: {
                            url: "/webApp/admin/hotel_branch/area/add/",
                            param: {
                                branch_id: 1,
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
                        branch_id: $rootScope.branch.branch_id,
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
                        branch_id: 1,
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
        });

// 评分审阅
    $routeProvider
        .when('/Review/Rank', {
            templateUrl: "./template/" + Templates.Review.Rank, controller: function ($scope) {
                var TAG = Templates.Review.Rank;
                var items = [
                    "门牌拍照", "沙盘", "欢迎屏", "氛围", "拍照", "烤瓷杯",
                    "小册子", "台历", "荣誉证书", "用心工作", "私人订制创新", "表扬信顾客满意度", "朋友圈顾客满意度", "网评顾客满意度"
                ];
                // 酒店排名
                // 房间排名
                // 宴会排名
                $scope.branches = [];
                for (var i = 0; i < 12; i++) {
                    var images = [];
                    for (var j = 0; j < 14; j++) {
                        var no = j % 9;
                        images.push({
                            id: j,
                            name: items[j],
                            url: "/static/css/image/head" + no + ".jpg",
                            score: j * 3
                        });
                    }
                    $scope.branches.push({
                        id: i,
                        name: "Branch" + i,
                        score: 12 + i,
                        images: images
                    });
                }
                $scope.edit = function (branch, image) {
                    Log.i(TAG, JSON.stringify($scope.branches[branch].images[image]));
                }
            }
        })
        .when('/Review/Tutorial', {templateUrl: "./template/" + Templates.Review.Tutorial});

// 智能订餐台
    $routeProvider
        .when('/SmartOrder/SmartOrder', {
            templateUrl: "./template/" + Templates.SmartOrder.SmartOrder, controller: function ($rootScope, $scope) {
                var TAG = Templates.SmartOrder.SmartOrder;
                $scope.weekdays = [
                    "周一", "周二", "周三", "周四", "周五", "周六"
                ];
                $scope.branch = $rootScope.branch;
                // 区域列表
                $scope.area = $rootScope.area;
                // 私人订制列表
                $scope.personal_tailor = angular.copy($rootScope.branch.personal_tailor);
                // 来电列表
                $scope.Phone = [];
                // 预约列表
                $scope.Reserve = [];
                // 订单列表
                $scope.Orders = [];
                // 分页导航、
                $scope.pages = [1, 2, 3, 4, 5, 6, 7, 8, 9];
                // 构造列表
                for (var i = 0; i < 5; i++) {
                    $scope.Phone.push({
                        id: i, time: "14:39", name: "赵强", gender: "male", phone: "18800184976", type: "活跃"
                    });
                    $scope.Reserve.push({
                        id: i, time: "14:39", name: "姜璐", gender: "female", phone: "18800184976", type: "流失"
                    });
                    $scope.Orders.push({
                        id: i, name: "赵强", gender: "male", phone: "18050082265", order_time: "2017/6/23 19:04:48",
                        meal_time: "06月08日晚餐18:00", order_channel: "预订台", area: "二楼", desk: "525", people: "6",
                        amount: "4135.00", order_status: "消费成功", operator: "张欢欢"
                    });
                }
                // 订单
                $scope.form = {
                    // 预定日期
                    dinner_date: "",
                    dinner_time: "",
                    dinner_period: "",
                    name: "",
                    contact: "",
                    guest_number: "",
                    desks: "",
                    banquet: "",
                    staff_description: ""
                };
                $scope.reserve = function () {
                    Log.i(TAG, "预定：" + JSON.stringify($scope.form));
                    var url = "/webApp/admin/order/submit/";
                    var param = $scope.form;
                };
                $scope.cancel = function () {

                };
                $scope.handlePhone = function (index) {
                    Log.i(TAG, JSON.stringify($scope.Phone[index]));
                };
                $scope.handleReserve = function (index) {
                    Log.i(TAG, JSON.stringify($scope.Reserve[index]));
                };
            }
        });


    $routeProvider
        .otherwise({redirectTo: "/SmartOrder/SmartOrder"});
}]);
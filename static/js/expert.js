/**
 * Created by 本山 on 2017/5/31.
 */

// 全局变量：记录所有固定的内容
BanquetExpert = {
    keu: "宴专家",
    en: {
        display: "显示"
    },
    zh_ch: {
        display: "Display"
    },
    hotel: {
        "hotel_id": 1,
        "name": "未登录",
        "icon": "/static/css/image/head1.jpg",
        "branches_count": 10,
        "owner_name": "杨秀荣",
        "create_time": "创建时间"
    },
    branch: ["门店1", "门店2", "门店3", "门店4", "门店5", "门店6"],
    selected_branch: 1,
    meals: {
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
    },
    area: [
        {
            value: 0, name: '一楼', order: 0, status: 1,
            seat: [
                {value: 0, name: '101', min: 1, max: 16, type: "大厅散台", order: 1, enable: false},
                {value: 1, name: '102', min: 1, max: 16, type: "豪华包间", order: 2, enable: true},
                {value: 2, name: '111', min: 1, max: 16, type: "大厅散台", order: 3, enable: false},
                {value: 3, name: '105', min: 1, max: 16, type: "豪华包间", order: 4, enable: true}
            ]
        },
        {
            value: 1, name: '二楼', order: 1, status: 0,
            seat: [
                {value: 0, name: '206', min: 5, max: 16, type: "大厅散台", order: 5, enable: true},
                {value: 1, name: '207', min: 5, max: 16, type: "豪华包间", order: 6, enable: false},
                {value: 2, name: '208', min: 5, max: 16, type: "大厅散台", order: 7, enable: true},
                {value: 3, name: '209', min: 5, max: 16, type: "大厅散台", order: 8, enable: false}
            ]
        },
        {
            value: 2, name: '三楼', order: 2, status: 0,
            seat: [
                {value: 0, name: '306', min: 8, max: 16, type: "豪华包间", order: 9, enable: true},
                {value: 1, name: '307', min: 8, max: 16, type: "大厅散台", order: 10, enable: false},
                {value: 2, name: '308', min: 8, max: 16, type: "豪华包间", order: 11, enable: true},
                {value: 3, name: '309', min: 8, max: 16, type: "大厅散台", order: 12, enable: false}
            ]
        },
        {
            value: 3, name: '五楼', order: 3, status: 1,
            seat: [
                {value: 0, name: '506', min: 12, max: 16, type: "豪华包间", order: 13, enable: true},
                {value: 1, name: '507', min: 12, max: 16, type: "豪华包间", order: 14, enable: false},
                {value: 2, name: '508', min: 12, max: 16, type: "豪华包间", order: 15, enable: false},
                {value: 3, name: '509', min: 12, max: 16, type: "豪华包间", order: 16, enable: true}
            ]
        }
    ],
    staff: [],
    channel: {
        inner: [
            {value: 1, name: 'A'},
            {value: 2, name: 'B'},
            {value: 3, name: 'C'},
            {value: 4, name: 'D'}
        ],
        outer: [
            {value: 5, name: 'E'},
            {value: 6, name: 'F'},
            {value: 7, name: 'G'},
            {value: 8, name: 'H'}
        ]
    },
    menus: [
        {
            title: "超级管理后台",
            menu_id: "SuperAdmin",
            item: [
                {title: "超级管理后台", item_id: "SuperAdmin"}
            ]
        },
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
            "title": "智能订餐台",
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
                {title: "自动推荐桌位", item_id: "SeatRecommend"}
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
    ],
    Breadcrumb: [
        {title: "主页"},
        {title: "预订管理"},
        {title: "餐段设置"}
    ]
};

// 获取员工列表
for (var i = 0; i < 36; i++) {
    BanquetExpert.staff.push({
        id: i,
        name: "赵强",
        gender: "female",
        phone: "1000000000",
        job: "无业游民",
        username: "赵XX",
        password: "",
        status: i % 3
    });
}

// 子页面模板
Templates = {
    // 路径导航
    Breadcrumb: "Drawer/Breadcrumb.html",
    // 超级管理后台
    SuperAdmin: {
        SuperAdmin: "SuperAdmin/SuperAdmin.html" // 超级管理后台
    },
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
        SeatRecommend: "Reserve/SeatRecommend.html"// 自动推荐桌位
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
    SuperAdmin: {
        SuperAdmin: {
            HotelDialog: "SuperAdmin/SuperAdmin/HotelDialog.html"
        }
    },
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

$.post({
    url: "/webApp/admin/hotel/profile/get/",
    data: JSON.stringify({}),
    success: function (data) {
        var obj = eval(data);
        // Log.i("expert.js", data);
        // Log.i("expert.js", JSON.stringify(data));
        BanquetExpert.hotel = data.data;
    },
    fail: function (error) {
        Log.i("expert.js", JSON.stringify(error));
        location.href = "login.html";
    }
});

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

// 侧边导航栏控制器
BanquetExpertApp.controller('drawerCtrl', function ($scope) {
    $scope.hotel = BanquetExpert.hotel;
    $scope.menus = BanquetExpert.menus;
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
            templateUrl: "./template/" + Templates.Channel.Channel, controller: function ($scope, $modal) {
                var TAG = Templates.Channel.Channel;
                $scope.staffs = BanquetExpert.staff;
                // 高层管理
                $scope.manager = [];
                for (var i = 0; i < 12; i++) {
                    $scope.manager.push({
                        // ID
                        id: i,
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
                    });
                }
                // 预订员和迎宾
                $scope.reserve = [];
                for (i = 0; i < 12; i++) {
                    $scope.reserve.push({
                        // ID
                        id: i,
                        // 操作
                        option: "edit",
                        // 姓名
                        name: "梅本山",
                        // 性别
                        gender: "male",
                        // 电话
                        phone: "18800184976",
                        // 职位
                        job: "董事长",
                        // 用户名
                        username: "mbs0221",
                        // 密码
                        password: "mbs0221",
                        // 职能权限
                        privilege: {
                            // 管理职能
                            manage: {}
                            ,
                            // 营销职能
                            marketing: {}
                            ,
                            // 预定职能
                            reserve: {}
                            ,
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
                            all_seat: false,
                            // 桌位信息
                            area: BanquetExpert.area
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
                    });
                }
                // 渠道
                $scope.channel = BanquetExpert.channel;
                for (i = 0; i < 12; i++) {
                    $scope.channel.outer.push({
                        // ID
                        id: i,
                        // 渠道名称
                        channel: "118114",
                        // 直属上级
                        parent: 1,
                        // 签约折扣标准
                        discount: 2,
                        // 合作周期
                        date_from: "2017/06/27",
                        date_to: "2017/06/27",
                        // 佣金核算方式
                        bonus: {
                            method: 1,
                            value: 12
                        }
                    });
                }
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
                                    all_seat: false,
                                    // 桌位信息
                                    area: BanquetExpert.area
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
                            $scope.area = BanquetExpert.area;
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
                            $scope.area = BanquetExpert.area;
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
                                    // 渠道名称
                                    channel: "118114",
                                    // 直属上级
                                    parent: 1,
                                    // 签约折扣标准
                                    discount: 2,
                                    // 合作周期
                                    date_from: "2017/06/27",
                                    date_to: "2017/06/27",
                                    // 佣金核算方式
                                    bonus: {
                                        method: 1,
                                        value: 12
                                    }
                                };
                                return channel;
                            }
                        },
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Channel.ExternalChannelDialog;
                            Log.i(TAG, "对话框控制器");
                            $scope.option = "新增";
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
            templateUrl: "./template/" + Templates.Channel.Staff, controller: function ($scope, $modal, $http) {
                var TAG = Templates.Channel.Staff;
                // 员工列表
                $scope.data = {
                    "count": 20,
                    "list": [{
                        "staff_id": 1,
                        "staff_number": "12345",
                        "name": "张三",
                        "icon": "头像地址",
                        "gender": 0,
                        "hotel_name": "北京宴",
                        "position": "经理",
                        "guest_channel": 1,
                        "authority": "权限",
                        "create_time": "创建时间"
                    }]
                };
                var url = "/webApp/admin/hotel/staff/list/";
                var param = {
                    hotel_id: BanquetExpert.hotel.hotel_id,
                    status: 1
                };
                $http.post(url, JSON.stringify(param)).success(function (obj) {
                    if (obj.status === "true") {
                        $scope.data = obj.data;
                    } else {
                        alert(obj.description);
                    }
                });
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
                        controller: function ($scope) {
                            var TAG = Dialog.Channel.Staff.EditStaff;
                            Log.i(TAG, "添加员工控制器");
                            $scope.option = "添加";
                            $scope.form = {
                                name: "赵强",
                                gender: "female",
                                phone: "1000000000",
                                job: "无业游民",
                                username: "赵XX",
                                password: "",
                                status: 1
                            };
                            $scope.submit = function () {
                                Log.i(TAG, "提交员工信息：" + $scope.form);
                                dlg.close($scope.form);
                            };
                            $scope.exit = function () {
                                Log.i(TAG, "员工离岗");
                            };
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
                        $scope.staff.push(result);
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
            templateUrl: "./template/" + Templates.Customer.CustomerProfiles, controller: function ($scope, $modal) {
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
                $scope.channel = BanquetExpert.channel;
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
                                phone: "18813101211",
                                name: "习某某",
                                gender: 1,
                                guest_type: "vip",
                                birthday: "1992-02-15",
                                birthday_type: 0,
                                like: "吃辣",
                                dislike: "不吃香菜",
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
                            $scope.channel = BanquetExpert.channel;
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
            templateUrl: "./template/" + Templates.Hotel.Branch, controller: function ($scope, $modal, $http) {
                var TAG = Templates.Hotel.Branch;
                $scope.data = {
                    count: 20,
                    list: [{
                        branch_id: 1,
                        name: "北京宴总店",
                        icon: "/static/css/image/head1.jpg",
                        pictures: ["picture1", "picture2"],
                        province: "北京市",
                        city: "北京市",
                        county: "丰台区",
                        address: "靛厂路333号",
                        facility: ["停车场", "吸烟区"],
                        pay_card: ["支付宝", "微信"],
                        phone: ["13051391335", "13188888888"],
                        cuisine: {},
                        hotel_name: "北京宴",
                        manager_name: "陈总",
                        create_time: "创建时间"
                    }]
                };
                var url = "/webApp/admin/hotel_branch/list/";
                var param = {
                    hotel_id: BanquetExpert.hotel.hotel_id
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
                            $scope.option = "添加";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑门店信息");
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存门店信息");
                                dlg.close(id);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消保存");
                            }
                        },
                        resolve: {
                            form: function () {
                                var branch = {
                                    name: "北京宴总店",
                                    icon: "http://oss.aliyun/banquet/avatar/1.jpg",
                                    pictures: "[picture1, picture2, ...]",
                                    province: "北京市",
                                    city: "北京市",
                                    county: "丰台区",
                                    address: "北京市丰台区靛厂路333号",
                                    meal_period: {
                                        Monday: {
                                            lunch: {from: "8:30", to: "12:00"},
                                            dinner: {from: "12:00", to: "18:00"},
                                            supper: {from: "18:00", to: "24:00"}
                                        },
                                        TuesDay: {
                                            lunch: {from: "8:30", to: "12:00"},
                                            dinner: {from: "12:00", to: "18:00"},
                                            supper: {from: "18:00", to: "24:00"}
                                        }
                                    },
                                    facility: ["停车场", "吸烟区"],
                                    pay_card: ["银联", "支付宝"],
                                    phone: ["13011111111", "13100000000"],
                                    cuisine: {
                                        "北京菜": ["烤鸭", "京酱肉丝"],
                                        "浙江菜": ["鸡"]
                                    },
                                    hotel_name: "北京宴",
                                    manager_name: "陈奎义",
                                    create_time: "创建时间"
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
                    }, function (reason) {
                        Log.i(TAG, reason);
                    });
                };
                $scope.editBranch = function (branch) {
                    Log.i(TAG, "编辑门店：" + branch.name);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Hotel.Branch.BranchDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.EditStaff;
                            Log.i(TAG, "编辑门店：" + branch.name);
                            $scope.option = "编辑";
                            $scope.form = form;
                            $scope.edit = function () {
                                Log.i(TAG, "编辑门店信息：" + $scope.form);
                            };
                            $scope.save = function () {
                                Log.i(TAG, "保存门店信息");
                                dlg.close(id);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, "取消保存");
                            }
                        },
                        resolve: {
                            form: function () {
                                return branch;
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
            templateUrl: "./template/" + Templates.Order.InsertOrder, controller: function ($scope) {
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
                $scope.channel = BanquetExpert.channel;
                $scope.table = [];
                for (i = 0; i < 10; i++) {
                    $scope.table.push({
                        id: i, name: "xxx", phone: "xxx", unit: "xxx", area: "xxx", seat: "xxx", count: 12,
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
            templateUrl: "./template/" + Templates.Order.OperationLog, controller: function ($scope) {
                var TAG = Templates.Order.OperationLog;
                $scope.option = {
                    date_from: "2017/06/10",
                    date_to: "2017/06/09",
                    select_area: 1,
                    select_seat: 0,
                    select_channel: 1,
                    keyword: ""
                };
                $scope.staff = ["A", "B", "C", "D", "E", "F", "G"];
                $scope.area = BanquetExpert.area;
                $scope.seat = $scope.area[0].seat;
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
                    $scope.seat = $scope.area[index].seat;
                    $scope.option.select_seat = 1;
                };
                $scope.search = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                }
            }
        })
        .when('/Order/OrderHistory', {
            templateUrl: "./template/" + Templates.Order.OrderHistory, controller: function ($scope, $modal) {
                var TAG = Templates.Order.OrderHistory;
                // 操作栏
                $scope.option = {
                    date_from: "2017/06/10",
                    date_to: "2017/06/09",
                    select_area: 0,
                    select_seat: 0,
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
                $scope.area = BanquetExpert.area;
                $scope.seat = [];
                $scope.channel = BanquetExpert.channel;
                $scope.nav = ["有效订单", "撤单", "红包", "散客", "全部订单"];
                $scope.details = {order: 10, person: 12, total: 10, average: 10};
                // 表格数据
                $scope.table = [];
                for (var i = 0; i < 10; i++) {
                    $scope.table.push({
                        id: i, name: "王", gender: "先生", phone: "18050082265", order_time: "2017/6/23 19:04:48	",
                        meal_time: "06月08日晚餐18:00", order_channel: "预订台", area: "二楼", seat: "二楼", people: "6",
                        amount: "4135.00", order_status: "消费成功", operator: "张欢欢"
                    });
                }
                // 事件处理
                $scope.on_area_change = function () {
                    var index = $scope.option.select_area;
                    $scope.seat = $scope.area[index].seat;
                    $scope.option.select_seat = 1;
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
                                seats: [
                                    {area: 0, seat: 2},
                                    {area: 1, seat: 2},
                                    {area: 2, seat: 2},
                                    {area: 3, seat: 2}
                                ]
                            };
                            // 接餐渠道
                            $scope.channel = BanquetExpert.channel;
                            $scope.date = [
                                "2017/6/6", "2017/6/7", "2017/6/8", "2017/6/9",
                                "2017/6/10", "2017/6/11", "2017/6/12", "2017/6/13"
                            ];
                            $scope.meals_time = ["午餐", "晚餐", "夜宵"];
                            $scope.areas = BanquetExpert.area;
                            $scope.seats = [];
                            $scope.removeSeat = function (seat) {
                                Log.i(TAG, "remove:" + index);
                                var index = $scope.order.seats.indexOf(seat);
                                $scope.order.seats.splice(index, 1);
                            };
                            $scope.addSeat = function () {
                                var item = {area: 1, seat: 1};
                                $scope.order.seats.push(item);
                                Log.i(TAG, "add seat:" + JSON.stringify(item));
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
                                seat: "315",
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
            templateUrl: "./template/" + Templates.Order.ReserveNotice, controller: function ($scope, $modal) {
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
                    seat_marge: true,
                    print_size: 0
                };
                $scope.detail = {
                    order_count: 0,
                    seat_count: 0,
                    customer_count: 0
                };
                $scope.area = BanquetExpert.area;
                $scope.channel = BanquetExpert.channel;
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
                        id: i, meal_time: "06月08日晚餐18:00", area: "二楼", seat: "(CEIEC)215", name: "高", gender: "女士",
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
                                seat: "315",
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
            templateUrl: "./template/" + Templates.Reserve.AreaDesk, controller: function ($scope, $http) {
                var TAG = Templates.Reserve.AreaDesk;
                var index = 0;
                // $http.get(url).success(function (response) {
                //     $scope.area = response.data;
                // });
                $scope.area = BanquetExpert.area;
                $scope.seat = BanquetExpert.area[index].seat;
                $scope.pages = [1, 2, 3, 4, 5, 6, 7];
                // TODO: 添加桌位
                $scope.add_seat = function () {
                    var obj = {
                        value: $scope.seat.length, name: '桌位' + $scope.seat.length,
                        min: 12, max: 16, type: "大厅散台", order: $scope.seat.length, enable: true
                    };
                    Log.i(TAG, "添加桌位：" + JSON.stringify(obj));
                    $scope.seat.push(obj);
                };
                // TODO: 保存区域桌位信息
                $scope.save = function () {
                    Log.i(TAG, "保存区域桌位信息：" + JSON.stringify(BanquetExpert.area));
                };
                $scope.nav = function (area_id) {
                    index = area_id;
                    Log.i(TAG, "选择区域：" + area_id);
                    $scope.seat = BanquetExpert.area[area_id].seat;
                };
                $scope.edit = function (desk_id) {
                    Log.i("修改桌位：" + desk_id);
                };
            }
        })
        .when('/Reserve/MealsTime', {
            templateUrl: "./template/" + Templates.Reserve.MealsTime, controller: function ($scope) {
                var TAG = Templates.Reserve.MealsTime;
                $scope.MealsTime = {
                    Lunch: BanquetExpert.meals.lunch,
                    Dinner: BanquetExpert.meals.dinner,
                    Supper: BanquetExpert.meals.supper,
                    hasLunch: false,
                    hasDinner: false,
                    hasSupper: true,
                    Week: ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"],
                    EnWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    Table: [
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        }
                    ]
                };
                $scope.save = function () {
                    Log.i(TAG, JSON.stringify({
                        hasLunch: $scope.MealsTime.hasLunch,
                        hasDinner: $scope.MealsTime.hasDinner,
                        hasSupper: $scope.MealsTime.hasSupper,
                        Table: $scope.MealsTime.Table
                    }));
                };
            }
        })
        .when('/Reserve/MealsArea', {
            templateUrl: "./template/" + Templates.Reserve.MealsArea, controller: function ($scope) {
                var TAG = Templates.Reserve.MealsArea;
                $scope.area = BanquetExpert.area;
                $scope.sync_area = function () {
                    Log.i(TAG, "同步区域列表");
                };
                $scope.add_area = function () {
                    var obj = {value: 0, name: '区域' + $scope.area.length, order: $scope.area.length, status: 1, seat: []};
                    Log.i(TAG, "添加区域：" + JSON.stringify(obj));
                    BanquetExpert.area.push(obj);
                };
                $scope.save = function () {
                    Log.i(TAG, "保存：" + JSON.stringify(BanquetExpert.area));
                };
            }
        })
        .when('/Reserve/SeatRecommend', {
            templateUrl: "./template/" + Templates.Reserve.SeatRecommend, controller: function ($scope, $http) {
                var TAG = Templates.Reserve.SeatRecommend;
                var seats = [];
                $.each(BanquetExpert.area, function (index, area) {
                    $.each(area.seat, function (index, seat) {
                        seat.area = area.name;
                        seats.push(seat);
                    });
                });
                $scope.seats = seats;
                $scope.numbers = [];
                for (var i = 0; i < 16; i++) {
                    $scope.numbers.push({value: i});
                }
                $scope.selected_count = 1;
                $scope.pages = [1, 2, 3, 4, 5, 6, 7];
                $scope.change = function (selectCount) {
                    Log.i(TAG, "选择了：" + selectCount);
                    $scope.seats = seats.filter(function (item) {
                        return item.min <= $scope.selected_count && item.max >= $scope.selected_count;
                    });
                };
                $scope.save = function () {
                    Log.i(TAG, JSON.stringify($scope.seats));
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
            templateUrl: "./template/" + Templates.SmartOrder.SmartOrder, controller: function ($scope) {
                var TAG = Templates.SmartOrder.SmartOrder;
                $scope.weekdays = [
                    "周一", "周二", "周三", "周四", "周五", "周六"
                ];
                // 区域列表
                $scope.area = BanquetExpert.area;
                // 来电列表
                $scope.phone = [];
                // 预约列表
                $scope.reserve = [];
                // 订单列表
                $scope.orders = [];
                // 分页导航、
                $scope.pages = [1, 2, 3, 4, 5, 6, 7, 8, 9];
                // 构造列表
                for (var i = 0; i < 5; i++) {
                    $scope.phone.push({
                        id: i, time: "14:39", name: "赵强", gender: "male", phone: "18800184976", type: "活跃"
                    });
                    $scope.reserve.push({
                        id: i, time: "14:39", name: "姜璐", gender: "female", phone: "18800184976", type: "流失"
                    });
                    $scope.orders.push({
                        id: i, name: "赵强", gender: "male", phone: "18050082265", order_time: "2017/6/23 19:04:48",
                        meal_time: "06月08日晚餐18:00", order_channel: "预订台", area: "二楼", seat: "525", people: "6",
                        amount: "4135.00", order_status: "消费成功", operator: "张欢欢"
                    });
                }
                $scope.handlePhone = function (index) {
                    Log.i(TAG, JSON.stringify($scope.phone[index]));
                };
                $scope.handleReserve = function (index) {
                    Log.i(TAG, JSON.stringify($scope.reserve[index]));
                };
            }
        });

    // 超级管理员
    $routeProvider
        .when('/SuperAdmin/SuperAdmin', {
            templateUrl: "./template/" + Templates.SuperAdmin.SuperAdmin, controller: function ($scope, $modal, $http) {
                var TAG = Templates.SuperAdmin.SuperAdmin;
                // 酒店列表
                $scope.data = {count: 0, list: []};
                // 获取酒店列表
                var url = "/webApp/super_admin/hotel/list/";
                $http.post(url, JSON.stringify({})).success(function (obj) {
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
                        templateUrl: "./template/" + Dialog.SuperAdmin.SuperAdmin.HotelDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.SuperAdmin.SuperAdmin.HotelDialog;
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
                                    // token: "129ASDFIOJIO3RN23U12934INASDF",
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
                        templateUrl: "./template/" + Dialog.SuperAdmin.SuperAdmin.HotelDialog,
                        controller: function ($scope, form) {
                            var TAG = Dialog.Channel.Staff.EditStaff;
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
            }
        });

    $routeProvider
        .otherwise({redirectTo: "/SmartOrder/SmartOrder"});
}]);
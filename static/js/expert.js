/**
 * Created by 本山 on 2017/5/31.
 */
/**
 * 全局变量：记录所有固定的内容
 *
 *
 */
BanquetExpert = {
    keu: "宴专家",
    en: {
        display: "显示"
    },
    zh_ch: {
        display: "Display"
    },
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
    staff: [
        {value: 0, name: 'aaa'},
        {value: 0, name: 'bbb'}
    ],
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
            {value: 8, name: 'H'},
            {value: 9, name: 'I'}
        ]
    },
    menus: [
        {
            title: "后台用户管理",
            menu_id: "Channel",
            item: [
                {title: "获客渠道", item_id: "Channel"},
                {title: "用户权限管理", item_id: "Privilege"}
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

$.get({
    url: "/webApp/admin/hotel/profile/",
    data: {
        token: window.Login.token
    },
    success: function (data) {
        console.log(window.Login.token);
        BanquetExpert.data = eval(data);
    }
});

// 子页面模板
Templates = {
    Breadcrumb: "Drawer/Breadcrumb.html", // 路径导航
    // 后台用户管理
    Channel: {
        Channel: "Channel/Channel.html", // 获客渠道*** AddManager AddOuterChannel AddReserve
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
    // 评分审阅
    Review: {
        Rank: "Review/Rank.html", // 餐厅排名
        Tutorial: "Review/Tutorial.html"// 中国服务私人订制标准视频教程
    }
};

// 对话框模板
Dialog = {
    Channel: {
        Channel: {
            AddManager: "Channel/Channel/AddManager.html",
            AddOuterChannel: "Channel/Channel/AddOuterChannel.html",
            AddReserve: "Channel/Channel/AddReserve.html"
        }
    },
    Customer: {
        CustomerProfiles: {
            AddCustomerProfiles: "Customer/CustomerProfiles/AddCustomerProfiles.html",
            BatchExport: "Customer/CustomerProfiles/BatchExport.html",
            BatchImport: "Customer/CustomerProfiles/BatchImport.html"
        }
    },
    Order: {
        OrderHistory: {
            OrderAppend: "Order/OrderHistory/OrderAppend",
            OrderDetails: "Order/OrderHistory/OrderDetails"
        },
        ReserveNotice: {
            ReserveOrderDetails: "Order/ReserveNotice/ReserveOrderDetails.html"
        }
    }
};

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

$(document).ready(function () {

    // 查找子节点
    // var find = function (obj, key, value) {
    //     var newObj = false;
    //     $.each(obj, function () {
    //         var testObj = this;
    //         $.each(testObj, function (k, v) {
    //             if (k === key && value === v) {
    //                 newObj = testObj;
    //             }
    //         });
    //     });
    //     return newObj;
    // };
    //
    // 刷新路径导航
    // var refreshBreadcrumb = function (path) {
    //     var string = path.substr(0, path.length - 5);
    //     var items = string.split('/');
    //     var menu = find(BanquetExpert.menus, 'menu_id', items[0]);
    //     var item = find(menu.item, 'item_id', items[1]);
    //     while (BanquetExpert.Breadcrumb.length > 1) {
    //         $.observable(BanquetExpert.Breadcrumb).remove();
    //     }
    //     $.observable(BanquetExpert.Breadcrumb).insert({title: menu.title});
    //     $.observable(BanquetExpert.Breadcrumb).insert({title: item.title});
    // };

});

var BanquetExpertApp = angular.module('BanquetExpertApp', ['ngRoute', 'ui.bootstrap']);
BanquetExpertApp.controller('drawerCtrl', function ($scope) {
    $scope.menus = BanquetExpert.menus;
});
BanquetExpertApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
    // 账户管理
        .when('/Account/AccountManage', {
            templateUrl: "./template/" + Templates.Account.AccountManage, controller: function ($scope) {

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
        .when('/Account/Restaurant', {templateUrl: "./template/" + Templates.Account.Restaurant})
        // 渠道管理
        .when('/Channel/Channel', {
            templateUrl: "./template/" + Templates.Channel.Channel, controller: function ($scope, $modal) {
                var TAG = Templates.Channel.Channel;
                // 对话框
                $scope.add_reserve = function () {
                    Log.i(TAG, "新增预订员和迎宾");
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.AddReserve,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                };
                $scope.add_manager = function () {
                    Log.i(TAG, "新增客户经理");
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.AddManager,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                };
                $scope.add_outer_channel = function () {
                    Log.i(TAG, "新增外部渠道");
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Channel.Channel.AddOuterChannel,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                };
            }
        })
        .when('/Channel/Privilege', {templateUrl: "./template/" + Templates.Channel.Privilege})
        // 客户管理
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
        .when('/Customer/CustomerAnalysis', {templateUrl: "./template/" + Templates.Customer.CustomerAnalysis})
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
                $scope.type = ["VVIP", "VIP", "常旅客", "董事", "流失"];
                // 表格数据
                $scope.table = [];
                for (var i = 0; i < 7; i++) {
                    $scope.table.push({
                        name: "南", gender: "先生", phone: "15811111881", unit: "无", cancel_rate: "53.51%",
                        credit: "1.2", order_count: "867", consumption: "2387457.00", last_meal_date: "2017年04月08日",
                        type: 0, rfm_type: "沉睡", channel: "王唯唯", marketing_sms: false, selected: false
                    });
                }
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
                    $scope.table.forEach(function (item) {
                        if (item.selected) {
                            count++;
                        }
                    });
                    $scope.detail.selected_count = count;
                    $scope.option.select_all = count === $scope.table.length;
                    Log.i(TAG, JSON.stringify($scope.detail));
                };
                $scope.select_all = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    $scope.table.forEach(function (item) {
                        item.selected = $scope.option.select_all;
                    });
                    Log.i(TAG, JSON.stringify($scope.table));
                };
                $scope.move = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    $scope.table.forEach(function (item) {
                        if (item.selected) {
                            item.type = $scope.option.to_type;
                        }
                    });
                    Log.i(TAG, JSON.stringify($scope.table));
                }
                // 对话框
                $scope.profiles_add = function () {
                    Log.i(TAG, "添加档案");
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.AddCustomerProfiles,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                };
                $scope.profiles_import = function () {
                    Log.i(TAG, "批量导入档案");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.BatchImport,
                        controller: function ($scope) {

                        }
                    });
                };
                $scope.profiles_export = function () {
                    Log.i(TAG, "批量导出档案");
                    $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.BatchExport,
                        controller: function ($scope) {

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
        .when('/Customer/MemberValue', {templateUrl: "./template/" + Templates.Customer.MemberValue})
        // 订单管理
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
                        id: i, meal_time: "06月08日晚餐18:00", area: "二楼", seat: "(CEIEC)215", name: "高", gender: "女士",
                        phone: "18510515888", count: "18", order_channel: "刘光艳", order_time: "2017/6/8 10:57:33",
                        type: "流失", status: "已订", operator: "刘光艳", detail: "...."
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
                // 对话框
                $scope.order_append = function () {
                    Log.i(TAG, "补录订单");
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Order.OrderHistory.OrderAppend,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                };
                $scope.order_details = function () {
                    Log.i(TAG, "订单详情");
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Order.OrderHistory.OrderDetails,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
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
                $scope.order_details = function (id) {
                    Log.i(TAG, "订单详情：" + id);
                    var modalInstance = $modal.open({
                        templateUrl: "./template/" + Dialog.Order.ReserveNotice.ReserveOrderDetails,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                        }
                    });
                    modalInstance.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                }
            }
        })
        // 预订管理
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
                var MealsTime = {
                    Lunch: BanquetExpert.meals.lunch,
                    Dinner: BanquetExpert.meals.dinner,
                    Supper: BanquetExpert.meals.supper,
                    Table: [
                        {
                            dayofweek: "星期一",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            dayofweek: "星期二",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            dayofweek: "星期三",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            dayofweek: "星期四",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            dayofweek: "星期五",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            dayofweek: "星期六",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        },
                        {
                            dayofweek: "星期天",
                            lunch: {from: "08:30", to: "11:30"},
                            dinner: {from: "15:00", to: "23:45"},
                            supper: {from: "22:00", to: "04:00"}
                        }
                    ]
                };
                $scope.save = function () {
                    Log.i(TAG, JSON.stringify(MealsTime.Table));
                };
                $scope.MealsTime = MealsTime;
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
                // 路由设置
                // var routes = {
                //     "/Reserve/MealsArea/SetSeat/:seat_id": function (seat_id) {
                //         Log.i(TAG, "设置桌位：" + seat_id);
                //     }
                // };
                // var router = window.Router(routes);
                // router.init();
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
        })
        // 评分审阅
        .when('/Review/Rank', {templateUrl: "./template/" + Templates.Review.Rank})
        .when('/Review/Tutorial', {templateUrl: "./template/" + Templates.Review.Tutorial})
        // 智能订餐台
        .when('/SmartOrder/SmartOrder', {templateUrl: "./template/" + Templates.SmartOrder.SmartOrder})
        .otherwise({redirectTo: "/"});
}]);

angular.bootstrap($("#main"), ['BanquetExpertApp']);
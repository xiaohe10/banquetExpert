/**
 * Created by 本山 on 2017/7/7.
 */

// 子页面模板
Templates = {
    // 路径导航
    Breadcrumb: "Drawer/Breadcrumb.html",
    // 智能订餐台
    SmartOrder: {
        SmartOrder: "SmartOrder/SmartOrder.html"// 智能订餐台
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
    // 评分审阅
    Review: {
        Rank: "Review/Rank.html", // 餐厅排名
        Tutorial: "Review/Tutorial.html"// 中国服务私人订制标准视频教程
    }
};

// 对话框模板
Dialog = {
    // 订单管理
    Order: {
        OrderHistory: {
            OrderAppend: "Order/OrderHistory/OrderAppend.html",
            OrderDetails: "Order/OrderHistory/OrderDetails.html"
        },
        ReserveNotice: {
            ReserveOrderDetails: "Order/ReserveNotice/ReserveOrderDetails.html"
        }
    },
    // 客户管理
    Customer: {
        CustomerProfiles: {
            AddCustomerProfiles: "Customer/CustomerProfiles/AddCustomerProfiles.html",
            BatchExport: "Customer/CustomerProfiles/BatchExport.html",
            BatchImport: "Customer/CustomerProfiles/BatchImport.html"
        }
    }
};

// 自定义日志工具
var Log = {
    i: function (tag, msg) {
        console.log("BanquetExpertStaff: " + tag + ": " + msg);
    },
    w: function (tag, msg) {
        console.warn("BanquetExpertStaff: " + tag + ": " + msg);
    },
    e: function (tag, msg) {
        console.error("BanquetExpertStaff: " + tag + ": " + msg);
    },
    d: function (tag, msg) {
        console.debug("BanquetExpertStaff: " + tag + ": " + msg);
    }
};

var StaffApp = angular.module('StaffApp', [
    'ngRoute',
    'ui.bootstrap'
]);

// 过滤器定义
StaffApp.filter('gender', function () {
    return function (gender) {
        var TAG = ["保密", "先生", "女士"];
        return TAG[gender];
    }
});
StaffApp.filter('surname', function () {
    return function (name) {
        return name.charAt(0);
    }
});
StaffApp.filter('birthday_type', function () {
    return function (birthday_type) {
        var TAG = ["阳历", "农历"];
        return TAG[birthday_type];
    }
});
StaffApp.filter('discount', function () {
    return function (discount) {
        var TAG = ["无折扣", "9.5折", "9.0折", "8.5折", "8.0折"];
        return TAG[discount];
    }
});
StaffApp.filter('status', function () {
    return function (status) {
        var TAG = ["活跃", "沉睡", "流失", "无订单"];
        return TAG[status];
    }
});
StaffApp.filter("channel", function () {
    return function (channel) {
        var TAG = ["无", "高层管理", "预定员和迎宾", "客户经理"];
        return TAG[channel];
    }
});
StaffApp.filter("dinner_period", function () {
    return function (dinner_period) {
        var TAG = ['午餐', '晚餐', '夜宵'];
        return TAG[dinner_period];
    }
});
StaffApp.filter("status", function () {
    return function (order_status) {
        var TAG = ["已订", "客到", "已完成", "已撤单"];
        return TAG[order_status];
    }
});

// 侧边导航栏控制器
StaffApp.controller('drawerCtrl', function ($routeParams, $rootScope, $scope, $http, $location) {

    var TAG = "drawerCtrl";
    
    // 酒店信息
    $rootScope.Hotel = {
        hotel_id: -1,
        name: "未登录",
        icon: "/static/css/image/head1.jpg",
        mage: "http://fs.kebide.com/2016/07/12/eed874b7ac2b4f04b6d6d735f49dc373.jpg",
        branches_count: 10,
        owner_name: "杨秀荣",
        create_time: "创建时间"
    };
    // 门店信息
    $rootScope.branch = {
        branch_id: -1,
        name: "预订台"
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
    // 侧边栏
    $scope.menus = [
        {
            title: "未登录",
            menu_id: "Login",
            item: []
        }
    ];
    // 路径导航
    $scope.Breadcrumb = [
        {title: "主页"},
        {title: "预订管理"},
        {title: "餐段设置"}
    ];

    // 【酒店】获取酒店信息
    var url = "/webApp/staff/hotel/";
    var param = {};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            Log.i(TAG, "获取酒店信息成功");
            $rootScope.Hotel = obj.data;
            $scope.hotel = $rootScope.Hotel;
            $scope.menus = [
                {
                    title: "智能订餐台",
                    menu_id: "SmartOrder",
                    item: [
                        {title: "智能订餐台", item_id: "SmartOrder"}
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

    // 【门店】获取门店区域列表area/list/";
    url = "/webApp/admin/hotel_branch/area/list/";
    param = {branch_id: 1};
    $http.post(url, JSON.stringify(param)).success(function (obj) {
        if (obj.status === "true") {
            $rootScope.area = obj.data;
        } else {
            alert(obj.description);
        }
    });
});

// Angular路由配置
StaffApp.config(['$routeProvider', function ($routeProvider) {

    // 【酒店】智能订餐台
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

}]);
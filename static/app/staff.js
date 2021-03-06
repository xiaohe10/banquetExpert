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
    // 账户管理
    Account: {
        FinanceManage: "Account/FinanceManage.html", // 财务报表
        SMSDetails: "Account/SMSDetails.html", // 短信详单
        AccountManage: "Account/AccountManage.html" // 修改密码
    },
    // 评分审阅
    Review: {
        Rank: "Review/Rank.html", // 餐厅排名
        Scoring: "Review/Scoring.html", // 我的评分
        Tutorial: "Review/Tutorial.html" // 中国服务私人订制标准视频教程
    },
    // 微课堂
    MicroCourse: {
        LiveCourse: "",
        LiveVideo: ""
    }
};

// 对话框模板
Dialog = {
    // 预订台
    SmartOrder: {
        SmartOrder: {
            CreateOrder: "SmartOrder/SmartOrder/ReserveOrderDialog.html"
        }
    },
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
StaffApp.filter("order_status", function () {
    return function (order_status) {
        var TAG = ["已订", "客到", "已完成", "已撤单"];
        return TAG[order_status];
    }
});
StaffApp.filter("desk_status", function () {
    return function (desk_status) {
        var TAG = ["空闲", "预定中", "用餐中"];
        return TAG[desk_status];
    }
});
StaffApp.filter("operation_type", function (operation_type) {
    return function () {
        var TAG = ["预定", "客到", "翻台", "调桌", "撤单", "补录"];
        return TAG[operation_type];
    }
});

// 服务定义
StaffApp.service('HotelService', function ($http) {

    // 获取员工列表
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

    // 获取渠道列表
    this.getChannelList = function (hotel_id) {
        var url = "/webApp/admin/hotel/channel/list/";
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

    // 获取员工所在酒店的门店列表
    this.getBranchList = function (hotel_id) {
        var url = "/webApp/staff/hotel_branch/list/ ";
        var param = {
            hotel_id: hotel_id
        };
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                return obj.data;
            } else {
                alert(obj.description);
            }
        });
    }
});
StaffApp.service('BranchService', function ($http) {

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
    };
});
StaffApp.service('StaffService', function ($http) {

    var TAG = "StaffService";

    // 【员工】获取酒店信息
    this.getHotelProfile = function ($rootScope) {
        var url = "/webApp/staff/hotel/";
        var param = {};
        $http.post(url, JSON.stringify(param)).success(function (obj) {
            if (obj.status === "true") {
                Log.i(TAG, "获取酒店信息成功");
                $rootScope.hotel = obj.data;
                $rootScope.Menus = [
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
    }
});

// 指令定义
StaffApp.directive('loading', function () {

    return {
        replace: true,
        restrict: 'AE',
        templateUrl: "",
        template: '<div id="circle-loading" class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%;">60%</div></div>',
        link: function ($scope, $element, attrs) {
            var top = $(window).height() / 2 - 25;
            var left = $(window).width() / 2 - 25;
            $('.loading').css({
                top: top,
                left: left
            });
            //$(tpl).appendTo('body');
        }
    };
});

// 加载器
StaffApp.factory('loadingInterceptor', function ($q) {

    return {
        request: function (config) {
            $("#circle-loading").show();
            return config || $q.when(config);
        },
        requestError: function (rejection) {
            $("#circle-loading").show();
        },
        response: function (response) {
            $("#circle-loading").hide();
            return response || $q.when(response);
        },
        responseError: function (rejection) {
            $("#circle-loading").hide();
            return $q.reject(rejection);
        }
    };
});

// 侧边导航栏控制器
StaffApp.controller('drawerCtrl', function ($routeParams, $rootScope, $scope, $http, $location) {

    var TAG = "drawerCtrl";

    $rootScope.loading = true;
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
    // 员工信息
    $rootScope.Staff = {};
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
    // 三十六宴
    $rootScope.Banquet = {
        "生日宴": ["满月宴", "百天宴", "周岁宴", "成人(18)宴", "生日(19-59)宴", "寿(60-90)宴", "期颐(90-100)宴"],
        "婚宴": ["求婚宴", "订婚宴", "婚宴", "回门宴", "答谢宴", "纪念日", "银婚", "金婚", "钻石婚"],
        "家宴": ["团圆宴", "接风宴", "送行宴", "庆祝宴", "追思宴"],
        "商务宴": ["开业大吉宴", "合作宴", "年会宴"],
        "师徒宴": ["拜师宴", "谢师宴"],
        "友谊宴": ["同学宴", "朋友宴", "Farewell Party"],
        "晋升宴": ["晋升者宴请同事", "同事宴请晋升者"],
        "乔迁宴": ["乔迁宴"],
        "文化交流宴": ["名人纪念宴", "文化推广宴", "品酒会"],
        "节日宴": ["七夕节", "父/母亲节"]
    };
    // 侧边栏
    $rootScope.Drawer = [
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
    // 标记员工端
    $rootScope.from = "staff";

    var Hotel = {
        // 获取员工列表
        getStaffList: function (hotel_id) {
            var url = "/webApp/admin/hotel/staff/list/";
            var param = {hotel_id: hotel_id};
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $rootScope.Hotel.Staff = obj.data;
                } else {
                    alert(obj.description);
                    $rootScope.Hotel.Staff = {count: '', list: []};
                }
            });
        },
        // 获取渠道列表
        getChannelList: function (hotel_id) {
            var url = "/webApp/admin/hotel/channel/list/";
            var param = {hotel_id: hotel_id};
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $rootScope.Hotel.Channel = obj.data;
                } else {
                    alert(obj.description);
                    $rootScope.Hotel.Channel = {count: '', list: []};
                }
            });
        }
    };

    var Staff = {
        // 获取员工信息
        getProfile: function (hotel_id) {
            var url = "/webApp/staff/profile/get/";
            var param = {hotel_id: hotel_id};
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $rootScope.Staff = obj.data;
                    $rootScope.loading = false;
                    $rootScope.Authority = {
                        '0100': true, '0101': true,
                        '0200': true, '0201': true, '0202': true, '0203': true, '0204': true, '0205': true, '0206': true,
                        '0300': true, '0301': true, '0302': true, '0303': true, '0304': true, '0305': true,
                        '0400': true, '0401': true, '0402': true, '0403': true,
                        '0500': true, '0501': true, '0502': true, '0503': true,
                        '0600': true, '0601': true,
                        '0700': true, '0701': true, '0702': true
                    };
                    $scope.Drawer = [
                        {
                            title: "智能订餐台",
                            menu_id: "SmartOrder",
                            authority: '0100',
                            item: [
                                {title: "智能订餐台", item_id: "SmartOrder", authority: '0101'}
                            ]
                        },
                        {
                            title: "订单管理",
                            menu_id: "Order",
                            authority: '0200',
                            item: [
                                {title: "预定通知单", item_id: "ReserveNotice", authority: '0201'},
                                {title: "历史订单", item_id: "OrderHistory", authority: '0202'},
                                {title: "订单金额录入", item_id: "InsertOrder", authority: '0203'},
                                {title: "订单统计", item_id: "OrderStatistics", authority: '0204'},
                                {title: "来电记录", item_id: "PhoneReserve", authority: '0205'},
                                {title: "操作日志", item_id: "OperationLog", authority: '0206'}
                            ]
                        },
                        {
                            title: "客户管理",
                            menu_id: "Customer",
                            authority: '0300',
                            item: [
                                {title: "客户档案列表", item_id: "CustomerProfiles", authority: '0301'},
                                {title: "客源情况分析", item_id: "CustomerAnalysis", authority: '0302'},
                                {title: "会员价值设置", item_id: "MemberValue", authority: '0303'},
                                {title: "客户档案回收站", item_id: "CustomerRecycleBin", authority: '0304'},
                                {title: "纪念日查询报表", item_id: "AnniversaryReport", authority: '0305'}
                            ]
                        },
                        {
                            title: "账户管理",
                            menu_id: "Account",
                            authority: '0400',
                            item: [
                                {title: "财务报表", item_id: "FinanceManage", authority: '0401'},
                                {title: "短信详单", item_id: "SMSDetails", authority: '0402'},
                                {title: "修改密码", item_id: "AccountManage", authority: '0403'}
                            ]
                        },
                        {
                            title: "评分审阅",
                            menu_id: "Review",
                            authority: '0500',
                            item: [
                                {title: "我的评分", item_id: "Scoring", authority: '0501'},
                                {title: "排名", item_id: "Rank", authority: '0502'},
                                {title: "中国服务私人订制标准视频教程", item_id: "Tutorial", authority: '0503'}
                            ]
                        },
                        {
                            "title": "微课堂管理",
                            menu_id: "MicroCourse",
                            authority: '0700',
                            item: [
                                {title: "直播课堂", item_id: "LiveCourse", authority: '0701'},
                                {title: "视频管理", item_id: "LiveVideo", authority: '0702'}
                            ]
                        },
                        {
                            "title": "移动客户端",
                            menu_id: "App",
                            authority: '0800',
                            item: [
                                {title: "我的客户", item_id: "MyCustomer"},
                                {title: "我的订单", item_id: "MyOrder"},
                                {title: "客户管理", item_id: "Customer"},
                                {
                                    title: "订单管理",
                                    item_id: "Order",
                                    item: [
                                        {
                                            title: "查看订单",
                                            item_id: "VisitOrder"
                                        },
                                        {
                                            title: "查看餐位",
                                            item_id: "VisitDesk",
                                            item: []
                                        }
                                    ]
                                }
                            ]
                        }
                    ];
                } else {
                    alert(obj.description);
                    $rootScope.Hotel = {
                        "hotel_id": 1,
                        "branch_id": 2,
                        "name": "北京宴",
                        "icon": "http://oss.aliyun/banquet/avatar/1.jpg",
                        "branches_count": 3,
                        "owner_name": "杨秀荣",
                        "create_time": "创建时间"
                    };
                }
            });
        },
        // 获取所在酒店信息
        getHotelProfile: function (hotel_id) {
            var url = "/webApp/staff/hotel/";
            var param = {hotel_id: hotel_id};
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $rootScope.Hotel = obj.data;
                } else {
                    alert(obj.description);
                    $rootScope.Hotel = {
                        "hotel_id": 1,
                        "branch_id": 2,
                        "name": "北京宴",
                        "icon": "http://oss.aliyun/banquet/avatar/1.jpg",
                        "branches_count": 3,
                        "owner_name": "杨秀荣",
                        "create_time": "创建时间"
                    };
                }
            });
        },
        // 获取员工所在酒店的门店列表
        getBranchList: function () {
            var url = "/webApp/staff/hotel_branch/list/ ";
            var param = {};
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $rootScope.Hotel.BranchList = obj.data;
                    $rootScope.Hotel.index = 1;
                } else {
                    alert(obj.description);
                    $rootScope.Hotel.BranchList = {count: '', list: []};
                    $rootScope.Hotel.index = 1;
                }
            })
        },
        // 搜索我的订单列表
        getOrderList: function (status, search_key) {
            var url = "/webApp/staff/order/search/";
            var param = {status: status, search_key: search_key};
            $http.post(url, JSON.stringify(param)).success(function (obj) {
                if (obj.status === "true") {
                    $scope.Staff.OrderList = obj.data;
                } else {
                    alert(obj.description);
                    $scope.Staff.OrderList = {count: '', list: []};
                }
            });
        }
    };
    // 更新酒店信息
    $rootScope.$watch('Hotel', function () {
        // 获取酒店的门店列表
        Staff.getBranchList();
    });

    // 获取员工信息
    Staff.getProfile();
    Staff.getHotelProfile();
});

// Angular路由配置
StaffApp.config(['$routeProvider', '$httpProvider', function ($routeProvider, $httpProvider) {

    $httpProvider.interceptors.push('loadingInterceptor');

    // 【员工】智能订餐台
    $routeProvider
        .when('/SmartOrder/SmartOrder', {
            templateUrl: "./template/SmartOrder/SmartOrder.html", controller: function ($rootScope, $scope, $http, $modal) {
                var TAG = Templates.SmartOrder.SmartOrder;
                // 门店
                var Branch = {
                    // 获取门店的详情
                    getProfile: function (branch_id) {
                        var url = "/webApp/hotel_branch/profile/";
                        var param = {branch_id: branch_id};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch = obj.data;
                            } else {
                                Log.e(TAG, "getProfile:" + obj.description);
                                alert(obj.description);
                            }
                        });
                    },
                    /***
                     * 获取门店的区域列表
                     *
                     * @param branch_id 门店ID
                     *
                     */
                    getAreaList: function (branch_id) {
                        var url = "/webApp/hotel_branch/area/list/";
                        var param = {branch_id: branch_id};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch.Area = obj.data;
                            } else {
                                Log.e(TAG, "getAreaList:" + obj.description);
                                $scope.Branch.Area = {count: '', list: []};
                            }
                        });
                    },
                    /***
                     *
                     * 获取门店某一天某餐段的桌位使用情况列表
                     *
                     * @param branch_id 门店ID
                     * @param date 就餐日期
                     * @param dinner_period 餐段
                     *
                     */
                    getAreaDesk: function (branch_id, date, dinner_period) {
                        var url = "/webApp/hotel_branch/desk/list/";
                        var param = {
                            "branch_id": branch_id,
                            "date": date,
                            "dinner_period": dinner_period
                        };
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch.AreaDesk = obj.data;
                            } else {
                                alert(obj.description);
                                $scope.Branch.AreaDesk = {count: '', list: []};
                            }
                        });
                    }
                };
                // 员工
                var Staff = {
                    // 预定列表
                    ReserveList: function () {
                        var url = "/webApp/staff/order/search/";
                        var param = {
                            status: 0
                        };
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Staff.ReserveList = obj.data;
                            } else {
                                alert(obj.description);
                                $scope.Staff.ReserveList = {count: '', list: []};
                            }
                        });
                    },
                    // 订单
                    OrderList: function () {
                        var url = "/webApp/staff/order/search/";
                        var param = {};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Staff.OrderList = obj.data;
                            } else {
                                alert(obj.description);
                                $scope.Staff.OrderList = {count: '', list: []};
                            }
                        });
                    }
                };
                var Now = new Date();
                $scope.MealsPeriod = ['午餐', '晚餐', '夜宵'];
                $scope.weekdays = ["周一", "周二", "周三", "周四", "周五", "周六"];
                $scope.WeekDays = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
                $scope.Reception = ['VIP', 'VVIP', '贵宾'];
                $scope.MealsTime = $rootScope.MealsTime.lunch;
                // 当前门店信息
                $scope.Branch = {
                    address: "北京市丰台区靛厂路333号",
                    branch_id: 6,
                    city: "北京",
                    county: "北京",
                    create_time: "2017-07-10T23:50:57.077",
                    hotel_name: "未登录",
                    icon: "",
                    manager_name: "郭藏燃",
                    name: "未选择门店",
                    province: "北京"
                };
                // 员工订单记录
                $scope.Staff = {
                    // 来电列表
                    PhoneList: {count: 0, list: []},
                    // 预约列表
                    ReserveList: {count: 0, list: []},
                    // 订单列表
                    OrderList: {
                        consumption: 0,
                        count: 0,
                        guest_consumption: "0.00",
                        guest_number: 0,
                        list: []
                    }
                };
                // 查询的表单
                var date = new Date();
                $scope.AreaOption = {
                    // 选择区域【默认全部区域】
                    name: "all_area",
                    // 只看空闲桌位【默认否】
                    empty_desk: false
                };
                $scope.QueryForm = {
                    branch_id: 0,
                    date: '2017-07-15',//Now.format('yyyy/MM/dd'),
                    dinner_period: 0
                };
                // 预定表单
                $scope.ReserveForm = {
                    // 预定用餐日期
                    dinner_date: Now.toDateString(),
                    // 预定用餐时间
                    dinner_time: Now.toTimeString(),
                    // 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵')
                    dinner_period: 0,
                    // 姓名
                    name: "",
                    // 联系电话
                    contact: "",
                    // 客人数量
                    guest_number: 10,
                    // 桌位ID的数组
                    desks: [],
                    // 桌位name的数组
                    rooms: [],
                    // 宴会类型，来自36宴
                    banquet: "",
                    // 员工备注
                    staff_description: "",
                    // --预约短信
                    order_sms: false,
                    // --发路线
                    order_route: false
                };
                // 预定操作
                $scope.ReserveOption = [
                    {name: "客到", value: "1"},
                    {name: "翻台", value: "2"},
                    {name: "调桌", value: "3"},
                    {name: "撤单", value: "4"}
                ];
                // 查询表单
                $scope.SearchForm = {
                    keyword: "",
                    type: 0
                };
                // 排序选项
                $scope.SortSelection = [
                    "按桌位排序", "按下单时间", "客户分类", "有换桌", "有接单人",
                    "有临牌", "操作人", "手机下单", "网络"
                ];
                // 分页显示
                $scope.pages = [1, 2, 3, 4, 5, 6, 7, 8, 9];
                // 检测门店列表更新
                $rootScope.$watch('Hotel.BranchList', function () {
                    if ($rootScope.Hotel.BranchList.list.length > 0) {
                        var index = 0;
                        Log.i(TAG, "选择门店：" + index);
                        var branch = $scope.Hotel.BranchList.list[index];
                        Branch.getProfile(branch.branch_id);
                    }
                });
                // 检测门店信息更新
                $scope.$watch('Branch', function () {
                    // 获取门店的区域列表
                    Branch.getAreaList($scope.Branch.branch_id);
                    // 获取门店的空闲餐位列表
                    Branch.getAreaDesk($scope.Branch.branch_id, $scope.QueryForm.date, $scope.QueryForm.dinner_period);
                });
                // 监测日期和餐段的变化
                $scope.$watch('QueryForm.date', function () {
                    Branch.getAreaDesk($scope.Branch.branch_id, $scope.QueryForm.date, $scope.QueryForm.dinner_period);
                    Staff.ReserveList();
                    Staff.OrderList();
                });
                // 获取门店的桌位列表
                $scope.$watch('QueryForm.dinner_period', function () {
                    Branch.getAreaDesk($scope.Branch.branch_id, $scope.QueryForm.date, $scope.QueryForm.dinner_period);
                    Staff.ReserveList();
                    Staff.OrderList();
                });
                // 获取数据
                Branch.getAreaDesk($scope.Branch.branch_id, $scope.QueryForm.date, $scope.QueryForm.dinner_period);
                Staff.ReserveList();
                Staff.OrderList();
                // 选择三十六宴
                $scope.selectOne = function (k, v) {
                    $(this).popover({
                        title: k,
                        content: "这是三十六宴"
                    });
                };
                // 选择私人订制
                $scope.selectTwo = function (k, v) {
                    var Html = "";
                    $(this).popover({
                        trigger: 'click',
                        title: k,
                        content: "这是私人订制"
                    });
                };
                // 选择门店
                $scope.selectBranch = function (index) {
                    Log.i(TAG, "选择门店：" + index);
                    var branch = $scope.Hotel.BranchList.list[index];
                    Branch.getProfile(branch.branch_id);
                };
                // 选择三十六宴
                $scope.selectBanquet = function () {
                    var dlg = $modal.open({
                        templateUrl: "./template/SmartOrder/SmartOrder/BanquetDialog.html",
                        resolve: {
                            form: function () {
                                return $scope.ReserveForm;
                            },
                            banquet: function () {
                                return $rootScope.Banquet;
                            }
                        },
                        controller: function ($scope, banquet, form) {
                            $scope.banquet = banquet;
                            $scope.form = form;
                            $scope.submit = function () {
                                dlg.close();
                            };
                            $scope.cancel = function () {
                                dlg.dismiss({reason: "关闭选项"})
                            }
                        }
                    });
                };
                // 选择私人订制
                $scope.selectPersonal = function () {
                    var dlg = $modal.open({
                        templateUrl: "./template/SmartOrder/SmartOrder/PersonalDialog.html",
                        resolve: {
                            branch: function () {
                                return $scope.Branch;
                            },
                            form: function () {
                                return $scope.ReserveForm;
                            }
                        },
                        controller: function ($scope, branch, form) {
                            $scope.branch = branch;
                            $scope.form = form;
                            // 选择私人订制对话框
                            $scope.selectLabel = function (label) {
                                var index = $scope.form.staff_description.indexOf(label);
                                if (index === -1) {
                                    $scope.form.staff_description += label + ", ";
                                } else {
                                    $scope.form.staff_description.replace(label + ",", "");
                                }
                            };
                            $scope.submit = function () {
                                dlg.close();
                            };
                            $scope.cancel = function () {
                                dlg.dismiss({reason: "关闭选项"})
                            }
                        }
                    });
                };
                // 选择私人订制对话框
                $scope.selectLabel = function (label) {
                    var index = $scope.ReserveForm.staff_description.indexOf(label);
                    if (index === -1) {
                        $scope.ReserveForm.staff_description += " " + label;
                    } else {
                        $scope.ReserveForm.staff_description.replace(label, "");
                    }
                };
                // 预定
                $scope.reserve = function () {
                    Log.i(TAG, "预定:" + JSON.stringify($scope.form));
                    // 用餐日期
                    $scope.ReserveForm.dinner_date = $scope.QueryForm.date;
                    // 选择桌位
                    var Desks = $scope.Branch.AreaDesk.list.filter(function (item) {
                        return item.selected === true;
                    });
                    $scope.ReserveForm.desks.splice(0, $scope.ReserveForm.desks.length);
                    $scope.ReserveForm.rooms.splice(0, $scope.ReserveForm.rooms.length);
                    Desks.forEach(function (item) {
                        $scope.ReserveForm.desks.push(item.desk_id);
                        $scope.ReserveForm.rooms.push(item.number);
                    });
                    // 选择餐段
                    $scope.ReserveForm.dinner_period = $scope.QueryForm.dinner_period;
                    $scope.ReserveForm.dinner_date.getDay();
                    switch ($scope.QueryForm.dinner_period) {
                        case '0':
                            $scope.MealsTime = $rootScope.MealsTime.lunch;
                            break;
                        case '1':
                            $scope.MealsTime = $rootScope.MealsTime.dinner;
                            break;
                        case '2':
                            $scope.MealsTime = $rootScope.MealsTime.supper;
                            break;
                        default:
                            $scope.MealsTime = $rootScope.MealsTime.lunch;
                            break;
                    }

                    var url = "/webApp/admin/order/submit/";
                    var param = $scope.ReserveForm;

                    // 弹出订单对话框
                    // var dlg = $modal.open({
                    //     templateUrl: "./template/" + Dialog.SmartOrder.SmartOrder.CreateOrder,
                    //     resolve: {
                    //         form: function () {
                    //             // 选中的桌位列表
                    //             var Desks = $scope.Branch.AreaDesk.list.filter(function (item) {
                    //                 return item.selected === true;
                    //             });
                    //             // 重新添加桌位
                    //             $scope.ReserveForm.desks.splice(0, $scope.ReserveForm.desks.length);
                    //             Desks.forEach(function (item) {
                    //                 $scope.ReserveForm.desks.push(item.desk_id);
                    //                 $scope.ReserveForm.rooms.push(item.number);
                    //             });
                    //             return $scope.ReserveForm;
                    //         },
                    //         MealsPeriod: function () {
                    //             return $scope.MealsPeriod;
                    //         }
                    //     },
                    //     controller: function ($scope, form, MealsPeriod) {
                    //         var TAG = Dialog.SmartOrder.SmartOrder.CreateOrder;
                    //         Log.i(TAG, "添加预订单控制器");
                    //         $scope.option = "添加";
                    //         $scope.form = form;
                    //         $scope.MealsPeriod = MealsPeriod;
                    //         // 餐段选择变动了
                    //         $scope.$watch('QueryForm.dinner_period', function (p1, p2, p3) {
                    //             switch ($scope.QueryForm.dinner_period) {
                    //                 case 0:
                    //                     $scope.MealsTime = $rootScope.MealsTime.lunch;
                    //                     break;
                    //                 case 1:
                    //                     $scope.MealsTime = $rootScope.MealsTime.dinner;
                    //                     break;
                    //                 case 2:
                    //                     $scope.MealsTime = $rootScope.MealsTime.supper;
                    //                     break;
                    //                 default:
                    //                     $scope.MealsTime = $rootScope.MealsTime.lunch;
                    //                     break;
                    //             }
                    //         });
                    //         // 提交
                    //         $scope.submit = function () {
                    //             Log.i(TAG, "提交预订单:" + $scope.form);
                    //             dlg.close($scope.form);
                    //         };
                    //         // 取消
                    //         $scope.cancel = function () {
                    //             Log.i(TAG, "取消预订单");
                    //         }
                    //     }
                    // });
                    // dlg.opened.then(function () {
                    //     Log.i(TAG, "对话框已经打开");
                    // });
                    // dlg.result.then(function (result) {
                    //     Log.i(TAG, JSON.stringify(result));
                    //     var url = "/webApp/order/submit/";
                    //     var param = angular.copy(result);
                    //     $http.post(url, JSON.stringify(param)).success(function (obj) {
                    //         if (obj.status === "true") {
                    //             alert("添加预定单成功，订单编号是:" + obj.data.order_id);
                    //         } else {
                    //             alert(obj.description);
                    //         }
                    //     });
                    // }, function (reason) {
                    //     Log.i(TAG, reason);
                    // });
                };
                // 提交预订单
                $scope.submit = function () {
                    var url = "/webApp/order/submit/";
                    var param = angular.copy($scope.ReserveForm);
                    // 转换数据类型
                    param.dinner_period = parseInt(param.dinner_period);
                    Log.i(TAG, JSON.stringify(param));
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            alert("添加预定单成功，订单编号是:" + obj.data.order_id);
                        } else {
                            alert(obj.description);
                        }
                    });
                };
                // 取消预订单
                $scope.cancel = function () {

                };
                // 查询
                $scope.search = function () {
                    Staff.OrderList();
                };
                // 处理来电
                $scope.handlePhone = function (index) {
                    Log.i(TAG, JSON.stringify($scope.Staff.PhoneList[index]));
                };
                // 处理预订单
                $scope.handleReserve = function (index) {
                    Log.i(TAG, JSON.stringify($scope.ReserveOption[index]));
                    // 添加用户提示
                    var Order = {
                        // 撤单
                        Cancel: function () {

                        },
                        // 换桌
                        // 加桌
                        // 修改
                        // 关闭
                        // 发路线
                        // 发短信
                        // 相关订单
                        // 客户档案
                        UpdateOrder: function (option) {
                            var url = "/webApp/order/update/";
                            var param = angular.copy($scope.ReserveForm);
                            switch (option) {
                                case "1": // 客到
                                    param.status = 1;
                                    break;
                                case "2": // 翻台
                                    param.status = 3;
                                    break;
                                case "3": // 调桌
                                    // param.status = 1;
                                    param.desks = [];
                                    param.table_count = 0;
                                    break;
                                case "4": // 撤单
                                    param.status = 3;
                                    break;
                                default:
                                    break;
                            }
                            // 转换数据类型
                            param.dinner_period = parseInt(param.dinner_period);
                            Log.i(TAG, JSON.stringify(param));
                            $http.post(url, JSON.stringify(param)).success(function (obj) {
                                if (obj.status === "true") {
                                    alert("添加预定单成功，订单编号是:" + obj.data.order_id);
                                } else {
                                    alert(obj.description);
                                }
                            });
                        }
                    };
                };
            }
        });

    // 【员工】订单管理
    $routeProvider
        .when('/Order/InsertOrder', {
            templateUrl: "./template/Order/InsertOrder.html", controller: function ($rootScope, $scope, $http) {
                var TAG = Templates.Order.InsertOrder;// "#/Order/InsertOrder";
                var Order = {
                    History: function (option) {
                        // 搜索订单列表
                        var url = "/webApp/order/search/";
                        var param = angular.copy(option);
                        param.date_from = param.date_to;
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data = obj.data;
                            } else {
                                $scope.data = {count: 0, list: []};
                                alert("无订单！");
                            }
                        });
                    }
                };
                $scope.option = {
                    // 选择开始日期
                    date_from: "2017-07-12",
                    // 选择结束日期
                    date_to: "2017-07-12",
                    // 选择渠道
                    select_channel: 0,
                    // 查询字符串
                    search_key: "",
                    // 排序参数
                    orderBy: 'name'
                };
                $scope.order = [];
                for (var i = 0; i < 7; i++) {
                    $scope.order.push({value: i, title: "2017-07-1" + i});
                }
                $scope.channel = $rootScope.channel;
                $scope.data = [];
                Order.History($scope.option);
                $scope.search = function () {
                    Log.i(TAG, "搜索：" + JSON.stringify($scope.option));
                    Order.History($scope.option);
                };
                $scope.save = function () {
                    Log.i(TAG, "保存：" + JSON.stringify($scope.data));
                }
            }
        })
        .when('/Order/OperationLog', {
            templateUrl: "./template/Order/OperationLog.html", controller: function ($rootScope, $scope, $http) {
                var TAG = Templates.Order.OperationLog;
                // 门店
                var Branch = {
                    /**
                     * 获取门店的详情
                     * @param branch_id 门店id
                     *
                     */
                    getProfile: function (branch_id) {
                        var url = "/webApp/hotel_branch/profile/";
                        var param = {branch_id: branch_id};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch = obj.data;
                                // alert("当前门店:" + $scope.Branch.name);
                            } else {
                                Log.e(TAG, "getProfile:" + obj.description);
                                alert(obj.description);
                            }
                        });
                    },
                    /***
                     * 获取门店的区域列表
                     *
                     * @param branch_id 门店ID
                     *
                     */
                    getAreaList: function (branch_id) {
                        var url = "/webApp/hotel_branch/area/list/";
                        var param = {branch_id: branch_id};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch.Area = obj.data;
                            } else {
                                Log.e(TAG, "getAreaList:" + obj.description);
                                $scope.Branch.Area = {count: '', list: []};
                            }
                        });
                    },
                    /***
                     *
                     * 获取门店某一天某餐段的桌位使用情况列表
                     *
                     * @param branch_id 门店ID
                     * @param date 就餐日期
                     * @param dinner_period 餐段
                     *
                     */
                    getAreaDesk: function (branch_id, date, dinner_period) {
                        var url = "/webApp/hotel_branch/desk/list/";
                        var param = {
                            "branch_id": branch_id,
                            "date": "2017-07-17",
                            "dinner_period": 0
                        };
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch.AreaDesk = obj.data;
                            } else {
                                alert(obj.description);
                                $scope.Branch.AreaDesk = {count: '', list: []};
                            }
                        });
                    }
                };
                var Order = {
                    OperationLog: function () {
                        var url = "/webApp/order/log/list/";
                        var param = angular.copy($scope.option);
                        param.branch_id = parseInt(param.branch_id);
                        param.area_id = parseInt(param.area_id);
                        param.desk_id = parseInt(param.desk_id);
                        $http.post(url, param).success(function (obj) {
                            if (obj.status === 0) {
                                $scope.data = obj.data;
                            } else {
                                $scope.data = {count: 0, list: []};
                            }
                        });
                    }
                };
                $scope.option = {
                    date_from: "2017/07/01",
                    date_to: "2017/07/31",
                    // order_id: 1,
                    branch_id: 1,
                    area_id: 1,
                    desk_id: 1,
                    select_channel: 1,
                    keyword: "",
                    orderBy: "create_time"
                };
                $scope.data = {count: 0, list: []};
                $scope.$watch('option.branch_id', function (p1, p2, p3) {
                    Branch.getProfile(($scope.option.branch_id));
                });
                $scope.$watch('Branch', function (p1, p2, p3) {
                    Branch.getAreaList($scope.option.branch_id);
                    Branch.getAreaDesk($scope.option.branch_id);
                });
                $scope.search = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    Order.OperationLog();
                }
            }
        })
        .when('/Order/OrderHistory', {
            templateUrl: "./template/Order/OrderHistory.html", controller: function ($rootScope, $scope, $http, $modal) {
                var TAG = Templates.Order.OrderHistory;
                var Order = {
                    History: function (option) {
                        // 搜索订单列表
                        var url = "/webApp/staff/order/search/";
                        var param = angular.copy(option);
                        param.branch_id = parseInt(param.branch_id);
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data = obj.data;
                            } else {
                                $scope.data = {count: 0, list: []};
                                alert("无订单！");
                            }
                        });
                    }
                };
                // 门店
                var Branch = {
                    // 获取门店的详情
                    getProfile: function (branch_id) {
                        var url = "/webApp/hotel_branch/profile/";
                        var param = {branch_id: branch_id};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch = obj.data;
                                // alert("当前门店:" + $scope.Branch.name);
                            } else {
                                Log.e(TAG, "getProfile:" + obj.description);
                                alert(obj.description);
                            }
                        });
                    },
                    /***
                     * 获取门店的区域列表
                     *
                     * @param branch_id 门店ID
                     *
                     */
                    getAreaList: function (branch_id) {
                        var url = "/webApp/hotel_branch/area/list/";
                        var param = {branch_id: branch_id};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch.Area = obj.data;
                            } else {
                                Log.e(TAG, "getAreaList:" + obj.description);
                                $scope.Branch.Area = {count: '', list: []};
                            }
                        });
                    },
                    /***
                     *
                     * 获取门店某一天某餐段的桌位使用情况列表
                     *
                     * @param branch_id 门店ID
                     * @param date 就餐日期
                     * @param dinner_period 餐段
                     *
                     */
                    getAreaDesk: function (branch_id, date, dinner_period) {
                        var url = "/webApp/hotel_branch/desk/list/";
                        var param = {
                            "branch_id": branch_id,
                            "date": date,
                            "dinner_period": dinner_period
                        };
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.Branch.AreaDesk = obj.data;
                            } else {
                                alert(obj.description);
                                $scope.Branch.AreaDesk = {count: '', list: []};
                            }
                        });
                    }
                };
                // 操作栏
                $scope.option = {
                    // 选择开始日期
                    date_from: "2017-07-01",
                    // 选择结束日期
                    date_to: "2017-08-09",
                    // 选择门店
                    branch_id: 1,
                    // 选择区域
                    area_id: 1,
                    // 选择桌位
                    desk_id: 1,
                    // 选择渠道
                    select_channel: 1,
                    // 查询字符串
                    search_key: "",
                    // 排序参数
                    orderBy: 'name',
                    // 订单状态
                    status: 0
                };
                // 详细信息
                $scope.detail = {
                    order_count: 0,
                    customer_count: 0,
                    total: 0,
                    average: 0
                };
                $scope.area = $rootScope.area;
                $scope.desk = [];
                $scope.channel = $rootScope.channel;
                $scope.nav = ['进行中', '已完成', '已撤单'];
                $scope.details = {order: 0, person: 0, total: 0, average: 0};
                // 表格数据
                $scope.data = {count: 0, list: []};
                // 监听数据变化
                $scope.$watch('option.branch_id', function (p1, p2, p3) {
                    Branch.getAreaList($scope.option.branch_id);
                    Branch.getAreaDesk();
                });
                // 事件处理
                $scope.on_area_change = function () {
                    Log.i(TAG, "选择区域:" + $scope.option.select_area);
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
                    Log.i(TAG, "查询订单数据:" + JSON.stringify($scope.option));
                    Order.History($scope.option);
                };
                $scope.export = function () {
                    Log.i(TAG, "导出订单数据:" + JSON.stringify($scope.table));
                };
                $scope.filter = function (index) {
                    Log.i(TAG, "查看" + index + ":" + $scope.nav[index]);
                    $scope.option.status = index;
                    Order.History($scope.option);
                };
                $scope.sort = function (index) {
                    // var tags = [
                    //     "客户姓名", "手机", "下单时间", "就餐时间", "接单渠道", "区域",
                    //     "桌位", "就餐人数", "消费金额", "订单状态", "操作人"
                    // ];
                    var tags = [
                        "name", "contact", "create_time", "arrival_time", "接单渠道", "区域",
                        "桌位", "guest_number", "consumption", "status", "internal_channel"
                    ];
                    Log.i(TAG, "根据 '" + tags[index] + "' 对列表排序");
                    $scope.option.orderBy = tags[index];
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
                $scope.order_details = function (order_id) {
                    Log.i(TAG, "订单详情:" + order_id);
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Order.OrderHistory.OrderDetails,
                        controller: function ($scope) {
                            var TAG = Dialog.Order.OrderHistory.OrderDetails;
                            Log.i(TAG, "对话框控制器");
                            $scope.order = {
                                details: {
                                    "order_id": 1,
                                    "staff_name": "小二",
                                    "create_time": "2014-02-01 10:00:00",
                                    "cancel_time": "2014-02-01 10:00:00",
                                    "arrival_time": "2014-02-01 10:00:00",
                                    "finish_time": "2014-02-01 10:00:00",
                                    "consumption": 1000,
                                    "status": 0,
                                    "dinner_date": "2014-02-01",
                                    "dinner_time": "12:00",
                                    "dinner_period": 0,
                                    "name": "李四",
                                    "guest_type": "vip",
                                    "contact": "18813101211",
                                    "guest_number": 10,
                                    "banquet": "满月宴",
                                    "desks": [{"desk_id": 1, "number": "309"}],
                                    "user_description": "生日宴，准备蜡烛",
                                    "staff_description": "客户年纪大，做好防滑",
                                    "water_card": "水牌内容",
                                    "door_card": "门牌内容",
                                    "sand_table": "沙盘内容",
                                    "welcome_screen": "欢迎xx领导",
                                    "welcome_fruit": 128,
                                    "welcome_card": "欢迎你",
                                    "pictures": ["http://demo.com/1.jpg", "http://demo.com/2.jpg"],
                                    "background_music": "我爱你中国",
                                    "has_candle": true,
                                    "has_flower": false,
                                    "has_balloon": false,
                                    "group_photo": "合照名称",
                                    "internal_channel": "刘光艳",
                                    "external_channel": "美团"
                                },
                                log: {count: 0, list: []}
                            };
                            // 获取订单详情
                            var Order = {
                                Details: function (order_id) {
                                    var url = "/webApp/order/profile/";
                                    var param = {
                                        order_id: order_id
                                    };
                                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                                        if (obj.status === "true") {
                                            $scope.order.details = obj.data;
                                        } else {
                                            $scope.order.details = {
                                                "order_id": 1,
                                                "staff_name": "小二",
                                                "create_time": "2014-02-01 10:00:00",
                                                "cancel_time": "2014-02-01 10:00:00",
                                                "arrival_time": "2014-02-01 10:00:00",
                                                "finish_time": "2014-02-01 10:00:00",
                                                "consumption": 1000,
                                                "status": 0,
                                                "dinner_date": "2014-02-01",
                                                "dinner_time": "12:00",
                                                "dinner_period": 0,
                                                "name": "李四",
                                                "guest_type": "vip",
                                                "contact": "18813101211",
                                                "guest_number": 10,
                                                "banquet": "满月宴",
                                                "desks": [{"desk_id": 1, "number": "309"}, {"desk_id": 2, "number": "312"}, {"desk_id": 3, "number": "311"}],
                                                "user_description": "生日宴，准备蜡烛",
                                                "staff_description": "客户年纪大，做好防滑",
                                                "water_card": "水牌内容",
                                                "door_card": "门牌内容",
                                                "sand_table": "沙盘内容",
                                                "welcome_screen": "欢迎xx领导",
                                                "welcome_fruit": 128,
                                                "welcome_card": "欢迎你",
                                                "pictures": ["http://demo.com/1.jpg", "http://demo.com/2.jpg"],
                                                "background_music": "我爱你中国",
                                                "has_candle": true,
                                                "has_flower": false,
                                                "has_balloon": false,
                                                "group_photo": "合照名称",
                                                "internal_channel": "刘光艳",
                                                "external_channel": "美团"
                                            };
                                            alert(obj.description);
                                        }
                                    });
                                },
                                OperationLog: function (order_id) {
                                    var url = "/webApp/order/log/list/";
                                    var param = {
                                        order_id: order_id
                                    };
                                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                                        if (obj.status === "true") {
                                            $scope.order.log = obj.data;
                                        } else {
                                            $scope.order.log = {count: 0, list: []};
                                            alert("无订单！");
                                        }
                                    });
                                }
                            };
                            Order.Details(order_id);
                            Order.OperationLog(order_id);
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
                                Log.i(TAG, JSON.stringify($scope.data));
                                dlg.dismiss({code: "cancel"});
                            }
                        }
                    });
                }
            }
        })
        .when('/Order/OrderStatistics', {
            templateUrl: "./template/Order/OrderStatistics.html", controller: function ($scope, $http) {
                var Color = [
                    '#ffccff', '#ccffcc', '#ffcccc', '#ccccff', '#ffccff', '#ccffcc',
                    '#ffcccc', '#ccccff', '#ffccff', '#ccffcc', '#ffcccc', '#ccccff'
                ];
                // 选项
                var options = {
                    scaleOverlay: true,
                    responsive: true,
                    legend: {
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: '客源流动监测图'
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    }
                };
                // 标签
                var labels = [];
                // 数据集
                var datasets = [];
                // 数据
                var data = {
                    labels: labels,
                    datasets: datasets
                };
                // 绘图
                var ctx = document.getElementById('chart1').getContext('2d');
                var chart = new Chart(ctx, {type: 'bar', data: data, options: options});
                var Order = {
                    OrderStatistics: function () {
                        // 月订单列表（员工服务的订单，不是填写的预订单）
                        var url = "/webApp/order/month_list/";
                        var param = {};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                var data = obj.data;
                                var order_number = [];
                                var guest_number = [];
                                var desk_number = [];
                                var consumption = [];
                                var person_consumption = [];
                                var desk_consumption = [];
                                labels.splice(0, labels.length);
                                angular.forEach(data, function (item, index, array) {
                                    labels.push(item.month);
                                    order_number.push(item.order_number);
                                    guest_number.push(item.guest_number);
                                    desk_number.push(item.desk_number);
                                    consumption.push(item.consumption);
                                    person_consumption.push(item.person_consumption);
                                    desk_consumption.push(item.desk_consumption);
                                });
                                datasets.splice(0, datasets.length);
                                datasets.push({data: order_number, backgroundColor: Color[0], label: "订单数"});
                                datasets.push({data: guest_number, backgroundColor: Color[0], label: "人数"});
                                datasets.push({data: desk_number, backgroundColor: Color[0], label: "桌数"});
                                datasets.push({data: consumption, backgroundColor: Color[0], label: "总消费"});
                                datasets.push({data: person_consumption, backgroundColor: Color[0], label: "人均消费"});
                                datasets.push({data: desk_consumption, backgroundColor: Color[0], label: "桌均消费"});
                                chart.update();
                            } else {
                                alert("无月订单列表");
                            }
                        });
                    }
                };
                Order.OrderStatistics();
            }
        })
        .when('/Order/PhoneReserve', {
            templateUrl: "./template/Order/PhoneReserve.html", controller: function ($scope) {
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
            templateUrl: "./template/Order/ReserveNotice.html", controller: function ($rootScope, $scope, $modal, $http) {
                var TAG = Templates.Order.ReserveNotice;
                // 操作栏
                $scope.option = {
                    date_from: "2017-07-01",
                    date_to: "2017-07-18",
                    dinner_period: "",
                    select_area: 0,
                    select_channel: 0,
                    keyword: "18800184976",
                    daily_report: 0,
                    phone_mask: false,
                    desk_merge: true,
                    print_size: 0,
                    orderBy: "name"
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
                $scope.data = {count: 0, list: []};
                var Order = {
                    getReserveOrder: function (option) {
                        Log.i(TAG, "查询订单数据:" + JSON.stringify(option));
                        // 搜索订单列表
                        var url = "/webApp/staff/order/search/";
                        var param = angular.copy(option);
                        param.branch_id = parseInt(param.branch_id);
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data = obj.data;
                            } else {
                                $scope.data = {count: 0, list: []};
                                alert("无订单！");
                            }
                        });
                    }
                };
                Order.getReserveOrder($scope.option);
                // 事件处理
                $scope.query = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    Order.getReserveOrder($scope.option);
                };
                $scope.export = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.print = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                };
                $scope.sort = function (index) {
                    var tags = [
                        "dinner_time", "table_count", "桌号", "name", "contact", "guest_number",
                        "internal_channel", "create_time", "guest_type", "status", "internal_channel",
                        "订单详情"
                    ];
                    Log.i(TAG, "根据 '" + tags[index] + "' 对列表排序");
                    $scope.option.orderBy = tags[index];
                };
                $scope.today = function (index) {
                    var tags = [
                        "今日报表", "午餐", "晚餐", "夜宵", "已撤销订单", "散客订单"
                    ];
                    Log.i(TAG, "根据 '" + tags[index] + "' 过滤列表数据");
                    switch (index) {
                        case 0:
                            $scope.option.date_from = "2017-07-18";
                            $scope.option.date_to = "2017-07-18";
                            break;
                        case 1:
                            $scope.option.dinner_period = 0;
                            break;
                        case 2:
                            $scope.option.dinner_period = 1;
                            break;
                        case 3:
                            $scope.option.dinner_period = 2;
                            break;
                        case 4:
                            $scope.option.status = 2;
                            break;
                        case 5:
                            $scope.option.status = 1;
                            break;
                    }
                    Order.getReserveOrder($scope.option);
                };
                // 对话框
                $scope.order_details = function (order_id) {
                    Log.i(TAG, "订单详情:" + order_id);
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
                            // 获取订单详情
                            var Order = {
                                OrderDetails: function (order_id) {
                                    var url = "/webApp/order/profile/";
                                    var param = {
                                        order_id: order_id
                                    };
                                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                                        if (obj.status === "true") {
                                            $scope.order.details = obj.data;
                                        } else {
                                            $scope.order.details = {
                                                "order_id": 1,
                                                "staff_name": "小二",
                                                "create_time": "2014-02-01 10:00:00",
                                                "cancel_time": "2014-02-01 10:00:00",
                                                "arrival_time": "2014-02-01 10:00:00",
                                                "finish_time": "2014-02-01 10:00:00",
                                                "consumption": 1000,
                                                "status": 0,
                                                "dinner_date": "2014-02-01",
                                                "dinner_time": "12:00",
                                                "dinner_period": 0,
                                                "name": "李四",
                                                "guest_type": "vip",
                                                "contact": "18813101211",
                                                "guest_number": 10,
                                                "banquet": "满月宴",
                                                "desks": [{"desk_id": 1, "number": "309"}, {"desk_id": 2, "number": "312"}, {"desk_id": 3, "number": "311"}],
                                                "user_description": "生日宴，准备蜡烛",
                                                "staff_description": "客户年纪大，做好防滑",
                                                "water_card": "水牌内容",
                                                "door_card": "门牌内容",
                                                "sand_table": "沙盘内容",
                                                "welcome_screen": "欢迎xx领导",
                                                "welcome_fruit": 128,
                                                "welcome_card": "欢迎你",
                                                "pictures": ["http://demo.com/1.jpg", "http://demo.com/2.jpg"],
                                                "background_music": "我爱你中国",
                                                "has_candle": true,
                                                "has_flower": false,
                                                "has_balloon": false,
                                                "group_photo": "合照名称",
                                                "internal_channel": "刘光艳",
                                                "external_channel": "美团"
                                            };
                                            alert(obj.description);
                                        }
                                    });
                                },
                                OperationLog: function (order_id) {
                                    var url = "/webApp/order/log/list/";
                                    var param = {
                                        order_id: order_id
                                    };
                                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                                        if (obj.status === "true") {
                                            $scope.order.log = obj.data;
                                        } else {
                                            $scope.order.log = {count: 0, list: []};
                                            alert("无订单！");
                                        }
                                    });
                                }
                            };
                            Order.OrderDetails(order_id);
                            Order.OperationLog(order_id);
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

    // 【员工】客户管理
    $routeProvider
        .when('/Customer/AnniversaryReport', {
            templateUrl: "./template/Customer/AnniversaryReport.html", controller: function ($scope) {
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
            templateUrl: "./template/Customer/CustomerAnalysis.html", controller: function ($scope, $http) {
                var Color = [
                    '#ffccff', '#ccffcc', '#ffcccc', '#ccccff', '#ffccff', '#ccffcc',
                    '#ffcccc', '#ccccff', '#ffccff', '#ccffcc', '#ffcccc', '#ccccff'
                ];
                var config = {
                    type: 'doughnut', // doughnut
                    data: {
                        datasets: [],
                        labels: ["活跃", "沉睡", "流失", "全部"]
                    },
                    options: {
                        responsive: true,
                        legend: {
                            position: 'top'
                        },
                        title: {
                            display: true,
                            text: '员工客户统计'
                        },
                        animation: {
                            animateScale: true,
                            animateRotate: true
                        }
                    }
                };
                var chart1 = document.getElementById('chart1').getContext('2d');
                var myDoughnut = new Chart(chart1, config);

                // 获取员工的客户统计
                var Staff = {
                    getGuestStatistics: function () {
                        var url = "/webApp/staff/guest/statistic/";
                        var param = {};
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                var rawData = obj.data;
                                var data = [
                                    rawData.active_guest_number,
                                    rawData.sleep_guest_number,
                                    rawData.lost_guest_number,
                                    rawData.all_guest_number
                                ];
                                config.data.datasets.push({data: data, backgroundColor: Color, label: "员工客户统计"});
                                myDoughnut.update();
                            } else {
                                // $scope.data = {count: 0, list: []};
                                alert("无订单！");
                            }
                        });
                    }
                };
                Staff.getGuestStatistics();
            }
        })
        .when('/Customer/CustomerProfiles', {
            templateUrl: "./template/Customer/CustomerProfiles.html", controller: function ($rootScope, $scope, $modal, $http) {
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
                $scope.status = ["全部", "活跃", "沉睡", "流失", "无订单"];
                // 表格数据
                $scope.data = {count: 0, list: []};
                var Guest = {
                    getProfileList: function () {
                        // 获取员工的客户列表（搜索）
                        var url = "/webApp/staff/guest/list/";
                        var param = {
                            search_key: $scope.option.keyword,
                            status: $scope.option.selected_type
                        };
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.data = obj.data;
                            } else {
                                alert("无客户档案");
                            }
                        });
                    }
                };
                // 事件处理
                $scope.query = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    // 获取员工的客户列表（搜索）
                    var url = "/webApp/staff/guest/list/";
                    var param = {
                        search_key: $scope.option.keyword,
                        status: $scope.selected_type
                    };
                    $http.post(url, JSON.stringify(param)).success(function (obj) {
                        if (obj.status === "true") {
                            $scope.data = obj.data;
                        } else {
                            alert("无客户档案");
                        }
                    });
                };
                $scope.member = function () {
                    Log.i(TAG, "会员价值设置");
                };
                $scope.filter = function (index) {
                    $scope.option.selected_type = index;
                    Log.i(TAG, JSON.stringify($scope.option));
                    Guest.getProfileList();
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
                    Log.i(TAG, JSON.stringify($scope.data));
                };
                $scope.move = function () {
                    Log.i(TAG, JSON.stringify($scope.option));
                    $scope.data.forEach(function (item) {
                        if (item.selected) {
                            item.type = $scope.option.to_type;
                        }
                    });
                    Log.i(TAG, JSON.stringify($scope.data));
                };
                $scope.edit = function (guest) {
                    Log.i(TAG, JSON.stringify(guest));
                };
                // 对话框
                $scope.profiles_add = function () {
                    Log.i(TAG, "添加档案");
                    var dlg = $modal.open({
                        templateUrl: "./template/" + Dialog.Customer.CustomerProfiles.AddCustomerProfiles,
                        controller: function ($scope) {
                            Log.i(TAG, "对话框控制器");
                            $scope.form = {
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
                            $scope.types = ["活跃", "沉寂", "流失"];
                            $scope.submit = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                                dlg.close($scope.form);
                            };
                            $scope.cancel = function () {
                                Log.i(TAG, JSON.stringify($scope.form));
                                dlg.dismiss({reason: "取消操作"});
                            }
                        }
                    });
                    dlg.opened.then(function () {
                        Log.i(TAG, "对话框已经打开");
                    });
                    dlg.result.then(function (result) {
                        Log.i(TAG, JSON.stringify(result));
                        var url = "/webApp/guest/profile/add/";
                        var param = angular.copy(result);
                        // 预处理
                        param.phone = JSON.stringify(param.phone);
                        param.like = JSON.stringify(param.like);
                        param.dislike = JSON.stringify(param.dislike);
                        Log.i(TAG, JSON.stringify(param));
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                alert("添加档案成功！");
                            } else {
                                alert(obj.description);
                            }
                        });
                    }, function (reason) {
                        Log.i(TAG, reason);
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
        .when('/Customer/CustomerProfile/:guest_id', {
            templateUrl: "./template/Customer/CustomerProfile.html", controller: function ($routeParams, $rootScope, $scope, $http) {
                var TAG = "/Customer/CustomerProfile";
                var guest_id = $routeParams.guest_id;
                var Guest = {
                    // 获取客户档案详情(根据ID或电话)
                    getProfile: function (guest_id) {
                        var url = "/webApp/guest/profile/";
                        var param = {
                            guest_id: guest_id
                        };
                        Log.i(TAG, JSON.stringify(param));
                        $http.post(url, JSON.stringify(param)).success(function (obj) {
                            if (obj.status === "true") {
                                $scope.form = obj.data;
                            } else {
                                alert("无此客户信息")
                            }
                        });
                    }
                };
                Guest.getProfile(guest_id);
            }
        })
        .when('/Customer/CustomerRecycleBin', {
            templateUrl: "./template/Customer/CustomerRecycleBin.html", controller: function ($scope) {
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
            templateUrl: "./template/Customer/MemberValue.html", controller: function ($scope) {

            }
        });

    // 【员工】账户管理
    $routeProvider
        .when('/Account/AccountManage', {
            templateUrl: "./template/Account/AccountManage.html", controller: function ($scope) {
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
            templateUrl: "./template/Account/FinanceManage.html", controller: function ($scope) {
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
        .when('/Account/SMSDetails', {
            templateUrl: "./template/Account/SMSDetails.html"
        });

    // 【评分员】评分审阅
    $routeProvider
        .when('/Review/Rank', {
            templateUrl: "./template/Review/Rank.html", controller: function ($scope) {
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
        .when('/Review/Scoring', {
            templateUrl: "./template/Review/Scoring.html", controller: function () {

            }
        })
        .when('/Review/Tutorial', {
            templateUrl: "./template/Review/Tutorial.html", controller: function () {

            }
        });

    // 【微课堂】微课堂
    $routeProvider
        .when('/MicroCourse/LiveCourse', {
            templateUrl: "./template/MicroCourse/LiveCourse.html", controller: function () {

            }
        })
        .when('/MicroCourse/LiveVideo', {
            templateUrl: "./template/MicroCourse/LiveVideo.html", controller: function () {

            }
        });

    $routeProvider
        .otherwise({redirectTo: "/SmartOrder/SmartOrder"});
}]);
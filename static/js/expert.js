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
                {value: 0, name: '101', min: 1, max: 16, type: "大厅散台	", order: 1, enable: false},
                {value: 1, name: '102', min: 1, max: 16, type: "豪华包间", order: 2, enable: true},
                {value: 2, name: '111', min: 1, max: 16, type: "大厅散台	", order: 3, enable: false},
                {value: 3, name: '105', min: 1, max: 16, type: "豪华包间", order: 4, enable: true}
            ]
        },
        {
            value: 1, name: '二楼', order: 1, status: 0,
            seat: [
                {value: 0, name: '206', min: 5, max: 16, type: "大厅散台	", order: 5, enable: true},
                {value: 1, name: '207', min: 5, max: 16, type: "豪华包间", order: 6, enable: false},
                {value: 2, name: '208', min: 5, max: 16, type: "大厅散台	", order: 7, enable: true},
                {value: 3, name: '209', min: 5, max: 16, type: "大厅散台	", order: 8, enable: false}
            ]
        },
        {
            value: 2, name: '三楼', order: 2, status: 0,
            seat: [
                {value: 0, name: '306', min: 8, max: 16, type: "豪华包间", order: 9, enable: true},
                {value: 1, name: '307', min: 8, max: 16, type: "大厅散台	", order: 10, enable: false},
                {value: 2, name: '308', min: 8, max: 16, type: "豪华包间", order: 11, enable: true},
                {value: 3, name: '309', min: 8, max: 16, type: "大厅散台	", order: 12, enable: false}
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
    channel: [
        {
            name: "内部渠道",
            items: [
                {value: 1, name: 'A'},
                {value: 2, name: 'B'},
                {value: 3, name: 'C'},
                {value: 4, name: 'D'}
            ]
        },
        {
            name: "外部渠道",
            items: [
                {value: 5, name: 'E'},
                {value: 6, name: 'F'},
                {value: 7, name: 'G'},
                {value: 8, name: 'H'},
                {value: 9, name: 'I'}
            ]
        }
    ],
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
}
;

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

var templates = {};
var log = {
    area: BanquetExpert.area,
    seat: [],
    staff: BanquetExpert.staff,
    channel: BanquetExpert.channel,
    log: [
        {time: 'aa', user: 'bb', type: 'cc', content: 'dd', info: 'ee'},
        {time: 'aa', user: 'bb', type: 'cc', content: 'dd', info: 'ee'},
        {time: 'aa', user: 'bb', type: 'cc', content: 'dd', info: 'ee'},
        {time: 'aa', user: 'bb', type: 'cc', content: 'dd', info: 'ee'},
        {time: 'aa', user: 'bb', type: 'cc', content: 'dd', info: 'ee'},
        {time: 'aa', user: 'bb', type: 'cc', content: 'dd', info: 'ee'}
    ]
};

// 子页面模板
var Templates = {
    Drawer: "Drawer/Drawer.html", // 侧边栏
    Breadcrumb: "Drawer/Breadcrumb.html", // 路径导航
    tabContent: {
        // 后台用户管理
        Channel: {
            Channel: "Channel/Channel.html", // 获客渠道
            Privilege: "Channel/Privilege.html" // 权限管理
        },
        // 智能订餐台
        SmartOrder: {
            SmartOrder: "SmartOrder/SmartOrder.html" // 智能订餐台
        },
        // 预定管理
        Reserve: {
            AreaDesk: "Reserve/AreaDesk.html", // 桌位设置
            MealsTime: "Reserve/MealsTime.html", // 餐段管理
            MealsArea: "Reserve/MealsArea.html", // 餐位设置
            SeatRecommend: "Reserve/SeatRecommend.html" // 自动推荐桌位
        },
        // 订单管理
        Order: {
            InsertOrder: "Order/InsertOrder.html",// 订单金额录入
            OperationLog: "Order/OperationLog.html", // 操作日志
            OrderHistory: "Order/OrderHistory.html",// 历史订单
            OrderStatistics: "Order/OrderStatistics.html",// 订单统计
            PhoneReserve: "Order/PhoneReserve.html", // 来电记录
            ReserveNotice: "Order/ReserveNotice.html" // 预定通知单
        },
        // 客户管理
        Customer: {
            AnniversaryReport: "Customer/AnniversaryReport.html", //
            CustomerAnalysis: "Customer/CustomerAnalysis.html", // 客源情况分析
            CustomerProfiles: "Customer/CustomerProfiles/AddCustomerProfiles.html", // 客户档案列表*** AddCustomerProfiles BatchExport
            CustomerRecycleBin: "Customer/CustomerRecycleBin.html", // 客户档案回收站
            MemberValue: "Customer/MemberValue.html" // 会员价值设置
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
            Tutorial: "Review/Tutorial.html" // 中国服务私人订制标准视频教程
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
    var find = function (obj, key, value) {
        var newObj = false;
        $.each(obj, function () {
            var testObj = this;
            $.each(testObj, function (k, v) {
                if (k === key && value === v) {
                    newObj = testObj;
                }
            });
        });
        return newObj;
    };

    var refreshData = function () {

    }

    // 刷新路径导航
    var refreshBreadcrumb = function (path) {
        var string = path.substr(0, path.length - 5);
        var items = string.split('/');
        var menu = find(BanquetExpert.menus, 'menu_id', items[0]);
        var item = find(menu.item, 'item_id', items[1]);
        while (BanquetExpert.Breadcrumb.length > 1) {
            $.observable(BanquetExpert.Breadcrumb).remove();
        }
        $.observable(BanquetExpert.Breadcrumb).insert({title: menu.title});
        $.observable(BanquetExpert.Breadcrumb).insert({title: item.title});
    };

    // 刷新子页面和更新路径导航
    var refresh = function (path, id, data) {
        if (id === "#main") {
            // 更新路径导航
            refreshBreadcrumb(path);
        }
        // 更新子页面
        var url = "./template/" + path;
        if (templates[url]) {
            // 存在模板
            var modal = templates[url];
            // 绑定模板与视图
            modal.link(id, data);
        } else {
            // 不存在模板
            $.ajax({
                url: url, // 模板路径
                type: "GET", //静态页用get方法，否则服务器会抛出405错误
                success: function (html) {
                    // 转换模板
                    var modal = $.templates(html);
                    templates[url] = modal;
                    // 绑定模板与视图
                    modal.link(id, data);
                }
            });
        }
    };

    // 初始化侧边导航栏/路径导航
    refresh(Templates.Drawer, "#drawer", BanquetExpert.menus);
    refresh(Templates.Breadcrumb, "#breadcrumb", BanquetExpert.Breadcrumb);

    // 设置本地路由
    var routes = {
        // 账户管理
        "/Account/AccountManage": function () {
            refreshBreadcrumb(Templates.tabContent.Account.AccountManage);
            $("main").load("./template/" + Templates.tabContent.Account.AccountManage);
        },
        "/Account/FinanceManage": function () {
            refreshBreadcrumb(Templates.tabContent.Account.FinanceManage);
            $("main").load("./template/" + Templates.tabContent.Account.FinanceManage);
        },
        "/Account/SMSDetails": function () {
            refreshBreadcrumb(Templates.tabContent.Account.SMSDetails);
            $("main").load("./template/" + Templates.tabContent.Account.SMSDetails);
        },
        "/Account/Restaurant": function () {
            refreshBreadcrumb(Templates.tabContent.Account.Restaurant);
            $("main").load("./template/" + Templates.tabContent.Account.Restaurant);
        },
        // 后台用户管理
        "/Channel/Channel": function () {
            refreshBreadcrumb(Templates.tabContent.Channel.Channel);
            $("main").load("./template/" + Templates.tabContent.Channel.Channel);
        },
        "/Channel/Privilege": function () {
            refreshBreadcrumb(Templates.tabContent.Channel.Privilege);
            $("main").load("./template/" + Templates.tabContent.Channel.Privilege);
        },
        // 客户管理
        "/Customer/AnniversaryReport": function () {
            refreshBreadcrumb(Templates.tabContent.Customer.AnniversaryReport);
            $("main").load("./template/" + Templates.tabContent.Customer.AnniversaryReport);
        },
        "/Customer/CustomerAnalysis": function () {
            refreshBreadcrumb(Templates.tabContent.Customer.CustomerAnalysis);
            $("main").load("./template/" + Templates.tabContent.Customer.CustomerAnalysis);
        },
        "/Customer/CustomerProfiles": function () {
            refreshBreadcrumb(Templates.tabContent.Customer.CustomerProfiles);
            $("main").load("./template/" + Templates.tabContent.Customer.CustomerProfiles);
        },
        "/Customer/CustomerRecycleBin": function () {
            refreshBreadcrumb(Templates.tabContent.Customer.CustomerRecycleBin);
            $("main").load("./template/" + Templates.tabContent.Customer.CustomerRecycleBin);
        },
        "/Customer/MemberValue": function () {
            refreshBreadcrumb(Templates.tabContent.Customer.MemberValue);
            $("main").load("./template/" + Templates.tabContent.Customer.MemberValue);
        },
        // 订单管理
        "/Order/InsertOrder": function () {
            refreshBreadcrumb(Templates.tabContent.Order.InsertOrder);
            $("main").load("./template/" + Templates.tabContent.Order.InsertOrder);
        },
        "/Order/OperationLog": function () {
            refreshBreadcrumb(Templates.tabContent.Order.OperationLog);
            $("main").load("./template/" + Templates.tabContent.Order.OperationLog);
        },
        "/Order/OrderHistory": function () {
            refreshBreadcrumb(Templates.tabContent.Order.OrderHistory);
            $("main").load("./template/" + Templates.tabContent.Order.OrderHistory);
        },
        "/Order/OrderStatistics": function () {
            refreshBreadcrumb(Templates.tabContent.Order.OrderStatistics);
            $("main").load("./template/" + Templates.tabContent.Order.OrderStatistics);
        },
        "/Order/PhoneReserve": function () {
            refreshBreadcrumb(Templates.tabContent.Order.PhoneReserve);
            $("main").load("./template/" + Templates.tabContent.Order.PhoneReserve);
        },
        "/Order/ReserveNotice": function () {
            refreshBreadcrumb(Templates.tabContent.Order.ReserveNotice);
            $("main").load("./template/" + Templates.tabContent.Order.ReserveNotice);
        },
        // 预定管理
        "/Reserve/AreaDesk": function () {
            refreshBreadcrumb(Templates.tabContent.Reserve.AreaDesk);
            $("main").load("./template/" + Templates.tabContent.Reserve.AreaDesk);
        },
        "/Reserve/MealsTime": function () {
            refreshBreadcrumb(Templates.tabContent.Reserve.MealsTime);
            $("main").load("./template/" + Templates.tabContent.Reserve.MealsTime);
        },
        "/Reserve/MealsArea": function () {
            refreshBreadcrumb(Templates.tabContent.Reserve.MealsArea);
            $("main").load("./template/" + Templates.tabContent.Reserve.MealsArea);
        },
        "/Reserve/SeatRecommend": function () {
            refreshBreadcrumb(Templates.tabContent.Reserve.SeatRecommend);
            $("main").load("./template/" + Templates.tabContent.Reserve.SeatRecommend);
        },
        // 评分审阅
        "/Review/Rank": function () {
            refreshBreadcrumb(Templates.tabContent.Review.Rank);
            $("main").load("./template/" + Templates.tabContent.Review.Rank);
        },
        "/Review/Tutorial": function () {
            refreshBreadcrumb(Templates.tabContent.Review.Tutorial);
            $("main").load("./template/" + Templates.tabContent.Review.Tutorial);
        },
        // 智能订餐台
        "/SmartOrder/SmartOrder": function () {
            refreshBreadcrumb(Templates.tabContent.SmartOrder.SmartOrder);
            $("main").load("./template/" + Templates.tabContent.SmartOrder.SmartOrder);
        }
    };
    var router = window.Router(routes);
    router.init();

});
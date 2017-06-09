/**
 * Created by 本山 on 2017/5/31.
 */
/**
 * 全局变量：记录所有固定的内容
 *
 * @type {{area: [区域], staff: [操作员], channel: {inner: [内部渠道], outer: [外部渠道]}}}
 */
var BanquetExpert = {
    area: [
        {
            value: 0, name: '一楼',
            seat: [
                {value: 0, name: '101', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 1, name: '102', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 2, name: '111', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 3, name: '105', min: 12, max: 16, type: "豪华包间", order: 1}
            ]
        },
        {
            value: 1, name: '二楼',
            seat: [
                {value: 0, name: '206', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 1, name: '207', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 2, name: '208', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 3, name: '209', min: 12, max: 16, type: "豪华包间", order: 1}
            ]
        },
        {
            value: 2, name: '三楼',
            seat: [
                {value: 0, name: '306', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 1, name: '307', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 2, name: '308', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 3, name: '309', min: 12, max: 16, type: "豪华包间", order: 1}
            ]
        },
        {
            value: 3, name: '五楼',
            seat: [
                {value: 0, name: '506', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 1, name: '507', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 2, name: '508', min: 12, max: 16, type: "豪华包间", order: 1},
                {value: 3, name: '509', min: 12, max: 16, type: "豪华包间", order: 1}
            ]
        }
    ],
    staff: [
        {value: 0, name: 'aaa'},
        {value: 0, name: 'bbb'}
    ],
    channel: {
        inner: [
            {value: 3, name: 'B'},
            {value: 3, name: 'B'},
            {value: 3, name: 'B'},
            {value: 3, name: 'B'}
        ],
        outer: [
            {value: 3, name: 'A'},
            {value: 3, name: 'A'},
            {value: 3, name: 'A'},
            {value: 3, name: 'A'},
            {value: 3, name: 'A'},
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
                {title: "设置桌位对应关系", item_id: "AreaDeskRelation"},
                {title: "餐段设置", item_id: "MealsTime"},
                {title: "餐位设置", item_id: "MealsArea"},
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
                {title: "餐厅基本信息", item_id: "Restaurant"},
                {title: "修改密码", item_id: "AccountManage"}
            ]
        },
        {
            title: "评分审阅",
            menu_id: "Review",
            item: [
                {title: "餐厅排名", item_id: "Rank"},
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
            AreaDeskRelation: "Reserve/AreaDeskRelation.html", // 设置桌位对应关系
            AreaDesk: "#", // 【餐位设置】桌位设置
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
            CustomerProfiles: "Customer/CustomerProfiles.html", // 客户档案列表
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

$(document).ready(function () {

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

    refresh(Templates.Drawer, "#drawer", BanquetExpert);
    refresh(Templates.Breadcrumb, "#breadcrumb", BanquetExpert);

    var routes = {
        // 账户管理
        "/Account/AccountManage": function () {
            refresh(Templates.tabContent.Account.AccountManage, "#main");
        },
        "/Account/FinanceManage": function () {
            refresh(Templates.tabContent.Account.FinanceManage, "#main");
        },
        "/Account/SMSDetails": function () {
            refresh(Templates.tabContent.Account.SMSDetails, "#main");
        },
        "/Account/Restaurant": function () {
            refresh(Templates.tabContent.Account.Restaurant, "#main");
        },
        // 后台用户管理
        "/Channel/Channel": function () {
            refresh(Templates.tabContent.Channel.Channel, "#main");
        },
        "/Channel/Privilege": function () {
            refresh(Templates.tabContent.Channel.Privilege, "#main");
        },
        // 客户管理
        "/Customer/AnniversaryReport": function () {
            refresh(Templates.tabContent.Customer.AnniversaryReport, "#main");
        },
        "/Customer/CustomerAnalysis": function () {
            refresh(Templates.tabContent.Customer.CustomerAnalysis, "#main");
        },
        "/Customer/CustomerProfiles": function () {
            refresh(Templates.tabContent.Customer.CustomerProfiles, "#main");
        },
        "/Customer/CustomerRecycleBin": function () {
            refresh(Templates.tabContent.Customer.CustomerRecycleBin, "#main");
        },
        "/Customer/MemberValue": function () {
            refresh(Templates.tabContent.Customer.MemberValue, "#main");
        },
        // 订单管理
        "/Order/InsertOrder": function () {
            refresh(Templates.tabContent.Order.InsertOrder, "#main");
        },
        "/Order/OperationLog": function () {
            refresh(Templates.tabContent.Order.OperationLog, "#main");
        },
        "/Order/OrderHistory": function () {
            refresh(Templates.tabContent.Order.OrderHistory, "#main");
        },
        "/Order/OrderStatistics": function () {
            refresh(Templates.tabContent.Order.OrderStatistics, "#main");
        },
        "/Order/PhoneReserve": function () {
            refresh(Templates.tabContent.Order.PhoneReserve, "#main");
        },
        "/Order/ReserveNotice": function () {
            refresh(Templates.tabContent.Order.ReserveNotice, "#main");
        },
        // 预定管理
        "/Reserve/AreaDeskRelation": function () {
            refresh(Templates.tabContent.Reserve.AreaDeskRelation, "#main");
        },
        "/Reserve/MealsTime": function () {
            refresh(Templates.tabContent.Reserve.MealsTime, "#main");
        },
        "/Reserve/MealsArea": function () {
            refresh(Templates.tabContent.Reserve.MealsArea, "#main");
        },
        "/Reserve/SeatRecommend": function () {
            refresh(Templates.tabContent.Reserve.SeatRecommend, "#main");
        },
        // 评分审阅
        "/Review/Rank": function () {
            refresh(Templates.tabContent.Review.Rank, "#main");
        },
        "/Review/Tutorial": function () {
            refresh(Templates.tabContent.Review.Tutorial, "#main");
        },
        // 智能订餐台
        "/SmartOrder/SmartOrder": function () {
            refresh(Templates.tabContent.SmartOrder.SmartOrder, "#main");
        }
    };

    var router = window.Router(routes);
    router.init();
});
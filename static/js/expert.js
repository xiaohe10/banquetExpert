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
                {value: 0, name: '101', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 1, name: '102', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 2, name: '111', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 3, name: '105', min: 12, max: 16, type:"豪华包间", order:1}
            ]
        },
        {
            value: 1, name: '二楼',
            seat: [
                {value: 0, name: '206', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 1, name: '207', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 2, name: '208', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 3, name: '209', min: 12, max: 16, type:"豪华包间", order:1}
            ]
        },
        {
            value: 2, name: '三楼',
            seat: [
                {value: 0, name: '306', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 1, name: '307', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 2, name: '308', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 3, name: '309', min: 12, max: 16, type:"豪华包间", order:1}
            ]
        },
        {
            value: 3, name: '五楼',
            seat: [
                {value: 0, name: '506', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 1, name: '507', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 2, name: '508', min: 12, max: 16, type:"豪华包间", order:1},
                {value: 3, name: '509', min: 12, max: 16, type:"豪华包间", order:1}
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
    menu: [
        {
            title: "后台用户管理",
            id: "user",
            item: [
                {title: "获客渠道", url: "#"},
                {title: "用户权限管理", url: "#"}
            ]
        },
        {
            title: "预订管理",
            id: "reservation",
            item: [
                {title: "设置桌位对应关系", url: "#", template: "./template/reservation/desk.html"},
                {title: "餐段设置", url: "#", template: "./template/reservation/meal-period.html"},
                {title: "餐位设置", url: "#", template: "./template/reservation/seat.html"},
                {title: "自动推荐桌位", url: "#", template: "./template/reservation/recommend.html"}
            ]
        },
        {
            title: "订单管理",
            id: "order",
            item: [
                {title: "预定通知单", url: "#", template: "./template/order/reservation.html"},
                {title: "历史订单", url: "#", template: "./template/order/history.html"},
                {title: "订单金额录入", url: "#"},
                {title: "订单统计", url: "#", template: "./template/order/statistics.html"},
                {title: "来电记录", url: "#", template: "./template/order/record.html" },
                {title: "操作日志", url: "#", template: "./template/order/log.html"}
            ]
        },
        {
            title: "客户管理",
            item: [
                {title: "客户档案列表", url: "#"},
                {title: "客源情况分析", url: "#"},
                {title: "会员价值设置", url: "#"},
                {title: "客户档案回收站", url: "#"},
                {title: "纪念日查询报表", url: "#"}
            ]
        }
    ]
};
var templates = {};
var url = "log";
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
var options = {
    drawer: {
        url: "./template/drawer/drawer.html",
        update: function (template) {
            $("#menu").html(template.render(BanquetExpert));
        }
    },
    area: {
        url: "",
        update: function (template) {
            $("#menu").html(template.render(BanquetExpert));
        }
    },
    log: {
        url: "./template/order/log.html",
        update: function (template) {
            $("#menu").html(template.render(BanquetExpert));
            alert("渲染log")
            // template.link("#content", log);
        }
    }
};
$(document).ready(function () {
    var refresh = function (url, update) {
        if (templates[url]) {
            // 存在模板
            var template = templates[url];
            // 绑定模板与视图
            update(template);
        } else {
            // 不存在模板
            $.ajax({
                url: url, // 模板路径
                type: "GET", //静态页用get方法，否则服务器会抛出405错误
                success: function (data) {
                    // 转换模板
                    var template = $.template(data);
                    templates[url] = template;
                    // 绑定模板与视图
                    update(template);
                }
            });
        }
    };
    refresh(options.drawer.url, options.drawer.update);
    refresh(options.log.url, options.log.update);
});
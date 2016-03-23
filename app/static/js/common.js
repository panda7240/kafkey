// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};
var common = {

    //EasyUI用DataGrid用日期格式化
    dateTimeFormatter: function (value, rec, index) {
        var date = new Date(value);
        return date.Format("yyyy-MM-dd hh:mm:ss");
    },

    //zipkin模块用Grid用日期格式化
    zipKinDateTimeFormatter: function (value, rec, index) {
        var date = new Date(value);
        return date.Format("yyyy-MM-dd hh:mm:ss.S");
    },
    showCenter: function (title, msg) {
        $.messager.show({
            title: title,
            msg: msg,
            showType: 'fade',
            style: {
                right: '',
                bottom: ''
            }
        });
    },
    showNoSelectRow: function () {
        common.showCenter("提示！", "没有选中任何行！");
    },
    showOptionSuccess: function () {
        common.showCenter("提示！", "操作成功！");
    },
    showOptionFail: function () {
        common.showCenter("提示！", "操作失败！可能数据已经发生变化，请刷新后重新操作！");
    },
    formatInvokeCount: function (val, row) {
        var successCount = 0;
        var errorCount = 0;
        if (val) {
            successCount = val;
        }
        if (row.invokeCountError) {
            errorCount = row.invokeCountError;
        }
        if (errorCount > 0) {
            return successCount + '/<span style="color:red;">' + errorCount + '</span>';
        } else {
            return successCount + '/0';
        }
    },

    formatLongLine: function (val, row) {
        if (val.length > 70) {
            return val.substring(0, 67) + "..."
        } else {
            return val;
        }
    },
    datetimeboxFormatter2: function (date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        var h = date.getHours();
        var mi = date.getMinutes();
        var s = date.getSeconds();
        var ms = date.getMilliseconds();
        return y + '-' + (m < 10 ? ('0' + m) : m) + '-' + (d < 10 ? ('0' + d) : d)
            + " "
            + (h < 10 ? ('0' + h) : h) + ":" + (mi < 10 ? ('0' + mi) : mi) + ":" + (s < 10 ? ('0' + s) : s);
//            + "." + (ms<10?('00'+ms):(ms<100?('0'+ms):ms));
    },
    datetimeboxFormatter: function (date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        var h = date.getHours();
        var mi = date.getMinutes();
        var s = date.getSeconds();
        var ms = date.getMilliseconds();
        return y + '/' + (m < 10 ? ('0' + m) : m) + '/' + (d < 10 ? ('0' + d) : d)
            + " "
            + (h < 10 ? ('0' + h) : h) + ":" + (mi < 10 ? ('0' + mi) : mi) + ":" + (s < 10 ? ('0' + s) : s);
//            + "." + (ms<10?('00'+ms):(ms<100?('0'+ms):ms));
    },
    detetimeboxParser: function (s) {
        //                s = s.replace(".",":");
        if (s.split(" ").length == 2) {
            var arrs = s.split(" ")[0].split("/");
            var tmp = new Date();
            tmp.setMilliseconds(0);
            if (arrs.length == 3) {
                tmp.setFullYear(arrs[0]);
                tmp.setMonth(+arrs[1] - 1);
                tmp.setDate(arrs[2]);
            }
            arrs = s.split(" ")[1].split(":");
            if (arrs.length == 3) {
                tmp.setHours(+arrs[0]);
                tmp.setMinutes(+arrs[1]);
                tmp.setSeconds(+arrs[2]);
                //                        tmp.setMilliseconds(+arrs[3]);
            }
        }
        if (new Date() < tmp) {
            //tmp 不合法
            return common.newStartDateOneHourBefore();
        }
        return tmp;
    },
    detetimeboxEndParser: function (s) {
        //                s = s.replace(".",":");
        if (s.split(" ").length == 2) {
            var arrs = s.split(" ")[0].split("/");
            var tmp = new Date();
            tmp.setMilliseconds(0);
            if (arrs.length == 3) {
                tmp.setFullYear(arrs[0]);
                tmp.setMonth(+arrs[1] - 1);
                tmp.setDate(arrs[2]);
            }
            arrs = s.split(" ")[1].split(":");
            if (arrs.length == 3) {
                tmp.setHours(+arrs[0]);
                tmp.setMinutes(+arrs[1]);
                tmp.setSeconds(+arrs[2]);
                //                        tmp.setMilliseconds(+arrs[3]);
            }
        }
        var ed = new Date();
        ed.setHours(24);
        ed.setMinutes(0);
        ed.setSeconds(0);
        ed.setMilliseconds(0);
        if (ed < tmp) {
            return ed;
        }
        return tmp;
    },
    newStartDate: function () {
        var d = new Date();
        d.setHours(0);
        d.setMinutes(0);
        d.setSeconds(0);
        d.setMilliseconds(0);
        return d;
    },
    newStartDateOneHourBefore: function () {
        var d = new Date();
        d.setHours(d.getHours() - 1);
        d.setMinutes(0);
        d.setSeconds(0);
        d.setMilliseconds(0);
        return d;
    },
    newEndDate: function () {
        var d = new Date();
        d.setHours(24);
        d.setMinutes(0);
        d.setSeconds(0);
        d.setMilliseconds(0);
        return d;
    },

    logPanelScroll: function (id) {
        var ul_module = $('ul#' + id);
        var seleted_li = ul_module.find('li.hlight');
        var prevCount = seleted_li.prevAll();
        if (prevCount.length) {
            var sh = 0;
            for (var i = 0; i < prevCount.length; i++) {
                sh += $(prevCount[i]).height();
            }
            if (sh) {
                ul_module.parent().scrollTop(sh + 5 * prevCount.length - 170);
//                ZZZ = ul_module.parent();
//                console.log(prevCount.length)
//                console.log(sh)
            }
        }
    },

    dateTimeToString: function (date) {//"yyyy-MM-dd hh:mm:ss"

        var year = date.getFullYear();       //年
        var month = date.getMonth() + 1;     //月
        var day = date.getDate();            //日

        var hh = date.getHours();            //时
        var mm = date.getMinutes();          //分

        var clock = year + "-";

        if (month < 10)
            clock += "0";

        clock += month + "-";

        if (day < 10)
            clock += "0";

        clock += day + " ";

        if (hh < 10)
            clock += "0";

        clock += hh + ":";
        if (mm < 10) clock += '0';
        clock += mm;
        return (clock);
    }


};

String.prototype.toDate = function () {
    var temp = this.toString();

    temp = temp.replace(/-/g, "/");

    var date = new Date(Date.parse(temp));

    return date;
};


createTabPanelForChildren = function (title, href) {

    //获取tab
    var iframeName = "link_iframeName";
    var $main_tabs = parent.$('#tabs');
    var tab = $main_tabs.tabs('getTab', title);
    if (tab) {
        $main_tabs.tabs('select', title);
        iframeName += $main_tabs.tabs('getTabIndex', tab);
        parent.$("#" + iframeName).attr('src', href);
        return;
    }
    //如果存在，激活
    iframeName += $main_tabs.tabs('tabs').length.toString();
    var content = '<iframe id="' + iframeName + '" name="' + iframeName + '" src="' + href + '" frameborder="0" width="100%" height="99.5%"></iframe>';
    //嵌入的其他链接
    $main_tabs.tabs('add', {
        title: title,
        content: content,
        closable: true,
        tools: [
            {
                iconCls: 'icon-reload',
                handler: function () {
                    parent.$("#" + iframeName).attr('src', href);
                }
            }
        ]
    });

};
import xadmin
from finance.models import FinanceRecord


@xadmin.sites.register(FinanceRecord)
class FinancRecordXAdmin:
    list_display = ('record_time', 'balance', 'debt', 'other', 'summary', 'describe')
    list_editable = ('describe', )

    list_filter = ('user__username', 'record_time')

    search_fields = ('user__username', 'describe')

    # 在对应的字段数据上显示一个详情的接口
    show_detail_fields = ['record_time']

    exclude = ['user', 'summary']

    # 提供一个自动刷新的接口：可选择5s或10s刷新
    refresh_times = (5, 10)

    # 导出模型数据类型，这个默认支持4种导出类型
    list_export = ('xls', 'xml', 'json')
    # 导出字段
    # list_export_fields = ()

    # 根据数据绘制图表
    data_charts = {
        "summary": {
            'title': u"余额",
            "x-field": "record_time",
            "y-field": ("summary",),  # 支持多条数据线
           },
    }

    def debt(self, obj):
        return obj.huabei_debt + obj.credit_debt

    def balance(self, obj):
        return obj.alipay_balance + obj.wechat_balance + obj.paycard_balance

    balance.short_description = '剩余资金'
    debt.short_description = '欠款'

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(user=request.user)

    def save_models(self, *args, **kwargs):
        self.new_obj.user = self.request.user
        return super().save_models(*args, **kwargs)


# xadmin的全局配置
from xadmin import views


# 全局配置
class GlobalSettings(object):
    # 修改title
    site_title = 'OfferHelp个人自助平台'
    # 修改footer
    site_footer = 'power by Master-Sun'
    # 设置左侧的菜单有下拉菜单的效果
    menu_style = 'accordion'
    # 设置左侧菜单栏实体类对应的图标
    global_search_models = (FinanceRecord,)
    # 设置对应的图标，图标参考：https://v3.bootcss.com/components/#glyphicons-glyphs
    global_models_icon = {
        FinanceRecord: "glyphicon glyphicon-check"
    }


# 将全局配置信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)

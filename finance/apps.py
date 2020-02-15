from django.apps import AppConfig


class FinanceConfig(AppConfig):
    name = 'finance'
    # xadmin的左侧会显示app及app中注册过的model，默认显示上面的name
    # 通过在这里设置verbose_name进行修改，修改后再去对应app的__init__.py中进行配置
    verbose_name = '金融服务'

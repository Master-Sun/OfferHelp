from django.contrib import admin
from finance.models import FinanceRecord


# Register your models here.
@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    list_display = ("alipay_balance", 'wechat_balance', 'paycard_balance', 'huabei_debt',
                    'credit_debt', 'other', 'summary', 'user', 'record_time')

    list_filter = ('user', )
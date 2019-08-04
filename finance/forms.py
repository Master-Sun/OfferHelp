from django import forms

from finance.models import FinanceRecord


class FinanceRecordForm(forms.ModelForm):
    alipay_balance = forms.DecimalField(label='支付宝余额')
    wechat_balance = forms.DecimalField(label='微信余额')
    paycard_balance = forms.DecimalField(label='工资卡余额')
    huabei_debt = forms.DecimalField(label='花呗欠款')
    credit_debt = forms.DecimalField(label='信用卡欠款')
    other = forms.DecimalField(label='其他', required=False)
    describe = forms.CharField(label='其他状况说明', widget=forms.TextInput, max_length=512, required=False)

    class Meta:
        model = FinanceRecord
        fields = ['alipay_balance', 'wechat_balance', 'paycard_balance', 'huabei_debt', 'credit_debt', 'other', 'describe']



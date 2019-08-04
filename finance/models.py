from django.db import models

from user.models import UserProfile


# Create your models here.
# 流水记录模型
class FinanceRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    alipay_balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='支付宝余额')
    wechat_balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='微信余额')
    paycard_balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='工资卡余额')
    huabei_debt = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='花呗欠款')
    credit_debt = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='信用卡欠款')
    other = models.DecimalField(max_digits=8, decimal_places=2, default=0.00,verbose_name='其他财务')
    describe = models.CharField(max_length=512, verbose_name='其他财务状况说明', blank=True, null=True)
    summary = models.CharField(max_length=256, verbose_name='合计余额')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    def __str__(self):
        return self.user.username

    # 重写模型的save方法，设置summary字段
    def save(self, *args, **kwargs):
        self.summary = self.alipay_balance + self.wechat_balance + self.paycard_balance + self.huabei_debt + self.credit_debt + \
            self.other
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '流水记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    @classmethod
    def get_record(cls, user):
        return FinanceRecord.objects.filter(user=user)
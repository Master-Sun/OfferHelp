from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.utils import timezone


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="昵称")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    TYPE_ITEMS = (
        (1, '激活'),
        (2, '找回密码')
    )

    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    code = models.CharField(max_length=256, verbose_name='验证码')
    code_type = models.PositiveIntegerField(choices=TYPE_ITEMS, verbose_name='验证码类型')
    email = models.EmailField(verbose_name='邮箱')
    expire_time = models.DateTimeField(verbose_name='过期时间')

    def __str__(self):
        return '<%s：%s>' % (self.user.username, self.code)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    # 重写save方法，保存对象时expire字段自动赋值为 当前时间+1min
    # settings中设置时区后datetime.datetime.now()得到的是不带时区的时间(naive time)，此时会有警告
    # 换成django中的timezone即可
    def save(self, *args, **kwargs):
        self.expire_time = timezone.now() + timezone.timedelta(seconds=60)
        super().save(*args, **kwargs)




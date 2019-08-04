from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="昵称")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

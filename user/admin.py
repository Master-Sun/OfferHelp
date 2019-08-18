from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from user.models import UserProfile, EmailVerifyRecord


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", 'nick_name', 'email', 'date_joined', '操作')

    # 自定义显示的字段
    def 操作(self, obj):
        return format_html("<a href={}>删除</a>", reverse("admin:user_userprofile_delete", args=(obj.id,)))

    # 用来搜索的字段
    search_fields = ('username', 'nick_name')

    # 右侧过滤的菜单
    list_filter = ("date_joined",)


@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'code_type', 'email', 'expire_time')
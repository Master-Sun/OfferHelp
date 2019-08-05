from django.contrib import admin
from netdisk.models import Directory, UploadFile


# Register your models here.
@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'dir_name', 'parent_dir_id', 'create_time')

    list_filter = ('user',)


@admin.register(UploadFile)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('dir', 'file_path', 'file_name', 'file_size', 'file_type', 'upload_time')

    list_filter = ('file_type', 'dir__user')    # 通过双下划线，指定显示关联类中对应的字段



from django.contrib import admin
from netdisk.models import Directory


# Register your models here.
@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'dir_name', 'parent_dir_id', 'create_time')

    list_filter = ('user',)



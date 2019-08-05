import os

import time
from django.db import models

from user.models import UserProfile

import uuid


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_name = '%s.%s' %(uuid.uuid1(), ext)
    path = os.path.join('file', '%Y', '%m', new_name)
    return time.strftime(path)


# Create your models here.
class Directory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    dir_name = models.CharField(max_length=256, verbose_name='目录名')
    parent_dir_id = models.CharField(max_length=128, verbose_name='上级目录')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '<%s：%s>' % (self.user.username, self.dir_name)

    class Meta:
        verbose_name = '目录信息表'
        verbose_name_plural = verbose_name

    def get_files(self):
        return UploadFile.objects.filter(dir=self)

    def get_dirs(self):
        return Directory.objects.filter(parent_dir_id=self.id)


class UploadFile(models.Model):
    dir = models.ForeignKey(Directory, verbose_name='所属目录', on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    file_path = models.FileField(upload_to=upload_to, verbose_name='存储路径')
    file_name = models.CharField(max_length=256, verbose_name='文件名')
    file_size = models.CharField(max_length=256, verbose_name='文件大小')
    file_type = models.CharField(max_length=128, verbose_name='文件类型')

    def __str__(self):
        return '<%s：%s>' % (self.dir.user.username, self.file_name)

    class Meta:
        verbose_name = '上传文件信息表'
        verbose_name_plural = verbose_name


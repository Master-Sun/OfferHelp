import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, redirect, reverse

from netdisk.models import Directory, UploadFile


# Create your views here.
@login_required
def index(request):
    root = Directory.objects.get(user=request.user, parent_dir_id=0)
    dirs = root.get_dirs()
    files = root.get_files()
    context = {
        'dirs': dirs,
        'files': files,
        'root': root,
    }
    return render(request, 'netdisk/index.html', context=context)


def upload(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        print(dir(file_obj))
        file_name = file_obj.name
        ext = file_name.split('.')[-1]

        upload_file = UploadFile()
        upload_file.file_name = file_name
        upload_file.file_path = file_obj
        upload_file.file_size = file_obj.size
        upload_file.file_type = ext

        dir_id = request.POST.get('dir_id')
        upload_file.dir = Directory.objects.get(id=dir_id)
        upload_file.save()
        return redirect(reverse('netdisk:entry_dir', args=(dir_id,)))


def create_dir(request):
    present_dir_id = request.POST.get('present_dir_id')
    dir_name = request.POST.get('dir_name')
    print(present_dir_id, dir_name)
    new_dir = Directory()
    new_dir.user = request.user
    new_dir.dir_name = dir_name
    new_dir.parent_dir_id = present_dir_id
    new_dir.save()
    return redirect(reverse('netdisk:entry_dir', args=(present_dir_id,)))


def entry_dir(request, dir_id):
    root = Directory.objects.get(id=dir_id, user=request.user)
    files = root.get_files()
    dirs = root.get_dirs()
    context = {
        'dirs': dirs,
        'files': files,
        'root': root,
    }
    return render(request, 'netdisk/index.html', context=context)


def delete_file(request):
    file_id = request.GET.get('file_id')
    file_obj = UploadFile.objects.filter(id=file_id)
    if file_obj:
        if file_obj[0].dir.user == request.user:
            file_obj[0].delete()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'fail', 'msg': '无权删除他人文件'})
    else:
        return HttpResponse({'result': 'fail', 'msg': '文件已删除或已删除'})



from django.shortcuts import render

from netdisk.models import Directory, UploadFile


# Create your views here.
def index(request):
    root = Directory.objects.filter(user=request.user)
    # dirs = root[0].get_root_dirs()
    # files = root[0].get_files()
    context = {
        # 'dirs': dirs,
        # 'files': files,
    }
    return render(request, 'netdisk/index.html', context=context)
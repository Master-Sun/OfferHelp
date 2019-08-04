from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render
from user.forms import UserRegisterForm, LoginForm

from netdisk.models import Directory


# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            # 根据提交的表单创建新的用户对象，但暂时不保存到数据库
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            auth.login(request, new_user)
            new_dir = Directory(user=new_user, dir_name='/', parent_dir_id='0')
            new_dir.save()
            return render(request, 'index.html')
    else:
        register_form = UserRegisterForm()
    return render(request, 'register.html', {"register_form": register_form})


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = auth.authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return render(request, 'index.html')
#             else:
#                 return render(request, 'registration/login.html', {'form': form})
#     else:
#         form = LoginForm()
#         return render(request, 'registration/login.html', {'form': form})


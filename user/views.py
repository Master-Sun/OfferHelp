import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import UserRegisterForm, LoginForm
from netdisk.models import Directory

import random, string

from django.utils import timezone

from OfferHelp.settings import EMAIL_FROM
from django.core.mail import send_mail

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# Create your views here.
from user.models import EmailVerifyRecord, UserProfile


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            # 会自动验证图形验证码是否正确
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


# 生成指定位数的验证码
def random_str(length=4):
    base_str = string.ascii_letters + string.digits
    rnd_list = random.sample(base_str, length)
    rnd_str = ''.join(rnd_list)
    return rnd_str


# 生成图形验证码django-simple-captcha
def captcha():
    # 生成hash码，对应一个验证码：7a1625794ea4b650eea3e8ae3e7c4712501509e8
    hash_key = CaptchaStore.generate_key()
    # 通过hash码得到验证码图片的url：/captcha/image/7a1625794ea4b650eea3e8ae3e7c4712501509e8/
    image_url = captcha_image_url(hash_key)
    return {'hash_key': hash_key, 'image_url': image_url}


# 提供验证码的刷新
def refresh_captcha(request):
    # application/json：告诉浏览器这是一个json格式的数据，不然他会当成字符串的
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


@login_required
def active_email(request):
    if request.method == 'GET':
        context = captcha()
        return render(request, 'active_email.html', context=context)
    else:
        email = request.POST.get('email')
        active_code = request.POST.get('active_code')
        context = {}

        # 判断是否有未过期的验证码存在
        active_result = EmailVerifyRecord.objects.filter(email=email, code=active_code, code_type=1, user=request.user,
                                               expire_time__gte=timezone.now()).exists()

        verify_code = request.POST.get('verify_code')
        hash_key = request.POST.get('hash_key')

        get_captcha = CaptchaStore.objects.get(hashkey=hash_key)
        # response拿到的是小写的
        captcha_result = (get_captcha.response == verify_code.lower())

        if active_result:
            if captcha_result:
                UserProfile.objects.filter(id=request.user.id).update(email=email)
                return redirect(reverse('user:active_email'))
            else:
                context.update({'verify_message': '验证码错误或已过期'})
        else:
            context.update({'active_message': '激活码错误或已过期'})
        context.update(captcha())
        return render(request, 'active_email.html', context=context)


@login_required
def send_active_code(request):
    email = request.POST.get('email')
    if email:
        is_exist = UserProfile.objects.filter(email=email).exists()
        if is_exist:
            return HttpResponse('该邮箱已注册')
        active_code = random_str(4)
        subject = '主题：邮箱激活'
        message = ''    # 邮件正文
        html_message = '<h1>激活码：%s，有效期：1分钟</h1>' % active_code
        # fail_silently设置为False时，邮件发送失败时将抛出异常
        # send_mail：发送单封邮件，返回值为成功发送邮件的数量，一般返回1
        # 设置了html_message将不再显示message的内容，可以直接传一个空字符串
        result = send_mail(subject, message, EMAIL_FROM, [email,], fail_silently=False, html_message=html_message)
        print(result)
        EmailVerifyRecord.objects.create(
            user=request.user,
            code=active_code,
            code_type=1,
            email=email,
        )
    return HttpResponse('验证码已发送')
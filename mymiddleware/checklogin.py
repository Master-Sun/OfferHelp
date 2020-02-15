from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.utils.deprecation import MiddlewareMixin

import re


class MyMiddleWare(MiddlewareMixin):
    # 在请求和路由之间 执行，
    def process_request(self, request):
        # print('中间件MyMiddleWare，process_request方法被调用')
        # 访问 /finance下的url 进行登陆验证，若未登陆则重定向到登陆页面
        if re.match(r'^/finance', request.path_info) and (not request.user.is_authenticated):
            return HttpResponseRedirect('/user/login/')
        return None
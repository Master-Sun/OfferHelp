"""OfferHelp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import TemplateView

from rest_framework.routers import DefaultRouter
from finance.apis import FinanceViewSet
from rest_framework.documentation import include_docs_urls

# 创建router代理一整套的restful接口
router = DefaultRouter()
router.register(r'finance', FinanceViewSet, base_name='api-finance')

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),    # 语言切换的接口
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='finance_restful_doc')),
    path('admin/', admin.site.urls),
    path('', xadmin.site.urls, name='xadmin_site'),  # name：用于当前url方向解析，namespace则代表还有下级url
    path('user/', include('user.urls', namespace='user')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('index', TemplateView.as_view(template_name='index.html'), name='index'),
    path('netdisk/', include('netdisk.urls', namespace='netdisk')),
    path('captcha/', include('captcha.urls')),    # 图形验证码的路由映射
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

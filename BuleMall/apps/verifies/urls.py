from django.urls import path, re_path
from apps.verifies import views

urlpatterns = [

    # 图片验证码 - 接收前端的UUID参数
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),

    # 短信验证码 - 接收用户表单中的手机号 - 需要校验
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),

]

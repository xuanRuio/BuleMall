import re

from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View


# 用户注册
from BuleMall.settings.dev import LOGGER
from apps.users.models import User


class RegisterView(View):

    def get(self, request):
        return render(request,'register.html')

    def post(self, request):
        """ 1.接收解析参数 """
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        """ 2.校验参数 """
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden("缺少参数！")
        if not re.match('^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden("请输入5-20个字符的用户名")
        if not re.match('^[0-9A-Za-z]{8,20}$',password):
            return http.HttpResponseForbidden("请输入8-20位的密码")
        if password2 != password:
            return http.HttpResponseForbidden("两次输入密码不一致")
        if not re.match('^1[345789]\d{9}$',mobile):
            return http.HttpResponseForbidden("请输入正确的手机号码")

        """ 短信验证码 """
        # 1.获取用户表单中的短信验证码
        sms_code = request.POST.get('msg_code')

        # 2.获取数据库中的短信验证码
        from django_redis import get_redis_connection
        sms_client = get_redis_connection('sms_code')
        sms_code_redis = sms_client.get('sms_%s' % mobile)

        # 3.判断是否存在 - 无验证码 - 返回错误结果
        if sms_code_redis is None:
            return render(request,'register.html',{'sms_code_errmsg':'无效的短信验证码'})
        # 4.判断是否存在 - 有验证码 - 删除此验证码
        sms_client.delete('sms_%s' % mobile)

        # 5.判断用户的验证码是否正确
        if sms_code != sms_code_redis.decode():
            return render(request,'register.html',{'sms_code_errmsg':'短信验证码有误'})

        if allow != 'on':
            return http.HttpResponseForbidden("请勾选协议")

        # 注册用户入库 - 注意自定义User类 - form apps.users.models import User
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            LOGGER.error(e)
            return render(request, 'register.html')

        # 保持登陆状态  from django.contrib.auth import login
        login(request, user)

        response = redirect(reverse("index:index_page"))
        response.set_cookie("username", user.username, max_age=3600 * 15 * 24)
        return response

# 判断用户名是否重复 - ajax请求
class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # 返回json数据,前端接收返回值count,进行判断用户名是否重复
        return http.JsonResponse({'code':'0','errmsg':'ok',"count":count})


# 判断手机号是否重复 - ajax请求
class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code':'0','errmsg':'ok',"count":count})


# 登陆页面
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 接收表单参数
        username = request.POST.get("username")
        password = request.POST.get("password")
        remembered = request.POST.get("remembered")

        # 判空校验
        if not all([username, password]):
            return http.HttpResponseForbidden("参数不齐全")

        # 校验用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden("请输入5-20个字符的用户名")

        # 校验密码
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden("请输入8-20位的密码")

        from django.contrib.auth import authenticate
        # authenticate - django自带验证方法返回当前user对象
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, "login.html", {'account_errmsg':'用户名或者密码错误,请检查！'})

        # 保持登陆状态 - django自带login()方法
        login(request, user)

        # 记住登录选项
        if remembered == "on":
            request.session.set_expiry(None)
        else:
            # 默认时间
            request.session.set_expiry(0)

        # 跳转首页
        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            response = redirect(reverse("index:index_page"))
        response.set_cookie("username", user.username, max_age=24*14*36)
        return response

# 退出登录
class LogoutView(View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        # 清空Cookies -> 首页用户名
        response = redirect(reverse('users:login'))
        response.delete_cookie("username")
        return response


# 个人中心 (隐私信息) 判断是否为当前用户登录
from django.contrib.auth.mixins import LoginRequiredMixin
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        # 请求对象获取
        context = {
            'username':request.user.username,
            'mobile':request.user.mobile,
            'email': '1536452582@qq.com',
            'email_active': True,
        }
        return render(request, 'user_center_info.html', context=context)


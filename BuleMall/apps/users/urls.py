from django.urls import path, re_path
from apps.users import views

app_name = "users"
urlpatterns = [

    # 注册路由
    path(r'register/', views.RegisterView.as_view()),

    # 用户名是否重复
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9]{5,20})/count/$', views.UsernameCountView.as_view()),

    # 手机号是否重复
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),

    # 登录页展示
    re_path(r'^login/$', views.LoginView.as_view(),name="login"),

    # 退出登录
    re_path(r'^logout/$', views.LogoutView.as_view()),

    # 用户中心
    re_path(r'^info/$', views.UserInfoView.as_view()),
]

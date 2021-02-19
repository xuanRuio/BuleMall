from django import http
from django.shortcuts import render
from django.views import View


# 图片验证码
class ImageCodeView(View):

    def get(self, request, uuid):
        from libs.captcha.captcha import captcha
        from django_redis import get_redis_connection
        """ 调用验证码获取验证码值和图片，值存于数据库，图片返回给前端页面 """
        text, image = captcha.generate_captcha()
        # 连接数据库
        img_client = get_redis_connection('image_code')
        # 设置具有过期时间的值
        img_client.setex("img_%s" % uuid, 300, text)
        return http.HttpResponse(image, content_type='image/jpeg')

# 短信验证码
class SmsCodeView(View):

    def get(self, request, mobile):

        # 获取前端用户传入的图片验证码
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        from django_redis import get_redis_connection
        # 获取redis中存入的图片验证码 - redis返回的使bytes类型
        image_client = get_redis_connection('image_code')
        img_code_redis = image_client.get("img_%s" % uuid)

        # 判断验证码是否失效
        if img_code_redis is None:
            return http.JsonResponse({'code':'4001','errmsg':'输入的图形验证码失效'})
        # 删除验证码
        image_client.delete("img_%s" % uuid)

        # 判断验证码是否相等  redis返回的使bytes类型  大小写
        if img_code_redis.decode().lower() != image_code.lower():
            return http.JsonResponse({'code':'4001','errmsg':'输入的图形验证码错误'})

        sms_client = get_redis_connection('sms_code')

        # 获取当前手机号是否频繁发送短信的标识
        send_flag = sms_client.get('send_flag_%s' % mobile)
        # 判断标识是否存在
        if send_flag:
            return http.JsonResponse({'code':'4002','errmsg':'发送短信过于频繁'})
        # 标识不存在，将随机6位短信验证码存入redis库，重新倒计时
        from random import randint
        sms_code = '%06d' % randint(0, 999999)
        sms_client.setex('send_flag_%s' % mobile, 60, 1)
        sms_client.setex('sms_%s' % mobile, 300, sms_code)
        print(f"短信验证码为{sms_code}")
        # 第三方短信验证码发送
        from libs.sms_ronglianyun import SendMessage
        # SendMessage.send_message(mobile, sms_code, 5)
        return http.JsonResponse({'code':'0','errmsg':'发送短信成功'})
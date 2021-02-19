from django.db import models

from django.contrib.auth.models import AbstractUser


# Django自带用户认证类 AbstractUser : 包含username,password【加解密】字段
class User(AbstractUser):

    # 添加自定义字段 mobile
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")

    class Meta:
        # 模型表名称
        db_table = 'tb_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
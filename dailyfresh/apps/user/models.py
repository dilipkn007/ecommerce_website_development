from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


# Create your models here.

# 使用django默认的认证系统
# python manage.py createsuperuser->auth_user->User模型类
class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class AddressManager(models.Manager):
    """地址模型管理器类"""

    # 封装方法: 改变原有查询的结果集
    # 封装方法: 用于操作模型管理器对象所在模型类对应的数据表(增、删、改、查)
    def get_default_address(self, user):
        """获取user用户的默认收货地址"""
        try:
            # address = Address.objects.get(user=user, is_default=True)
            address = self.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        except self.model.DoesNotExist:
            address = None

        # 返回address
        return address

    def get_all_address(self, user):
        """获取所有地址"""
        try:
            have_address = self.filter(user=user)
        except self.model.DoesNotExist:
            have_address = None
        return have_address


class Address(BaseModel):
    '''地址模型类'''
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义模型管理器类的对象
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

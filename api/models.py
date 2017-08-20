# coding: utf-8
"""
定义了项目中使用的的数据模型
"""
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    """
    继承django框架的用户管理器
    """
    def create_user(self, email, nickname, password=None):
        """
        创建新用户

        Parameters:
            :email: 用户邮件地址\n
            :nickname: 昵称\n
            :password: 密码明文字符串,django将自动对密码进行加密\n

        Returns:
            :user: 返回新创建的User对象\n
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            nickname=nickname,
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    继承django抽象用户模型的用户数据模型
    """
    
    """ 用户电子邮件地址,作为区别用户的凭据,不可重复,最大长度为255 """
    email = models.EmailField(max_length=255, unique=True)
    """ 用户昵称,可重复,最大长度为32位 """
    nickname = models.CharField(max_length=32)
    """ 用户创建时间,注册用户对象时自动生成 """
    created_at = models.DateTimeField(auto_now_add=True)
    """ 用户付费状态 """
    has_paied = models.BooleanField(default=False)
    """ 用户游戏进程,保存当前已经通过的关卡数量 """
    game_progress = models.IntegerField(default=0)
    """ 指定用户管理器 """
    objects = UserManager()
    """ 指定用户身份标识字段 """
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-created_at',)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class GameLevels(models.Model):
    """
    存储系统游戏关卡
    """

    """ 地图id,作为区别关卡的标识字段 """
    map_id = models.SmallIntegerField(primary_key=True)
    """ 存储地图内容的字符串,最大长度1000 """
    map = models.CharField(max_length=1000, default=None)
    """ 关卡名称 """
    name = models.CharField(max_length=100, default=None)
    """ 关卡提示 """
    tips = models.CharField(max_length=1000, default=None)
    """ 初始代码 """
    codes = models.CharField(max_length=1000, default=None)
    """ 权限控制 """
    mode = models.CharField(max_length=1000, default=None)


class DesignedMaps(models.Model):
    """
    存储用户编辑的地图
    """

    """ 地图id,作为区别地图的标识字段 """
    map_id = models.AutoField(primary_key=True)
    """ 存储地图内容的字符串,最大长度1000 """
    map = models.CharField(max_length=1000)
    """ 地图名称 """
    name = models.CharField(max_length=32)
    """ 地图说明 """
    remarks = models.CharField(max_length=1000)
    """ 地图作者 """
    author = models.ForeignKey(User)
    """ 地图发布状态 """
    is_published = models.BooleanField(default=False)

    def publish(self):
        """
        发布地图
        """
        self.is_published = True
        self.save()

    def cancel_publish(self):
        """
        取消发布地图
        """
        self.is_published = False
        self.save()


class FavoriteMaps(models.Model):
    """
    存储用户收藏的地图列表
    """

    """ 用户身份,使用User模型中的对象作为外键 """
    user = models.ForeignKey(User)
    """ 地图,使用DesignedMaps模型中的对象作为外键 """
    map = models.ForeignKey(DesignedMaps)


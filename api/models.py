#coding: utf-8

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):

    def create_user(self, email, nickname, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            nickname=nickname,
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):

        user = self.create_user(email, nickname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    # email作为唯一认证标识符
    email = models.EmailField(max_length=100, unique=True)
    # 昵称
    nickname = models.CharField(max_length=32)
    # 注册时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 是否是管理员
    is_admin = models.BooleanField(default=False)
    # 是否已付费
    has_paied = models.BooleanField(default=False)
    # 关卡进度
    game_progress = models.IntegerField(default=0)


    objects = UserManager()

    # 描述User模型上用作唯一标识符的字段名称的字符串
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        ordering = ('-created_at',)
    
    # 在python2应定义 __unicode__
    # 在基类有定义,指到get_username(),指到USERNAME_FIELD
    def __str__(self):
        return self.email

    # 据说这个函数不定义会报错
    def get_full_name(self):
        return self.email

    # 据说这个函数不定义会报错
    def get_short_name(self):
        return self.email
    
    # 有没有特殊权限
    def has_perm(self, perm, obj=None):
        return True

    # 能不能查看app_label这个app
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class GameLevels(models.Model):
    map_id = models.AutoField(primary_key=True)
    map = models.CharField(max_length=1000)
    level_three_steps = models.SmallIntegerField()
    level_two_steps = models.SmallIntegerField()
    tips = models.CharField(max_length=1000)
    goal = models.CharField(max_length=1000)

    def __str__(self):
        return '{},{}'.format(self.map_id, self.tips)

class DesignedMaps(models.Model):
    map_id = models.AutoField(primary_key=True)
    map = models.CharField(max_length=1000)
    name = models.CharField(max_length=32)
    remarks = models.CharField(max_length=1000)
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.map_id

class FavoriteMaps(models.Model):
    user = models.ForeignKey(User)
    map = models.ForeignKey(DesignedMaps)

    def __str__(self):
        return '{}:{}'.format(self.user.id, self.map.map_id)

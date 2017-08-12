# coding: utf-8
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


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    has_paied = models.BooleanField(default=False)
    game_progress = models.IntegerField(default=0)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('-created_at',)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class GameLevels(models.Model):
    map_id = models.AutoField(primary_key=True)
    map = models.CharField(max_length=1000)
    level_three_steps = models.SmallIntegerField()
    level_two_steps = models.SmallIntegerField()
    tips = models.CharField(max_length=1000)
    goal = models.CharField(max_length=1000)


class DesignedMaps(models.Model):
    map_id = models.AutoField(primary_key=True)
    map = models.CharField(max_length=1000)
    name = models.CharField(max_length=32)
    remarks = models.CharField(max_length=1000)
    author = models.ForeignKey(User)
    is_published = models.BooleanField(default=False)

    def publish(self):
        self.is_published = True
        self.save()

    def cancel_publish(self):
        self.is_published = False
        self.save()


class FavoriteMaps(models.Model):
    user = models.ForeignKey(User)
    map = models.ForeignKey(DesignedMaps)

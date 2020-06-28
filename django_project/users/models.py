
# Create your models here.

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('아이디', max_length=30, unique=True)
    email = models.EmailField('이메일', blank=True)
    name = models.CharField('이름', max_length=30)
    gender = models.CharField('성별',max_length=2)
    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용중', default=True)
    date_joined = models.DateTimeField('가입일', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']  # 필수입력값

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'


class ViewedBook(models.Model):
    user = models.ForeignKey(User, verbose_name='검색한 사용자', on_delete=models.CASCADE)
    book = models.IntegerField('검색한 책')
    date = models.DateTimeField('검색한 시간', default=timezone.now)

    def __str__(self):
        return str(self.book)
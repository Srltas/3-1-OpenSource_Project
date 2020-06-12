
# Create your models here.

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class users(models.Model):
    username = models.CharField(max_length=64, verbose_name='사용자명')
    useremail = models.EmailField(max_length=128, verbose_name='사용자이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'library_users'
        verbose_name_plural = '도서관 사용자'


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('아이디', max_length=30, unique=True)
    email = models.EmailField('이메일', blank=True)
    name = models.CharField('이름', max_length=30)
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
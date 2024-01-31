from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):  # BaseUserManager : User를 생성할 때 사용하는 클래스
    use_in_migrations = True # 새로운 모델을 생성하고 이를 MIGRATION에 적용하려면 TRUE로 설정해야 함.

    def create_user(self, email, username, password=None):  # 일반USER 생성
        if not username:
            raise ValueError('must have user username')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):  # 관리자user 생성
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):

    objects = CustomUserManager()
    student_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=4)


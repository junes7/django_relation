from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followings",
        blank=True
    )

    # 각종 필드를 추가
    # createsuperuser
    # shell_plus
    # create_user is_staff, 최고권한 True

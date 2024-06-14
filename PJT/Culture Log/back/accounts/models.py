from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import get_random_profile_image


# 팔로우 기능 구현 (24.05.20)
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False , related_name = 'followers')
    profile_image = models.CharField(max_length=255, blank=True, default='')  # 프로필 이미지 필드 자동으로 추가

    def __str__(self):
            return self.username
    
    def save(self, *args, **kwargs):
        if not self.profile_image:
            self.profile_image = get_random_profile_image()
        super().save(*args, **kwargs)
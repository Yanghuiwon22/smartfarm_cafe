from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from multiselectfield import MultiSelectField
from messaging.models import Message
from softeng_2023_prj import settings
from django.contrib.auth import get_user_model

# User = get_user_model()

def reserve_upload_to(instance, filename):
    instance.sender_username = instance.sender.username
    extension = filename.split('.')[-1]  # 파일 확장자 추출
    new_filename = f'{uuid.uuid4().hex}.{extension}'
    current_date = datetime.now()

    # return f'reserve_meal/images/%Y/%M/%D/'
    return f'reserve_meal/images/{current_date.year}/{current_date.month:02d}/{current_date.day:02d}/{instance.sender_username}/{new_filename}'


# Create your models here.
class ReserveMeal(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_reserve', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_reserve', null=True, on_delete=models.CASCADE)
    timetable = models.ImageField(upload_to=reserve_upload_to)
    content = models.TextField()

    food_opt = [
        ('한식', '한식'),
        ('중식', '중식'),
        ('양식', '양식'),
        ('일식', '일식'),
    ]
    food = MultiSelectField(max_length=101, choices=food_opt)

    title = models.CharField(max_length=100)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.pk}] From {self.sender} to {self.receiver}: {self.content}"

    def get_absolute_url(self):  # 폼을 성공적으로 처리 시 이동할 페이지 주소
        return f'/reserve_meal/'

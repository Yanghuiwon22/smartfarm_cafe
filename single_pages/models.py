from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    student_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=4)
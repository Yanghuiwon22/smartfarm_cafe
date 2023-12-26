from django.db import models
import os
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
# Create your models here.


class BookImage(models.Model):
    image = models.ImageField(upload_to='bookstore/images/%Y/%m/%d')

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/bookstore/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

# 게시글 내용
class BookStore(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    price_set = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    content = models.TextField()
    img_file = models.ImageField(upload_to='bookstore/images/%Y/%m/%d', blank=True)

    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    traces_opt = [
        ('밑줄(연필/샤프)', '필기흔적 없음'),
        ('밑줄(연필/샤프)', '밑줄(연필/샤프)'),
        ('밑줄(볼펜/형광펜)', '밑줄(볼펜/형광펜)'),
        ('필기(연필/샤프)', '필기(연필/샤프)'),
        ('필기(볼펜/형광펜)', '필기(볼펜/형광펜)'),
    ]
    traces = MultiSelectField(max_length=101, choices=traces_opt)
    status_opt = [
        ('밑줄(연필/샤프)', '거의 새것'),
        ('밑줄(연필/샤프)', '겉표지 깨끗함'),
        ('밑줄(볼펜/형광펜)', '이름(서명) 기입 없음'),
        ('필기(연필/샤프)', '페이지 변색 없음'),
        ('필기(볼펜/형광펜)', '페이지 훼손'),
    ]
    status = MultiSelectField(max_length=100, choices=status_opt)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)


    def __str__(self):
        return f'[{self.publisher}] {self.title} :: {self.writer}'

    def get_absolute_url(self):
        return f'/bookstore/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.img_file.name)

    def get_file_ext(self):
        return self.img_file().split('.')[-1]

from django import forms
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db import models
import os
from django.urls import reverse

# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('archive:category_page', args=[self.slug])
#
#     class Meta:
#         verbose_name_plural = 'Categories'

class Archive(models.Model):
    title = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    student = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    content = models.TextField()
    head_image = models.ImageField(upload_to='archive/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='archive/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.student}'

    def get_absolute_url(self):
        return f'/archive/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]


    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]
from django.urls import path, include
from . import views
# from .views import upload_file
from django.contrib import admin

urlpatterns = [
    path('', views.ArchiveList.as_view(), name='archive_list'),
    path('<int:pk>/', views.ArchiveDetail.as_view()),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('register/', views.ArchiveForm_Form.as_view(), name='archive_register_form'),
    path('archive/category/<str:slug>', views.category_page),
    # path('upload/', upload_file, name='upload_file'),
]


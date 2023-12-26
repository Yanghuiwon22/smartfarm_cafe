from django.urls import path
from . import views


urlpatterns = [
    path('about_me/', views.about_me, name="about_SF"),
    path('', views.landing, name='smartfarm_landing'),
    path('my_page/', views.my_page, name='my_page'),
    ]
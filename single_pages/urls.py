from django.urls import path
from . import views

urlpatterns = [
    path('about_me/', views.about_me, name="about_SF"),
    path('', views.landing, name='smartfarm_landing'),
    path('accounts/login/', views.custom_login, name='custom_login'),
    path('accounts/signup/', views.signup, name='custom_signup'),
    path('accounts/logout/', views.custom_logout, name='custom_logout'),
]
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # 밥약
    path('', views.reserve_list, name='reserve_list'),

    # 밥약 작성폼
    path('reserve_form/', views.ReserveMeal_Form.as_view(), name='reserve_regi'),
    path('reserve_form_secret/', views.ReserveMeal_Form_Secret.as_view(), name='reserve_regi_secret'),

    # 메세지
    path('mypage_meal', views.mypage_meal, name='mypage_meal'),
    path('send_reserve_message/<int:pk>', views.send_reserve_message, name='send_reserve_message')

]

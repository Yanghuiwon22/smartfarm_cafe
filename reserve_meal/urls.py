from django.contrib import admin
from django.urls import path, include
from .views import reserve_main, reserve_list, ReserveMeal_Form, ReserveMealDetail,ReserveMeal_Form_Secret

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', reserve_main, name='reserve_main'),
    path('regi/', ReserveMeal_Form.as_view(), name='reserve_regi'),
    path('regi_secret/', ReserveMeal_Form_Secret.as_view(), name='reserve_regi_secret'),

    # path('reserve_list/', ReserveMealDetail.as_view(), name='reserve_list'),
    path('reserve_list/', reserve_list, name='reserve_list'),

]

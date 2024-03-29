"""
URL configuration for softeng_2023_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

smartfarm_council = 'http://sfarm.taegon.kr:15060/'

urlpatterns = [
    path('', include('single_pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('archive/', include("archive.urls")),
    path('bookstore/', include("bookstore.urls")),
    path('reserve_meal/', include('reserve_meal.urls')),
    path('messaging/', include("messaging.urls")),
    # path('allbum/', include("allbum.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

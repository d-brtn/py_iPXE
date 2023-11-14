#urls.py
from django.contrib import admin
from django.urls import path
from menu import views
from django.conf.urls import include
from rest_framework import routers  
router = routers.DefaultRouter()
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'wim', views.WimagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
]

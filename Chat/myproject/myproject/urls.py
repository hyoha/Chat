# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # Django 관리자 페이지
    path('', include('blog.urls')),    # blog.urls를 루트 URL에 포함
]

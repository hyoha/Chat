# blog/urls.py
from django.urls import path
from . import views  # 현재 blog 앱의 views.py에서 함수 불러오기

urlpatterns = [
    path('', views.blog_main, name='blog_main'),  # 루트 URL → blog_main 뷰 실행
    path('ask/', views.blog_ask, name='blog_ask'),  # /ask/ URL → blog_ask 뷰 실행
]

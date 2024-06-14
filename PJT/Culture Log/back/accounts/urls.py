from django.contrib import admin
from django.urls import path, include
from accounts import views


urlpatterns = [
    path('',views.user_list),
    path('<str:user_name>/',views.user_detail), # 개인 유저 조회 추가 작성 
    path('<int:user_id>/follow/', views.follow),
    path('<int:user_id>/follow-stats/', views.follow_stats),
]

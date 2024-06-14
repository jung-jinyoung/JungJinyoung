from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('books/', views.book_list),
    path('books/<str:book_isbn>/', views.book_details),   # 개별 책 조회
    path('movies/',views.movie_list),
    path('playlist/',views.playlist),
    path('reviews/<int:review_pk>/', views.review_detail), # 리뷰 수정, 삭제 
    path('reviews/user/<int:user_id>/', views.review_list), # 해당 유저가 작성한 리뷰 조회
    path('reviews/create/', views.create_review), # 유저가 리뷰 작성할 경우
    ## chat gpt 추천 경로 
    path('greeting/', views.greeting),
    path('recommend/book/', views.recommend_book),
    path('recommend/movie/', views.recommend_movie),
    # 책, 영화 등을 저장했을 때의 경로
    path('choice/movie/<int:movie_id>/',views.choiced_movie),
    path('choice/book/<str:book_isbn>/', views.choiced_book),
    # 커뮤니티 기능 구현 : 주간 기록왕, 추천 많이 받은 책과 영화
    path('weekly/users/',views.weekly_users),
    path('weekly/movies/',views.weekly_moives),
    path('weekly/books/',views.weekly_books),

]
 
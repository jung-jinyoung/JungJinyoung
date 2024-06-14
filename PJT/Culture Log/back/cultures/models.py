from django.db import models
from django.conf import settings


class Book(models.Model):
    isbn = models.TextField() ## 추가
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    categoryName = models.TextField() ## 추가 : 전체 카테고리로 저장 (24.05.18)
    category = models.CharField(max_length=255) # 가장 마지막에 분류되어 있는 카테고리만 저장 (24.05.19) 
    description = models.TextField()
    cover = models.TextField()
    adult = models.BooleanField(default = False)
    publisher = models.CharField(max_length=255)
    link = models.TextField()
    readers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_books', blank=True)
    

    # admin 페이지 데이터생성을 위한 작성
    def __str__(self):
            return self.title
    
    
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    overview  = models.TextField()
    poster = models.TextField()
    adult = models.BooleanField(default = False)
    genre = models.TextField()
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watched_movies', blank=True)
    
    # admin 페이지 데이터생성을 위한 작성
    def __str__(self):
            return self.title


class Playlist(models.Model):
    url = models.TextField()
    genre = models.TextField()
    thumbnails = models.TextField() # 추가 : 유저 페이지에 기록용으로 썸네일 이미지 경로 생성 (24.05.20) 


# GPT에서 추천받은 책과 영화를 저장, 조회할 모델 작성
class ChoicedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    ## 로그인 하지 않은 유저의 경우 => null값으로 작성할 수 있도록
    choiced_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    choiced_at = models.DateField(auto_now_add=True)

    # 추가 : 로그인 한 유저가 현재 진행중인 책이 있는지 확인하기 위해 필드 생성
    # 24.05.20
    # is_done = models.BooleanField(default=False) # 기능 구현 취소 25.05.23
    
    # 현재 진행중인 책이 있다면 -> 책을 읽은 진도를 표시하기 위해 필드 추가
    pages = models.IntegerField()
    now_page = models.IntegerField()
    time = models.TextField()

    # 선택된 날씨와 기분
    mood = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    
    def __str__(self):
            return self.book.title


class ChoicedMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    ## 로그인 하지 않은 유저의 경우 => null값으로 작성할 수 있도록
    choiced_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    choiced_at = models.DateField(auto_now_add=True)

    # 추가 : 로그인 한 유저가 현재 진행중인 영화 있는지 확인하기 위해 필드 생성
    # 24.05.20 
    # is_done = models.BooleanField(default=False) # 기능 구현 취소 25.05.23

    # 선택된 날씨와 기분
    mood = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)

    def __str__(self):
            return self.movie.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE, related_name='movie_review')
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE, related_name='book_review')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weather = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)
    # 책을 리뷰했을 경우 그날 최종적으로 들었던 플레이리스트 저장을 위한 필드 생성
    # 24.05.20
    # playlist_url = models.TextField(null=True, blank=True)
    # playlist_image = models.TextField(null=True, blank=True)
    
    content = models.TextField(max_length=300) # 300자 내로 리뷰를 작성할 수 있도록 수정
    created_at = models.DateField(auto_now_add=True)
    score = models.PositiveIntegerField() # 추가 : 유저 점수 반영하기 위해 생성 (24.05.20)

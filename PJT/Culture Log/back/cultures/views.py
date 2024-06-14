# django 라이브러리 작성
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# DRF 관련 작성
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# 해당 model/serializer 불러오기 
from .serializers import (
    BookListSerializer, MovieListSerializer, ChoicedMovieSerializer, PlayListSerializer, ChoicedBookSerializer, ReviewSerializer)
from .models import Book, Movie, Review, Playlist


#  전체 책 리스트 조회하기
@api_view(['GET'])
def book_list(request):
    books = get_list_or_404(Book)
    print(books)
    serializer = BookListSerializer(books, many = True )
    return Response(serializer.data)


# bookIsbn 를 통해 개별 책 정보 조회하기
@api_view(['GET'])
def book_details(request, book_isbn):
    book = get_object_or_404(Book, isbn=book_isbn)
    serializer = BookListSerializer(book)
    return Response(serializer.data)

 
# 전체 영화 리스트 조회하기
@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# 전체 플레이리스트 조회하기
@api_view(['GET']) 
def playlist(request):
     playlists = get_list_or_404(Playlist)
     serializer = PlayListSerializer(playlists, many=True)
     return Response(serializer.data)

""" 리뷰 작성 구현 24.05.19 
    책 + 플리 아직 미작성 => 리뷰 데이터 모델 수정해야할 듯 
"""
# 리뷰 작성
@api_view(['POST'])
def create_review(request):
    print(request.data)
    writer = request.user
    content = request.data.get('content')
    score = request.data.get('score')
    movie_id = request.data.get('movie_id')
    book_id = request.data.get('book_id')
    mood = request.data.get('mood')
    weather = request.data.get('weather')
    
    # 영화에 대한 리뷰일 경우
    if movie_id:
        movie = get_object_or_404(Movie, movie_id=movie_id)
        review = Review.objects.create(writer=writer, content=content, movie=movie, score=score, mood=mood,weather=weather )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # 책에 대한 리뷰일 경우 
    elif book_id:
        book = get_object_or_404(Book, pk=book_id)
        review = Review.objects.create(writer=writer, content=content, book=book, score=score)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # 그 외의 응답 처리
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# 유저 리뷰 조회 구현하기
@api_view(['GET'])
def review_list(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(writer=user).order_by('-created_at')  # 최신 리뷰부터 정렬
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)



# 개별 리뷰 CRUD 구현하기
@api_view(['PUT','DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request,review_pk):
    review = Review.objects.get(pk=review_pk)
    print(request.data)
    # 작성자와 일치하지 않을 경우 
    if review.writer != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        print(request.data)
        serializer = ReviewSerializer(review, data = request.data, partial = True )
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################### 

""" chat gpt 추천 받기 """
from django.conf import settings
from django.http import JsonResponse # Vue로 json타입으로 변환하여 전송하기 위해 import 
import json
import requests


chat_gpt_api_key = settings.CHAT_GPT_API_KEY

@api_view(['POST'])
def greeting(request):
    # 입력된 기분과 날씨 받기 
    mood = request.data.get('mood')
    weather = request.data.get('weather')

    
    # (디버깅용) 입력되지 않았을 경우 에러 메시지 제공 
    if not mood or not weather :
        return Response({'error': "Mood and weather are required."})
    
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {chat_gpt_api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
        {"role": "system", "content": "당신은 다정한 친구입니다."},
        {"role": "user", "content": f" {mood}한 기분과 {weather} 날씨에 어울리는 인사를 건네주세요. \n 단, 100글자 내로 간단하게 모든 단어를 한국말로 존댓말로 건내주세요. 인사만 작성해서, 줄띄우기까지 부탁해."}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response_content = response.content.decode('utf-8', 'ignore') # decode 에러 해결
    greeting_json = json.loads(response_content) # json 변환
    
    if response:
        greeting = greeting_json['choices'][0]['message']['content']
        return Response({"greeting": greeting}, status=200)
    else:
        return Response({"error": "Error occurred while fetching brecommendations."}, status=500)


@api_view(['POST'])
def recommend_book(request):
    # 입력된 기분과 날씨 받기 
    mood = request.data.get('mood')
    weather = request.data.get('weather')

    # (디버깅용) 입력되지 않았을 경우 에러 메시지 제공 
    if not mood or not weather :
        return Response({'error': "Mood and weather are required."})
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {chat_gpt_api_key}",
    }
    data = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
        {"role": "system", "content": "당신은 친절한 조력자입니다."},
        {"role": "user", "content": f" 장르 리스트는 다음과 같습니다. : 에세이, 인문학, 경제, 과학, 자기계발, 액션, 판타지, 코믹, 추리/미스테리소설, 심령연구, 소설, 시  \n{mood}한 기분과 {weather} 날씨에 어울리는 책 장르를 장르 리스트에서 두개 이상 추천해주세요. \n단, 장르 이름만 띄어쓰기와 ','로 구분하여 제안해주세요. "}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    response_content = response.content.decode('utf-8', 'ignore') # decode
    book_recommendation_json = json.loads(response_content)
    if response:
        book_recommendation = book_recommendation_json['choices'][0]['message']['content']
        recommended_genres = book_recommendation.split(", ")
        receommended_books = []
        for genre in recommended_genres :
            books = Book.objects.filter(category__icontains=genre)
            # 조회된 책을 최종 결과 리스트에 추가, 중복을 피하기 위해 set을 사용
            for book in books:
                book_data = {
                'title': book.title,
                'author': book.author,
                'category': book.category,
                'isbn': book.isbn,
                'adult': book.adult,
                'description': book.description,
                'cover': book.cover,
                'publisher': book.publisher,
                'link': book.link

            }
                if book_data not in receommended_books:
                    receommended_books.append(book_data)
        
        # 최종 결과를 JSON 응답으로 반환
        return JsonResponse({'books': receommended_books})
            
    else:
        return Response({"error": "Error occurred while fetching book recommendations."}, status=500)



# tmdb가 제공하는 장르 리스트를 새로 매핑 
# 장르 이름과 ID 매핑
genre_mapping = {
    "액션": 28,
    "모험": 12,
    "애니메이션": 16,
    "코미디": 35,
    "범죄": 80,
    "다큐멘터리": 99,
    "드라마": 18,
    "가족": 10751,
    "판타지": 14,
    "역사": 36,
    "공포": 27,
    "음악": 10402,
    "미스터리": 9648,
    "로맨스": 10749,
    "SF": 878,
    "TV 영화": 10770,
    "스릴러": 53,
    "전쟁": 10752,
    "서부": 37
}
@api_view(['POST'])
def recommend_movie(request):
    # 입력된 기분과 날씨 받기 
    mood = request.data.get('mood')
    weather = request.data.get('weather')
    print(request.data)
    # 각 장르에 대해 영화 데이터를 조회하고 결과를 합침
    genre_ids = [16]
    recommended_movies = []

    
    # (디버깅용) 입력되지 않았을 경우 에러 메시지 제공 
    if not mood or not weather :
        return Response({'error': "Mood and weather are required."})
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {chat_gpt_api_key}",
    }
    data = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
        {"role": "system", "content": "당신은 친절한 조력자입니다."},
        {"role": "user", "content": f" 장르 리스트는 다음과 같습니다. : 액션, 애니메이션, 코미디, 범죄, 다큐멘터리, 판타지, 공포, 음악, 미스터리, 로맨스, SF, 스릴러, 전쟁 \n{mood}한 기분과 {weather} 날씨에 어울리는 책 장르를 장르 리스트에서 두개 이상 추천해주세요. \n단, 장르 이름만 띄어쓰기와 ','로 구분하여 제안해주세요. "}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response_content = response.content.decode('utf-8', 'ignore') # decode
    movie_recommendation_json = json.loads(response_content)
    if response:
        # genre 추천 
        movie_recommendation = movie_recommendation_json['choices'][0]['message']['content']
        # 추천받은 장르 문자열에서 장르 이름들을 구분하여 가져오기 위해 다음과 같이 작성함. 
        recommended_genres = movie_recommendation.split(", ")
        # DB 에 저장되어 있는 영화 조회 -> 해당 장르만 가져오기 
        genre_ids = [genre_mapping[genre.strip()] for genre in recommended_genres if genre.strip() in genre_mapping]
        
        # 영화 조회 
        # 결과를 저장할 리스트
        recommended_movies = []

        # 각 장르에 대해 영화 데이터를 조회하고 결과를 합침
        for genre_id in genre_ids:
            # 현재 장르를 포함하는 영화를 조회
            movies = Movie.objects.filter(genre__icontains=str(genre_id))
            
            # 조회된 영화를 최종 결과 리스트에 추가, 중복을 피하기 위해 set을 사용
            for movie in movies:
                movie_data = {
                'movie_id': movie.movie_id,
                'title': movie.title,
                'overview': movie.overview,
                'poster': movie.poster,
                'adult': movie.adult,
                'genre': movie.genre
            }
                if movie_data not in recommended_movies:
                    recommended_movies.append(movie_data)
        
        # 데이터 확인하기 위해 출력
        # print(final_movies)
        # 최종 결과를 JSON 응답으로 반환
        return JsonResponse({'movies': recommended_movies})
        
    else:
        return Response({"error": "Error occurred while fetching book recommendations."}, status=500)

###########################
"""
24.05.19
선택된 영화 및 책 데이터베이스에 저장하기 구현
++++ 플레이리스트 아직 미구현
"""
from .models import ChoicedBook, ChoicedMovie

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def choiced_book(request, book_isbn):
    book = get_object_or_404(Book, isbn=book_isbn)

    if request.method == 'POST':
        # POST 요청에서는 현재 진행중인 책을 추가합니다.
        serializer = ChoicedBookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        # PUT 요청에서는 현재 진행중인 책의 정보를 업데이트합니다.
        choiced_book = get_object_or_404(ChoicedBook, book=book, choiced_by=request.user)
        serializer = ChoicedBookSerializer(choiced_book, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def choiced_movie(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    choiced_by = request.user if request.user.is_authenticated else None
    mood = request.data.get('mood')
    weather = request.data.get('weather')
    

    # 선택된 영화 DB에 저장
    choiced_movie = ChoicedMovie.objects.create(movie=movie, choiced_by=choiced_by, mood=mood, weather=weather)
    serializer = ChoicedMovieSerializer(choiced_movie)
    return Response(serializer.data)


"""
커뮤니티 기능 구현 : 2024.05.19
주간 가장 많이 기록한 유저 조회
주간 가장 많이 추천받은 책 / 영화 조회  

수정 : 2024.05.20
필요한 필드 조회 후 json 파일로 전송 
"""

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

# 현재 시간 및 일주일 전의 날짜 계산
now = timezone.now()
one_week_ago = now - timedelta(days=7)

@api_view(['GET'])
def weekly_users(request):
    User = get_user_model()
    # 주간 동안 작성된 리뷰들을 작성자(User)별로 그룹화하여 리뷰 개수를 세어서 내림차순으로 정렬
    weekly_most_active_users = Review.objects.filter(created_at__gte=one_week_ago)\
                                             .values('writer')\
                                             .annotate(review_count=Count('id'))\
                                             .order_by('-review_count')
    
    # 유저의 ID 목록을 추출
    user_ids = [user['writer'] for user in weekly_most_active_users[:5]]  # Top 5 users

    users = []
    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        users.append({
            'username': user.username,
            'profile_image': f'/profile_images/{user.profile_image}'
        })
    return JsonResponse(users, safe=False)


@api_view(['GET'])
def weekly_moives(request):
    # 주간 동안 추천받은 영화들을 그룹화하여 추천 횟수를 기준으로 내림차순으로 정렬
    weekly_most_recommended_movies = ChoicedMovie.objects.filter(choiced_at__gte=one_week_ago)\
                                                          .values('movie')\
                                                          .annotate(recommendation_count=Count('movie'))\
                                                          .order_by('-recommendation_count')
    # 영화의 ID 목록을 추출
    movie_ids = [movie['movie'] for movie in weekly_most_recommended_movies]

    movies = []
    for movie_id in movie_ids:
        movie = Movie.objects.get(id=movie_id)
        movies.append({
            'movie_id': movie.movie_id,
            'title': movie.title,
            'overview': movie.overview,
            'poster': movie.poster,
        })

    return JsonResponse(movies, safe=False)



@api_view(['GET'])
def weekly_books(request):
    # 주간 동안 추천받은 책들을 그룹화하여 추천 횟수를 기준으로 내림차순으로 정렬
    weekly_most_recommended_books = ChoicedBook.objects.filter(choiced_at__gte=one_week_ago)\
                                                        .values('book')\
                                                        .annotate(recommendation_count=Count('book'))\
                                                        .order_by('-recommendation_count')
    
    
    print(weekly_most_recommended_books)

    # 책의 ID 목록을 추출
    book_ids = [book['book'] for book in weekly_most_recommended_books]
    books = []
    for book_id in book_ids:
        book = Book.objects.get(id=book_id)
        books.append({
            'isbn': book.isbn,
            'title': book.title,
            'description': book.description,
            'cover': book.cover,
        })
    return JsonResponse(books, safe=False)
    

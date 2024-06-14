import requests
from django.core.management.base import BaseCommand
from cultures.models import Movie
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY

# 영화 api 받아서 model에 정의된 필드에 저장
class Command(BaseCommand):
    help = 'Fetch movies from tmdb API and create fixtures'

    def handle(self, *args, **options):
        # tmdb API 정보
        api_key = TMDB_API_KEY
        for number in range(1,6):
            base_url = f'https://api.themoviedb.org/3/movie/top_rated?language=ko-KR&page={number}'

            discover_url = f'{base_url}/discover/movie'

            # API 요청 파라미터 설정 (예: 인기 있는 영화 순서대로)
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # API 요청 보내기
            response = requests.get(base_url, headers=headers)
            data = response.json()
            
            # 가져온 데이터 확인을 위한 출력
            # print(data)

            # 가져온 데이터에서 필요한 정보 추출 및 저장
            for movie_data in data.get('results'):
                # print(movie_data,sep="\n")
                # 영화 정보 추출
                title = movie_data.get('title')
                overview = movie_data.get('overview')
                poster_path = movie_data.get('poster_path')
                genre_ids = movie_data.get('genre_ids') 


                # 영화 모델에 저장
                movie = Movie(
                    title=title,
                    overview=overview,
                    movie_id=movie_data.get('id'),
                    poster=f'https://image.tmdb.org/t/p/w500{poster_path}',
                    adult=movie_data.get('adult'),
                    # 숫자 장르 id 리스트를 문자열 리스트로 변환하고 콤마로 구분하여 하나의 문자열로 만듦
                    genre = ','.join(map(str, genre_ids)) ## 수정 : 문자열로 전환 후 저장
                )
                movie.save()

        self.stdout.write(self.style.SUCCESS('Successfully created fixtures for movies'))

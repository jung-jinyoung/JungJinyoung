import requests
from django.core.management.base import BaseCommand
from cultures.models import Playlist
from django.conf import settings

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

# 검색 및 DB 저장하기 위한 리스트 생성 
keywords = ['가사 없는', '클래식', '팝송', '행복', '비오는 날', '인디', 'JPOP', '재즈', '락 밴드']
genres = ['calm', 'classic', 'pop', 'happy', 'rainy', 'blue', 'j-pop', 'jazz', 'rock']

# 유튜브 api 받아서 model에 정의된 필드에 저장
class Command(BaseCommand):
    help = 'Fetch playlist from youtube API and create fixtures'
    def handle(self, *args, **options):
        # 유튜브 API 정보
        api_key = YOUTUBE_API_KEY
        url = 'https://www.googleapis.com/youtube/v3/search'
        # url = 'https://www.googleapis.com/youtube/v3/videos'
        for turn in range(len(keywords)):
            keyword = keywords[turn]
            genre = genres[turn]
            # API 요청 파라미터 설정
            params = {
                'key': api_key,
                'part': 'snippet',
                'maxResults': 10,  # 가져올 결과의 최대 개수 설정
                'q': f'playlist {keyword}',  # 검색어 설정
                'type': 'video'
            }
            # API 요청 보내기
            response = requests.get(url, params=params)
            data = response.json()
            # 동영상 정보 추출 및 출력
            videos = data.get('items')
            for video in videos:
                # 주소를 입력하기 위한 아이디 조회
                video_id = video['id']['videoId']

                video_url = f'https://www.youtube.com/watch?v={video_id}'
                thumbnails = video['snippet']['thumbnails']['high']['url']  # 기본 썸네일 URL 가져오기 : 고해상도
                
                # 플레이리스트 모델에 저장

                playlist = Playlist(
                    url = video_url,
                    genre = genre,
                    thumbnails = thumbnails
                )
                playlist.save()
                
                
        

        


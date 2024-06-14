import requests
from django.core.management.base import BaseCommand
from cultures.models import Book
from django.conf import settings

ALADDIN_API_KEY = settings.ALADDIN_API_KEY


class Command(BaseCommand):
    help = 'Fetch books from aladdin API and create fixtures'

    def handle(self, *args, **options):
        # 알라딘 API 정보
        api_key = ALADDIN_API_KEY
        base_url = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'
        for number in range(1,7):
            discover_url = f'{base_url}?ttbkey={api_key}&QueryType=Bestseller&MaxResults=100&start={number}&SearchTarget=Book&output=js&Version=20131101'

            # API 요청 보내기
            response = requests.get(discover_url)
            data = response.json()
            # print(len(data["item"]))
            print(data["item"])
            
            for turn in range(50):
                book_data = data["item"][turn]

                isbn = book_data.get('isbn')
                title = book_data.get('title')
                author = book_data.get('author')
                categoryName = book_data.get('categoryName')
                category = categoryName.split('>')[-1] # 가장 마지막에 있는 카테고리 저장
                description = book_data.get('description')
                cover = book_data.get('cover')
                publisher = book_data.get('publisher')
                link = book_data.get('link')
                adult = book_data.get('adult')

                
                ## 요구되지 않는 카테고리는 넘어갈 수 있도록 조건문 작성(24.05.19)
                # 교육용 책 빼기
                if "교육" in category :
                    continue
                # 시나리오 책 빼기
                if "시나리오" in category:
                    continue
                # 수험 관련 서적과 어린이 서적 제외
                if '수험서' in categoryName:
                    continue
                if '토익' in categoryName:
                    continue
                if '어린이' in categoryName:
                    continue

                # Book 모델에 저장
                book = Book.objects.create(
                    isbn = isbn,
                    title=title,
                    author=author,
                    categoryName = categoryName,
                    category = category,
                    description=description,
                    cover=cover,
                    adult=adult,
                    publisher=publisher,
                    link=link,
                )
                
        # 저장된 Book 모델 확인
        self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))
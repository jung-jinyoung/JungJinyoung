from rest_framework import serializers
from .models import Book, Movie, Review, Playlist, ChoicedBook, ChoicedMovie
from accounts.models import User


# 전체 책 리스트 조회
class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# 전체 영화 리스트 조회
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# 전체 리뷰 리스트 조회
class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


# 전체 플레이 리스트 조회
class PlayListSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Playlist
        fields = '__all__'


"""
조회 및 선택 알고리즘 구현 후 작성
24.05.19

주석 처리 => 사용하지 않음 
# 선택한 책 시리얼라이저 작성
class ChoicedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoicedBook
        fields = '__all__'
# 선택한 영화 시리얼라이저 작성
class ChoicedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoicedMovie
        fields = '__all__'
"""
class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'content', 'title', 'writer', 'poster', 'created_at', 'score','mood','weather',]
    
    def get_title(self, obj):
        if obj.book:
            return obj.book.title
        elif obj.movie:
            return obj.movie.title
        return None

    def get_poster(self, obj):
        if obj.book:
            return obj.book.cover
        elif obj.movie:
            return obj.movie.poster
        return None
    def get_poster(self, obj):
        if obj.book:
            return obj.book.cover
        elif obj.movie:
            return obj.movie.poster
        return None

    # def get_mood(self, obj):
    #     if obj.book:
    #         return obj.book.mood
    #     elif obj.movie:
    #         return obj.movie.mood
    #     return None

    # def get_weather(self, obj):
    #     if obj.book:
    #         return obj.book.weather
    #     elif obj.movie:
    #         return obj.movie.weather
    #     return None

# 선택한 영화 시리얼라이저
class ChoicedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoicedMovie
        fields = "__all__"


# 선택한 책 시리얼라이저
class ChoicedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoicedBook
        fields = '__all__'

    # def create(self, validated_data):
    #     # 인증된 사용자인 경우에만 책을 선택할 수 있도 록
    #     # user_name = self.context['request'].user if self.context['request'].user.is_authenticated else None
    #     # mood = validated_data.pop('mood')
    #     # weather = validated_data.pop('weather')
    #     # user = User.objects.get(username=user_name)
    #     # choiced_book = ChoicedBook.objects.create(choiced_by=user, mood=mood, weather=weather, choiced_by=user, mood=mood, weather=weather,)
    #     choiced_book = ChoicedBook.objects.create(**validated_data)
    #     return choiced_book

    # def update(self, instance, validated_data):
    #     # 작성자만 수정할 수 있도록
    #     if instance.choiced_by != self.context['request'].user:
    #         raise serializers.ValidationError("Permission denied")
        
    #     instance.mood = validated_data.get('mood', instance.mood)
    #     instance.weather = validated_data.get('weather', instance.weather)
    #     instance.pages = validated_data.get('pages', instance.pages)
    #     instance.now_page = validated_data.get('now_page', instance.now_page)
    #     instance.time = validated_data.get('time', instance.time)
    #     instance.save()
    #     return instance
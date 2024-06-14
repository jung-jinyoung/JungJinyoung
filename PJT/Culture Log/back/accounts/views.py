from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

## User에 대한 정보를 전달하기 위한 시리얼라이저 
from .serializers import UserSerializer



# Create your views here.

User = get_user_model()


@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# 유저 조회
@api_view(['GET'])
# @login_required
def user_detail(request, user_name):
    person = get_object_or_404(User, username = user_name)
    return Response({
        'id': person.pk,
        'username': person.username,
        'profileImg' : person.profile_image,
        'followers' : person.followers.values('id', 'username')
        })



## 팔로우 / 언팔로우 기능 구현 
@api_view(['POST'])
def follow(request, user_id) :
    print(request.user)
    person = get_object_or_404(User, pk=user_id)
    if person != request.user :
        if request.user in person.followers.all() :
            person.followers.remove(request.user)
            return Response({'status': 'unfollowed'}, 
                            status=status.HTTP_200_OK)

        else :
            person.followers.add(request.user)
            return Response({'status': 'followed'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'No'}, status=status.HTTP_200_OK)

## 유저 팔로우 상태를 전달하기 위한 뷰함수 전달 
@api_view(['GET'])
def follow_stats(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)
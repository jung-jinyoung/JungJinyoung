import random

## 저장된 이미지 중 랜덤으로 지정해 주는 함수 작성
def get_random_profile_image():
    images = [
        'profileImage (1).png',
        'profileImage (2).png',
        'profileImage (3).png',
        'profileImage (4).png',
        'profileImage (5).png',
        'profileImage (6).png',
        'profileImage (7).png',
        'profileImage (8).png',
        'profileImage (10).png',
        'profileImage (11).png',
        'profileImage (12).png',
        'profileImage (13).png',
        'profileImage (14).png',
        'profileImage (15).png',
        'profileImage (16).png',
        'profileImage (17).png'
    ]
    return random.choice(images)
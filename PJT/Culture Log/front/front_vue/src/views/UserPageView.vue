<template>
  <div class="container" v-if="user">
    <div class="user-info">
      <div class="img-container">
        <img :src="user.userImg" alt="Profile Image">
      </div>
      <p>{{ username }}</p>
      <div class="follow_detail">
        
        <button 
        v-if="user.userId"
        @click="followButton(user.userId, token)"
        class="followBtn"
        >
        {{ isFollowing ? 'Unfollow' : 'Follow' }}
        </button>
        <div class="followContent">
          <p style="font-weight: bold ; margin-bottom: 0;">
            Followers 
            </p>
          <p style="margin-top: 10px;">{{ user.followers }}</p>
          <hr>
          <p style="font-weight: bold ; margin-bottom: 0;;">Followings</p>
          <p style="margin-top: 10px;">{{ user.followings }}</p>
        </div>
      </div>
    </div>
    <div class="user_log">
      <div v-if="!user.reviews">
        loading
      </div>
      <div v-else>
        <Review 
          :reviews = userStore.user.reviews
          :username = userStore.user.username
        />
      </div>
    </div>
  
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute  } from 'vue-router'
import axios from 'axios'
import Review from '@/components/Review.vue';
import { useAuthStore } from '@/stores/counter';
import { useUsersStore } from '@/stores/users'



const store = useAuthStore()
const token = store.token

const userStore = useUsersStore()


// 로그인한 유저 

// 해당 유저 페이지의 유저 관련
const user = ref(null)
const isFollowing = computed(() => {
    return user.value.followers_list.some(follower => follower.username === store.now_user);
})
  
// 팔로우 버튼 구현
const followButton = function(userId, token) {
axios({
  method: 'post',
  url: `http://127.0.0.1:8000/api/v1/users/${userId}/follow/`,
  headers: {
    Authorization: `Token ${token}`
  }
})
  .then((response) => {
    //팔로우 리스트 업데이트
    axios.get(`http://127.0.0.1:8000/api/v1/users/${user.value.username}/`)
      .then((response) => {
        user.value.followers_list = response.data.followers
        console.log(followers_list)
      })
      .catch((error) => {
        console.log(error)
      })
    
    userStore.updateFollowCounts();
    
  })
  .catch((error) => {
    console.log(error);
  });
};


const route = useRoute()
watch(() => route.params.username, (newUsername) => {
  userStore.user_detail(newUsername)
  user.value = userStore.user
})

onMounted(() => {
  const route = useRoute()
  const username = route.params.username
  
  // 유저 페이지 구현을 위한 해당 유저 불러오기 
  userStore.user_detail(username)
  user.value = userStore.user
  console.log(user)
  
})

</script>

<style scoped>
.container {
  padding-top: 12px;
  display: flex;
  max-width: 1800px;  /* 최대 너비 설정 */
  justify-content: center;
  align-items: flex-start;
  /* padding: 5px 20px; */
}

.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items:center;
  padding : 30px 10px;
  width: 300px; /* 왼쪽에 고정된 너비 */
  margin-right: 30px; /* 오른쪽 여백 추가 */
  text-align: center;
  background-color: rgb(255, 255, 255);
  min-height:400px; /* user_log의 최소 높이를 container의 높이와 동일하게 설정 */

}

.img-container {
  border: 2px solid black;
  background-color: white; /* 배경색을 원한다면 변경 */
  border-radius: 50%; /* 둥근 모서리 */
  width: 150px; /* 원형 배경의 너비 */
  height:  150px; /* 원형 배경의 높이 */
  padding: 15px;
  overflow: hidden; /* 둥근 모서리를 유지하기 위해 필요 */
  
}

img {
  width: 100%; /* 이미지를 컨테이너의 너비에 맞춤 */
  height: 100%; /* 이미지를 컨테이너의 높이에 맞춤 */
  object-fit: cover; /* 이미지가 컨테이너를 채우도록 함 */
}
/* 리뷰 리스트가 출력될 부분 */
.user_log{
  width: 1200px;
  background-color: white;
  height: 100%;
  min-height: 530px;
  margin-bottom: 30px;
}

/* 팔로우 부분 */
.follow_detail {
  text-align: start;
  width: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.followContent{
  margin-top: 20px;
  text-align: center
}

.followBtn{
  background-color: rgb(143, 143, 143); /* 파란색 배경 */
  color: white; /* 흰색 글씨 */
  border: none; /* 선 없음 */
  max-width: 100px;
  width: 100%;
  padding: 5px 10px;

  text-align: center;
  /* font-size: 1px; 글씨 크기 */
  border-radius: 5px; /* 둥근 모서리 */
  cursor: pointer; /* 클릭할 수 있는 커서 */
  transition: background-color 0.3s; /* 배경색 전환 효과 */
}
.update-btn:hover {
  background-color: rgb(255, 255, 255); /* 호버 시 어두운 파란색 */
  color: black ;
}
</style>


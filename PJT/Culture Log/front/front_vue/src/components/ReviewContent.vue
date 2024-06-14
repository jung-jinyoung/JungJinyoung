<template>

    <div v-if="is_choiced" class="content_detail">
      <div class="review" style="max-width: 200px;" v-if="!is_clicked">
        <img :src="review.poster" />
        <p>{{ review.title }}</p>
      </div>
      <div style="padding-right: 20px; padding-bottom: 20px;">
        <p v-if="!is_clicked">📌 {{ review.created_at }}</p>
        <div class="log" v-if="!is_clicked">
          <span>weather {{ weatherDescriptions[review.weather] }}</span>
          <span> feeling {{ moods[review.mood] }}</span>
          <div class="star-rating">
            <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= review.score }">★</span>
            <hr>
          </div>


          <p>
            {{ review.content }}
          </p>
    
          <div class="buttons" v-if="is_correct">
            <button 
            @click="clickUpdate"
            class="update-btn">
            수정</button>
            <button 
            @click="clickDelete"
            class="delete-btn">
            
            삭제</button>
          </div>
      </div>
  </div>
    <UpdateReview
      v-if="is_clicked"
      :is_clicked="is_clicked"
      :review="review"
      @closeModal="updateModal"
      
    />
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed,watch } from "vue";
import UpdateReview from "./UpdateReview.vue";
import { useAuthStore } from "@/stores/counter";
import { useUsersStore } from "@/stores/users";
import axios from "axios";
import router from "@/router";

const store = useAuthStore();
const token = store.token;

const props = defineProps({
  review: Object,
  is_choiced: Boolean,
});


const userStore = useUsersStore();
const moods = {
  'HAPPY': '😆',
  'SOSO' : '🙂',
  'SAD' : '😢',
  'ANGRY' : '😡',
  'EXHAUSTED' : '🥴'
}
const weatherDescriptions = {
    'Clear': '🌞',
    'Clouds': '⛅',
    'Rain': '💧',
    'Snow': '⛄',
    'Thunderstorm': '⚡',
    'Fog': '💨',
    'Mist': '🌂'
  }
// const todayMood = mood[]
// const todayWeather = ref(null)

const emit = defineEmits(['update', 'delete']);

// 전체 유저 모델 불러오기
const users = userStore.users;
const writer = users.find((user) => user.id === props.review.writer); //객체로 넘어옴

const is_correct = computed(() => {
  return writer.username === store.now_user;
});

const is_clicked = ref(false)
const clickUpdate = function () {
  is_clicked.value = true;
  
};

// 모달 끄고 업데이트 


const updateModal = function() {
  emit('update')
  closeModal()

}
const closeModal = function(){
  is_clicked.value = false; // 모달 상태 변경하여 모달 닫기

}
const clickDelete = function () {
  axios({
    method: "delete",
    url: `http://127.0.0.1:8000/api/v1/cultures/reviews/${props.review.id}/`,
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((response) => {
      userStore.get_reviews(props.review.writer);
      emit('delete')
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<style scoped>
.content_detail {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  min-height: 400px;
  height: 100%;
  gap: 30px
}

.review {
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-height: 100px;
  align-items: center;
  padding: 20px;
  margin-bottom: 20px;
  flex: 4;
}

.review img {
  max-width: 120px;
  height: auto;
}

.log {
  border: 1px solid rgb(96, 96, 96);
  border-radius: 5px;
  padding: 10px 30px
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding-bottom: 10px;
}
.update-btn {
  background-color: rgb(0, 140, 255); /* 파란색 배경 */
  color: white; /* 흰색 글씨 */
  border: none; /* 선 없음 */
  padding: 5px 10px; 
  /* font-size: 1px; 글씨 크기 */
  border-radius: 5px; /* 둥근 모서리 */
  cursor: pointer; /* 클릭할 수 있는 커서 */
  transition: background-color 0.3s; /* 배경색 전환 효과 */
}

.update-btn:hover {
  background-color: darkblue; /* 호버 시 어두운 파란색 */
}
.delete-btn {
  background-color: rgb(255, 0, 60); /* 파란색 배경 */
  color: white; /* 흰색 글씨 */
  border: none; /* 선 없음 */
  padding: 5px 10px; 
  /* font-size: 1px; 글씨 크기 */
  border-radius: 5px; /* 둥근 모서리 */
  cursor: pointer; /* 클릭할 수 있는 커서 */
  transition: background-color 0.3s; /* 배경색 전환 효과 */
}

.delete-btn:hover {
  background-color: rgb(139, 0, 58); /* 호버 시 어두운 파란색 */
}

/* 점수 구현 완료  */
.star-rating {
  font-size: 16px; /* 별 크기 */
  margin-top: 10px;
}

.star {
  color: black; /* 검정색 기본 별 색상 */
}

.star.filled {
  color: gold; /* 노란색으로 채워진 별 색상 */
}
</style>

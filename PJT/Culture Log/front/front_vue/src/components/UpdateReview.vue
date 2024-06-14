<template>
  <div class="update-review">
    <h3>{{ props.review.title }}</h3>
    <p>{{ props.review.created_at }}에 작성한 기록을 수정중입니다.</p>
    <form @submit.prevent="updateReview">
      <div class="content">
        <label for="content">content</label>
        <textarea
          id="content"
          v-model="form.content"
          :placeholder="props.review.content"
          maxlength="300"
        ></textarea>
      </div>
      <div class="content">
        <!-- <input type="number" id="score" v-model="form.score" @input="updateStars" /> -->
        <div class="star-rating">
          <template v-for="star in 5">
            <span
              class="star"
              :class="{ 'filled': star <= selectedStar }"
              @click="updateScore(star)"
            >★</span>
          </template>
        </div>
      </div>
      <div class="buttons">
        <button type="submit" @click="updateReview" class="update-btn">저장</button>
        <button type="button" @click="$emit('close')" class="delete-btn">취소</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/stores/counter";
import { useUsersStore } from "@/stores/users";

const store = useAuthStore();
const token = store.token;

const props = defineProps({
  review: Object,
  is_clicked: Boolean,
});
const form = ref({
  title: props.review.title,
  content: props.review.content,
  score: props.review.score,
});
// const updateScore = (star) => {
//   form.score = star;
//   selectedStar.value = star;
// };
const selectedStar = ref(form.score);

// 별을 클릭하면 해당 값으로 score를 업데이트하는 함수
const updateScore = (star) => {
  form.score = star;
  selectedStar.value = star;
};


const emit = defineEmits(['closeModeal']);
const userStore = useUsersStore();
const users = userStore.users;
const username = users.find((user) => user.id === props.review.writer); // usename
const updateReview = function () {
  console.log(form.score)
  axios({
    method: "PUT",
    url: `http://127.0.0.1:8000/api/v1/cultures/reviews/${props.review.id}/`,
    headers: {
      Authorization: `Token ${token}`,
    },
    data: {
      content: form.value.content,
      score: form.score,
    },
  })
    
  .then((response) => {
      // 수정
      userStore.get_reviews(props.review.writer);
      emit('closeModal')
    }
      )
    .catch((error) => {
      console.log(error);
    });
};
const is_clicked = ref(props.is_clicked)

</script>

<style scoped>
.star-rating {
  font-size: 24px; /* 별 크기 */
}

.star {
  color: black; /* 검정색 기본 별 색상 */
  cursor: pointer; /* 포인터 커서 */
}

.star.filled {
  color: gold; /* 노란색으로 채워진 별 색상 */
}
.update-review {
  border: 1px solid #ccc;
  padding: 20px 40px;
  border-radius: 10px;
}
.update-review form {
  display: flex;
  flex-direction: column;
}

.update-review label {
  margin: 5px 0;
  font-weight: bold;
  font-size: 16px;
}

.update-review input[type="number"] {
  text-align: center;
  width: 50px;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
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
/* 숫자 입력 버튼 보이기 구현 */
.update-review input[type="number"]::-webkit-inner-spin-button,
.update-review input[type="number"]::-webkit-outer-spin-button {
  opacity: 1;
}
.update-review textarea,
.update-review input[type="text"] {
  text-align: center;
  width: 250px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.125);
}
.update-review textarea {
  height: 100px;
  resize: none; /* 사용자가 크기를 조절하지 못하도록 설정 */
}

.update-review .buttons {
  display: flex;
  justify-content: center;
  gap: 10px; /* 버튼 사이의 간격 설정 */
}

.update-review .buttons button {
  padding: 10px 20px; /* 버튼 내부의 패딩 설정 */
  margin: 0 5px; /* 버튼 사이의 간격 설정 */
}
.buttons {
  display: flex;
  justify-content: center;
  gap: 10px; /* 버튼 사이의 간격 설정 */
  margin-top: 15px;
}
</style>

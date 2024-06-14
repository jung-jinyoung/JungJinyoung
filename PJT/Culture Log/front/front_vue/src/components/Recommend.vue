<template>
  <div class="container">
    <div class="buttons">
      <!-- 기분은 url 주소에 있음 -->
      <!-- 날씨는 store에 있음 -->
      <button @click="toggleRecommendation('book')">책 추천 🐱‍👤</button>
      <button @click="toggleRecommendation('movie')">영화 추천 🐱‍🏍</button>
    </div>

    <div class="recommendations">
      <div v-if="showBook">
        <RecommendBook :mood="mood" :weather="weather" />
      </div>

      <div v-if="showMovie">
        <RecommendMovie :mood="mood" :weather="weather" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import RecommendBook from './RecommendBook.vue'
import RecommendMovie from './RecommendMovie.vue'

const route = useRoute();
const mood = ref(route.query.mood);
const weather = ref(route.query.weather);

const showBook = ref(false);
const showMovie = ref(false);

const toggleRecommendation = (type) => {
  if (type === 'book') {
    showBook.value = !showBook.value;
  } else if (type === 'movie') {
    showMovie.value = !showMovie.value;
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding-bottom: 50px;
}

.buttons {
  position: absolute;
  top: 20px; /* 상단에서 20px 아래에 위치 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 40px; /* 버튼 사이의 간격을 줄입니다 */
}

.buttons button {
  padding: 15px 30px; /* 버튼 내부 여백을 설정합니다 */
  font-size: 1.2rem; /* 버튼 텍스트 크기를 설정합니다 */
  border: 2px solid #4CAF50; /* 테두리 스타일을 추가합니다 */
  border-radius: 5px; /* 버튼 테두리를 둥글게 만듭니다 */
  background-color: white; /* 배경색을 흰색으로 설정합니다 */
  color: #4CAF50; /* 텍스트 색상을 초록색으로 설정합니다 */
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s; /* 부드러운 전환 효과를 추가합니다 */
}

.buttons button:hover {
  background-color: #4CAF50; /* 호버 상태에서 배경색을 초록색으로 변경합니다 */
  color: white; /* 호버 상태에서 텍스트 색상을 흰색으로 변경합니다 */
}

.recommendations {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 상단에서부터 시작 */
  margin-top: 100px; /* 버튼보다 100px 아래에 위치 */
  width: 100%;
}

/* 반응형 디자인을 위한 미디어 쿼리 */
@media (max-width: 768px) {
  .buttons {
    flex-direction: column;
    gap: 20px; /* 버튼 사이의 간격을 줄입니다 */
  }

  .buttons button {
    width: 100%;
    max-width: 300px;
    padding: 10px 20px; /* 버튼 내부 여백을 줄입니다 */
    font-size: 1rem; /* 버튼 텍스트 크기를 줄입니다 */
  }
}

@media (max-width: 480px) {
  .buttons button {
    padding: 8px 16px; /* 버튼 내부 여백을 더 줄입니다 */
    font-size: 0.9rem; /* 버튼 텍스트 크기를 더 줄입니다 */
  }
}

</style>

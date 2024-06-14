<template>
    <div class="container">
      <h2 class="my-4">📚 Book Recommend 📚</h2>
      <button class="btn" @click="recommendBooks">새로 추천받기</button>
      <div class="main"> 
        <div v-for="book in recommendedBooks" :key="book.id" class="card" style="width: 18rem;">
          <img class="card-img-top" :src="book.cover" :alt="book.title" @click="goToBookPage(book.isbn)" style="cursor: pointer;">
          <div class="card-body">
              <h4 class="card-title">책 제목 : {{ book.title }}</h4>
              <p class="card-text">{{ book.description }}</p>
          </div>
        </div>
      </div> 
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  
  // Mood를 route param에서 가져오기
  const route = useRoute()
  const mood = ref(route.params.mood)
  console.log(mood.value)
  
  // Weather 스토어에서 날씨 정보 가져오기
  import { useWeatherStore } from '@/stores/weather'
  const { weather } = useWeatherStore();
  
  // Router 사용 설정
  const router = useRouter()
  
  // 추천받은 책 리스트와 추천된 책 리스트
  const allBooks = ref([])
  const recommendedBooks = ref([])
  
  // 책 표지를 클릭했을 때 해당 디테일 페이지로 이동
  function goToBookPage(bookIsbn) {
  router.push({ name: 'bookpage', params: { bookIsbn: bookIsbn, mood: mood.value }})
  }
  
  // 랜덤으로 책 3개를 추천
  function recommendBooks() {
    const shuffled = [...allBooks.value].sort(() => 0.5 - Math.random())
    recommendedBooks.value = shuffled.slice(0, 3)
  }
  
  // axios로 책 추천 요청 보내기
  onMounted(() => {
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/cultures/recommend/book/',
      data: {
        mood: mood.value,
        weather: weather,
      },
    })
      .then((response) => {
        console.log(response.data)
        allBooks.value = response.data.books;
        recommendBooks()
      })
      .catch((error) => {
        console.log(error)
      })
  })
</script>
  
<style scoped>
 /* 추가 스타일을 여기에 작성하세요 */

.main {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px; /* 카드 사이의 간격을 추가합니다 */
  justify-items: center;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1200px; /* 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
  text-align: center;
}

.card {
  width: 20px;
  border: 1px solid #0f0f0f;
  border-radius: 5px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  height: 525px;
  padding: 20px 10px;
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  width: 30%;
  height: auto;
  padding-top: 10px;
  margin: auto;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  border: 2px solid #4CAF50;
  border-radius: 10 px;
  background-color: white;
  color: #4CAF50;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
  margin-bottom: 20px;
}

.btn:hover {
  background-color: #4CAF50;
  color: white;
}

/* 제목 스타일 */
h2 {
  margin-bottom: 20px;
  padding-top: 10px;
}


</style>
  
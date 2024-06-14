<template>
    <h2>🎥 Movie Recommend 🎥</h2>
    <div class="main">
        <button v-if="recommendedMovies"
        class="btn" 
        @click="recommendMovies">
            새로 추천받기
        </button>
        
        <div class="container" v-if="recommendMovies">
          <div v-for="movie in recommendedMovies" :key="movie.movie_id" class="card" style="width: 18rem;">
            <img class="card-img-top" :src="movie.poster" :alt="movie.title" @click="goToMoviePage(movie.movie_id)" style="cursor: pointer;">
            <div class="card-body">
                <h4 class="card-title">영화 제목 : {{ movie.title }}</h4>
                
                <p class="card-text">
                  <span v-if="movie.overview">
                    {{ movie.overview }}
                  </span>
                  <span v-else >
                    줄거리 준비중. . .  😂
                  </span>
                </p>
            </div>
          </div>
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useMoviesStore } from '@/stores/movie';
  import axios from 'axios'

  
  // Mood를 route param에서 가져오기
  const route = useRoute()
  const mood = ref(route.params.mood)
  // Weather 스토어에서 날씨 정보 가져오기
  import { useWeatherStore } from '@/stores/weather'
  const { weather } = useWeatherStore();
  
  // Router 사용 설정
  const router = useRouter()
  
  // 추천받은 책 리스트와 추천된 책 리스트
  const allMovies = ref([])
  const recommendedMovies = ref([])
  
  // 책 표지를 클릭했을 때 해당 디테일 페이지로 이동
  function goToMoviePage(movie_id) {
    router.push({ name: 'moviepage', params: { movie_id: movie_id }})
  }
  
  // 랜덤으로 영화 3개를 추천
  function recommendMovies() {
    const shuffled = [...allMovies.value].sort(() => 0.5 - Math.random())
    recommendedMovies.value = shuffled.slice(0, 3)
  }

  // axios로 영화 추천 요청 보내기
  onMounted(() => {

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/cultures/recommend/movie/',
      data: {
        mood: mood.value,
        weather: weather,
      },
    })
      .then((response) => {
        allMovies.value = response.data.movies;
        recommendMovies()
        const movieStore = useMoviesStore()
        movieStore.allMovies = response.data.movies // store에 저장 
      })
      .catch((error) => {
        console.log(error)
      })
  })
</script>
  
<style scoped>
  /* 추가 스타일을 여기에 작성하세요 */
  h2{
    text-align: center;
  }
  .main{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .container {
    display: flex;
    max-width: 1200px; /* 최대 너비 설정 */
    gap:10px;
    margin: 0 auto; /* 중앙 정렬 */
    text-align: center;
    flex-wrap: wrap;
    margin-bottom: 10%;
}

.card:hover {
  transform: scale(1.05);
}

.card{
    width: 400px;
    border: 1px solid #000000;
    border-radius: 5px;
    background-color: #ffffff;
    padding: 15px 30px;
}

img{
    width: 100%;
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

</style>
  
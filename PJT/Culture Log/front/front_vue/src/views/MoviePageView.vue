<template>
  <div v-if="find_movie" class="movie-page">
    <!-- 왼쪽에 위치한 영화 정보 -->
    <div class="movie_info background">
      <img :src="find_movie.poster">
      <h2>{{ find_movie.title }}</h2>
      <p style="margin-bottom: 10px;">
        <span v-for="genre in genres" :key="genre.id" class="genre" style="margin-right:5px">
          {{ genre }}
        </span>
      </p>
    </div>
    
    <!-- 오른쪽에 위치한 줄거리와 트레일러 -->
    <div class="trailer-and-overview">
      <div class="movie_trailer background">
        <h3>Trailer Video</h3>
        <div v-if="youtubeUrl">
          <iframe width="640" height="360" :src="youtubeUrl" frameborder="0"></iframe>
        </div>
        <div v-else>
          <p>트레일러 영상이 없습니다.. 😢</p>
        </div>
      </div>

      <div class="movie_overview background">
        <h3>Overview</h3>
        <div class="overview2">{{ find_movie.overview }}</div>
      </div>
    </div>
  </div>

  <div style="text-align: center; margin-top: 20px;">
    <button 
      @click="showReviewModal = true"
      class="review-button"
    >
      Save & Write Review
    </button>
  </div>
  
  <div v-if="showReviewModal" class="modal-overlay">
    <div class="modal">
      <h3>Review and Rating</h3>
      <label>
        리뷰:
        <textarea v-model="movieReview" maxlength="300" class="review-textarea" placeholder="300자 내로 작성해주세요 :)"></textarea>
      </label>
      
      <label>
      별점:
      <div class="rating-stars">
        <template v-for="star in 5">
          <span
            class="star"
            :class="{ 'filled': star <= movieRating }"
            @click="movieRating = star"
          >★</span>
        </template>
      </div>
    </label>
    <div>
      <button class="btn" @click="confirmSaveMovieReview"> 저장 </button>
      <button class="btn" @click="showReviewModal = false"> 취소 </button>
    </div>
    </div>
  </div>

</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMoviesStore } from '@/stores/movie';
import { useMoodStore } from '@/stores/mood';
import { useWeatherStore } from '@/stores/weather';
import { useAuthStore } from '@/stores/counter';
import { useUsersStore } from '@/stores/users';
import axios from 'axios';


const router = useRouter();
const route = useRoute();

const find_movie = ref(null);
const youtubeUrl = ref('');
const genres = ref(null);

const movieReview = ref('');
const movieRating = ref(0);
const savedMovieReview = ref('');
const savedMovieRating = ref(0);
const showMovieReview = ref(false); 
const showReviewModal = ref(false);

const confirmSaveMovieReview = () => {
  if (window.confirm('현재 정보를 저장하시겠습니까?')) {
    saveMovieReview();
  }
};

const saveMovieReview = () => {
  const moodStore = useMoodStore();
  const weatherStore = useWeatherStore();
  const authStore = useAuthStore();
  const token = authStore.getToken();
  const username = authStore.now_user;

  savedMovieReview.value = movieReview.value;
  savedMovieRating.value = movieRating.value;
  showMovieReview.value = true;
  showReviewModal.value = false;

  const requestData = {
    content: movieReview.value,
    score: movieRating.value,
    movie_id: find_movie.value.movie_id,
    mood: moodStore.mood.name,
    weather: weatherStore.weather
  };


  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/v1/cultures/reviews/create/',
    data: requestData,
    headers: {
      Authorization: `Token ${token}`
    }
  }).then(response => {
    router.push({ name: 'Profile', params: { username: username } });
  }).catch(error => {
    console.error('Error saving review:', error);
  });
};

onMounted(() => {
  const moodStore = useMoodStore();
  const weatherStore = useWeatherStore();
  const authStore = useAuthStore();
  const token = authStore.getToken();

  const movie_id = route.params.movie_id;
  const movieStore = useMoviesStore();
  const allMovies = movieStore.allMovies;
  find_movie.value = allMovies.find((movie) => movie.movie_id == movie_id);

  const requestData = {
    content: movieReview.value,
    score: movieRating.value,
    movie_id: find_movie.value.movie_id,
    mood: moodStore.mood.name,
    weather: weatherStore.weather
  };

  // choiced_movie 저장
  axios({
    method: 'post',
    url: `http://127.0.0.1:8000/api/v1/cultures/choice/movie/${movie_id}/`,
    data: requestData,
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.log(error);
    });

  genres.value = movieStore.genres
    .filter(genre => find_movie.value.genre.includes(genre.id))
    .map(genre => genre.name);

  // 트레일러 영상
  const tmdbKey = import.meta.env.VITE_TMDB_API_KEY;
  axios({
    method: 'GET',
    url: `https://api.themoviedb.org/3/movie/${movie_id}/videos?language=ko-KR`,
    headers: {
      accept: 'application/json',
      Authorization: `Bearer ${tmdbKey}`
    }
  })
    .then((response) => {
      const data = response.data;
      const youtubeId = data.results[0].key;
      youtubeUrl.value = `http://www.youtube.com/embed/${youtubeId}`;
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>

<style scoped>
  img {
    width: 100%;
    max-width: 280px;
  }

  .movie-page {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    margin: 20px;
    text-align: center;
  }

  .movie_info {
    flex: 3;
    margin-right: 20px;
    height: 350px; /* 높이를 줄여서 버튼이 보이도록 조정 */
  }

  .movie_overview {
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
    height: 150px; /* 높이를 줄여서 버튼이 보이도록 조정 */
  }

  .trailer-and-overview {
    flex: 7;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
 .movie_info.background {
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 12px;
    height: 600px; /* 트레일러 높이를 조정 */
  }


  .movie_trailer.background {
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 10px;
    height: 420px; /* 트레일러 높이를 조정 */
  }

  .background {
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 10px;
  }

  .review-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 1.2rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s, box-shadow 0.3s;
  }

  .review-button:hover {
    background-color: #45a049;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }

  .modal {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 80%;
    max-width: 400px;
    overflow: auto;
    z-index: 10000;
  }

  .modal h3 {
    margin-top: 0;
  }

  .modal label {
    margin-bottom: 10px;
  }

  .modal button {
    width: calc(50% - 10px);
  }

  .review-textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 20px;
  }

  .rating-stars {
    font-size: 24px;
  }

  .rating-stars .star {
    cursor: pointer;
  }

  .rating-stars .star.filled {
    color: gold;
  }

  .btn {
    padding: 10px 20px;
    font-size: 1rem;
    border: 2px solid #4CAF50;
    border-radius: 5px;
    background-color: white;
    color: #4CAF50;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s, border-color 0.3s;
    margin: 5px;
  }

  @media (max-width: 1225px) {
    .movie-page {
      flex-direction: column;
    }

    .movie_info, .trailer-and-overview {
      width: 100%;
      margin: 10px auto;
    }

    .background {
      margin-bottom: 20px;
    }

    img {
      width: 200px;
    }
  }
</style>



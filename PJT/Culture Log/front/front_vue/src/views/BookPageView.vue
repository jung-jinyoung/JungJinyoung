<template>
  <div>
    <!-- Wrapper for book info, timer, and page info -->
    <div class="content-wrapper">
      <!-- Left Column: Book Info -->
      <div class="left-column">
        <div class="card book-info">
          <div class="book-img">
            <img :src="onebook.cover" :alt="onebook.title" />
          </div>
          <h2>{{ onebook.title }}</h2>
          <div class="discription"> 
            <p>{{ onebook.description }}</p>
          </div>
         
        </div>
      </div>

      <!-- Right Column: Page Info and Timer -->
      <div class="right-column">
        <!-- Timer -->
        <div class="timer">
          <h3>Timer</h3>
          <div class="clock">{{ formattedTime }}</div>
          <button class="btn" @click="toggleTimer">{{ isRunning ? 'Pause' : 'Start' }}</button>
        </div>
        <!-- Page Info -->
        <div class="card page-info">
          <h3>페이지 정보  {{ book.pagesRead }} / {{ book.page }} ({{ readingPercentage }}%)</h3>
          <div class="page-inputs">
            <label>
              Total Pages:
              <input v-model.number="book.page" type="number" placeholder="Total Pages" />
            </label>
            <label>
              Pages Read:
              <input v-model.number="book.pagesRead" type="number" placeholder="Pages Read" />
            </label>
          </div>
        </div>

      </div>
    </div>

    <!-- Wrapper for Playlist -->
    <div class="playlist-wrapper">
      <Playlist />
    </div>

    <!-- Save Button -->
    <div class="save">
      <button class="btn" @click="openReviewModal">책 정보 저장하기</button>
    </div>

    <!-- Review Modal -->
<div v-if="showReviewModal" class="modal-overlay">
  <div class="modal">
    <h3>Review and Rating</h3>
    <label>
      리뷰:
      <textarea v-model="bookReview" class="review-textarea" placeholder="300자 내로 작성해주세요 :)"></textarea>
    </label>
    <label>
      별점:
      <div class="rating-stars">
        <template v-for="star in 5">
          <span
            class="star"
            :class="{ 'filled': star <= bookRating }"
            @click="bookRating = star"
          >★</span>
        </template>
      </div>
    </label>

    <button class="btn" @click="confirmSave">Save</button>
    <button class="btn" @click="showReviewModal = false">Cancel</button>
  </div>
  </div>
  </div>
</template>



<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import Playlist from '@/components/Playlist.vue';
import { useMoodStore } from '@/stores/mood';
import { useAuthStore } from '@/stores/counter';
import { useUsersStore } from '@/stores/users';
import { useWeatherStore } from '@/stores/weather';

const route = useRoute();
const router = useRouter();
const bookIsbn = route.params.bookIsbn;
const mood = ref(route.params.mood);
const onebook = ref({});
const book = ref({
  pagesRead: 0,
  page: 0,
});

const { weather } = useWeatherStore();
const bookReview = ref('');
const bookRating = ref(0);
const showReviewModal = ref(false);

const seconds = ref(0);
const minutes = ref(0);
const hours = ref(0);
const isRunning = ref(false);
let timerInterval = null;



const startTimer = () => {
  if (!isRunning.value) {
    isRunning.value = true;
    timerInterval = setInterval(() => {
      seconds.value++;
      if (seconds.value === 60) {
        seconds.value = 0;
        minutes.value++;
        if (minutes.value === 60) {
          minutes.value = 0;
          hours.value++;
        }
      }
    }, 1000);
  }
};

const stopTimer = () => {
  if (isRunning.value) {
    isRunning.value = false;
    clearInterval(timerInterval);
  }
};

const toggleTimer = () => {
  if (isRunning.value) {
    stopTimer();
  } else {
    startTimer();
  }
};

const formattedTime = computed(() => {
  return `${String(hours.value).padStart(2, '0')}:${String(minutes.value).padStart(2, '0')}:${String(seconds.value).padStart(2, '0')}`;
});

const readingPercentage = computed(() => {
  if (book.value.page > 0) {
    return Math.round((book.value.pagesRead / book.value.page) * 100);
  }
  return 0;
});

const openReviewModal = () => {
  showReviewModal.value = true;
  document.querySelector('.main-content').scrollTop = 0; // main-content의 스크롤을 맨 위로 이동
};

const confirmSave = () => {
  if (confirm('저장하시겠습니까?')) {
    saveBookInfo();
    saveReview();
    showReviewModal.value = false;
    router.push({ name: 'Profile', params: {username: username}}); // 리다이렉션을 위한 라우트 이름
  }
};

// console.log(onebook)

const saveBookInfo = () => {
  stopTimer();
  try {
    const authStore = useAuthStore();
    const userStore = useUsersStore();
    const token = authStore.getToken();
    const userId = userStore.getUserId();

    if (!token) throw new Error('No auth token found');
    if (!userId) throw new Error('No user ID found');
    
    const requestData = {
      book: onebook.value.id,
      choiced_by: userId,
      pages: book.value.page,
      now_page: book.value.pagesRead,
      time: formattedTime.value,
      mood: mood.value,
      weather: weather,
    };

    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/cultures/choice/book/${bookIsbn}/`,
      data: requestData,
      headers: {
        Authorization: `Token ${token}`,
      },
    }).then(response => {
      console.log('Book info saved:', response.data);
    }).catch(error => {
      console.error('Error saving book info:', error);
    });
  } catch (error) {
    console.error('Error getting auth token:', error);
  }
};

const saveReview = () => {
  try {
    const moodStore = useMoodStore();
    const weatherStore = useWeatherStore();
    const authStore = useAuthStore();
    const token = authStore.getToken();
    const username = authStore.now_user;

    // if (!token) throw new Error('No auth token found');
    // if (!userId) throw new Error('No user ID found');

    const requestData = {
      content: bookReview.value,
      score: bookRating.value,
      book_id: onebook.value.id,
      mood: moodStore.mood.name,
      weather: weatherStore.weather


    };

    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/cultures/reviews/create/`,
      data: requestData,
      headers: {
        Authorization: `Token ${token}`,
      },
    }).then(response => {
      router.push({ name: 'Profile', params: { username: username } });

      console.log('Review saved:', response.data);
    }).catch(error => {
      console.error('Error saving review:', error);
    });
  } catch (error) {
    console.error('Error getting auth token:', error);
  }
};

onMounted(() => {
  axios.get(`http://127.0.0.1:8000/api/v1/cultures/books/${bookIsbn}/`)
    .then(response => {
      onebook.value = response.data;
      console.log(onebook.value);
    })
    .catch(error => {
      console.error('Error loading book data:', error);
    });
});
</script>

<style scoped>

.content-wrapper {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  
}

.left-column, .right-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.left-column {
  flex: 0 1 60%; 
  
}

.right-column {
  flex: 0 1 40%
}

.card {
  width: 98%; /* To occupy the entire width of the column */
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  height: 100%;
}

.card img {
  max-width: 100%;
  border-radius: 8px;
}

.card h2 {
  font-size: 1.5rem;
  margin: 10px 0;
}

.card p {
  font-size: 1rem;
  color: #555;
}

.page-info {
  text-align: center;
  font-size: 1rem;
  color: #333;
}

.page-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.page-inputs label {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-inputs input {
  margin-top: 5px;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 25%;
}

.timer {
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.clock {
  font-size: 2rem;
  font-weight: bold;
  font-family: 'Courier New', Courier, monospace;
  padding: 10px;
  border: 2px solid #4CAF50;
  border-radius: 5px;
  display: inline-block;
  margin-bottom: 10px;
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

.save {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.btn:hover {
  background-color: #4CAF50;
  color: white;
}

.discription {
  display: flex;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  padding: 10px; /* 위아래 공간 추가 */
  margin: 0 20px; /* 좌우 여백 추가 */
  text-align: center; /* 텍스트 가운데 정렬 */
}

.playlist-wrapper {
  width: auto;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: auto;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
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

.book-img {
  margin-top: 10px
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

</style>


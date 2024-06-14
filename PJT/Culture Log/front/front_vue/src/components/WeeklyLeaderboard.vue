<template>
  <div class="leaderboard">
    <button @click="refreshRankings">실시간 순위 확인하기</button>
    <section>
      <h2>Weekly Top Users</h2>
      <ol>
        <li v-for="user in topUsers" :key="user.username">
          <div @click="goToMyPage(user.username)" class="profile-wrapper">
            <img 
              :src="user.profile_image" 
              alt="Profile Image" 
              v-if="user.profile_image"
              class="profile-image"
            />
            {{ user.username }}
          </div>
        </li>
      </ol>
    </section>

    <section>
      <h2>Top Recommended Movies</h2>
      <ol>
        <li v-for="movie in topMovies" :key="movie.movie_id">
          <img :src="movie.poster" alt="Poster" />
          {{ movie.title }}
        </li>
      </ol>
    </section>

    <section>
      <h2>Top Recommended Books</h2>
      <ol>
        <li v-for="book in topBooks" :key="book.isbn">
          <img :src="book.cover" alt="Book Cover" />
          {{ book.title }}
        </li>
      </ol>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter()

const goToMyPage = (username) => {
  router.push({ name: 'Profile', params: { username: username } });
}

const topUsers = ref([]);
const topMovies = ref([]);
const topBooks = ref([]);

const fetchWeeklyTopUsers = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/v1/cultures/weekly/users/');
  topUsers.value = response.data.slice(0, 5);
};

const fetchTopMovies = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/v1/cultures/weekly/movies/');
  topMovies.value = response.data.slice(0, 3);
};

const fetchTopBooks = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/v1/cultures/weekly/books/');
  topBooks.value = response.data.slice(0, 3);
};

const refreshRankings = () => {
  fetchWeeklyTopUsers();
  fetchTopMovies();
  fetchTopBooks();
};

onMounted(() => {
  refreshRankings();
});
</script>

<style scoped>
.profile-wrapper {
  cursor: pointer;
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

/* 프로필 사진에 마우스를 올렸을 때 포인터 변경 */
.profile-wrapper:hover {
  cursor: pointer;
}

.leaderboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

section {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
}

h2 {
  margin-bottom: 10px;
}

ol {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

button {
  align-self: flex-start;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>

<template>
  <div id="main_page">
    <div id="background">
      <video ref="backgroundVideo" muted autoplay loop @play="handlePlay" @pause="handlePause" 
             :class="{ blur: shouldBlur }">
        <source :src="videoSrc" type="video/mp4">
      </video>
    </div>
    <header>
        <nav>
          <RouterLink to="/" >
            <button class="nav_button">Home</button>
          </RouterLink>
          <span v-if="store.isLogin === false"> | 
            <RouterLink to="/signup">
              <button class="nav_button">SignUp</button>
            </RouterLink>
            <span> | </span>
            <RouterLink to="/login">
              <button class="nav_button">Login</button>
            </RouterLink>
          </span>
          <span v-else>
            <span> | </span>
              <button @click="goToPage" class="nav_button">
                MyPage
              </button>
            <span> | </span>
            <span href="#" @click="logout" class="nav_button">Logout</span>
          </span>
          <span> | </span>
          <RouterLink to="/ranking">
            <button class="nav_button">Community</button>
          </RouterLink>
        </nav>
    </header>
    
    <div class="main-content">
      <RouterView :weather="weather" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router';
import { useAuthStore } from './stores/counter';
import { useWeatherStore } from '@/stores/weather';
import { useUsersStore } from './stores/users';

const store = useAuthStore()
const router = useRouter()
const route = useRoute()

// const user = ref(store.now_user)
const logout = function() {
  store.logOut();

};

const goToPage = function() {
  router.push({name:'Profile', params:{username:store.now_user}})
}


const number = ref(null)
const weather = ref(null)
const isBlur = ref(false)
const backgroundVideo = ref(null)
const isPlaying = ref(false) // 비디오 재생 상태 추적을 위한 ref

// 비디오 재생 상태에 따른 블러 처리 여부를 결정하는 computed 속성
const shouldBlur = computed(() => {
  return isBlur.value && !isPlaying.value;
});

const handlePlay = () => {
  isPlaying.value = true;
};

const handlePause = () => {
  isPlaying.value = false;
};

onMounted(() => {
  const weather_store = useWeatherStore();
  // weather_store.CurrentLocation();
  // weather_store.getInformation(weather_store.lat, weather_store.lon);
  number.value = weather_store.weatherNumber;
  weather.value = weather_store.weather;
  console.log(weather.value)

  const user_store = useUsersStore()
  user_store.get_users()
});

const videoSrc = computed(() => {
  return `/media/background/${number.value}.mov`;
});

watch(route, (newRoute) => {
  if (newRoute.path === '/recommend/book' || newRoute.path === '/recommend/movie' || newRoute.name === 'Profile') {
    isBlur.value = true;
    if (backgroundVideo.value) {
      backgroundVideo.value.pause();
    }
  } else {
    isBlur.value = false;
    if (backgroundVideo.value) {
      backgroundVideo.value.play();
    }
  }
});

</script>


<style scoped>
header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
  background-color: rgba(0, 0, 0, 0.438);
  padding: 12px;
  color: white;
  font-size: 15px;
}



.nav_button {
  cursor: pointer;
  background: none;
  border: none;
  font-size: 15px;
  transition: color 0.3s, text-shadow 0.3s;
}

.nav_button:hover {
  color: #ffffff;
  text-shadow: 0 0 5px white;
}

a, button {
  border: none;
  background-color: transparent;
  color: white;
  font-size: 15px;
}

#background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

#background video {
  position: absolute;
  top: -50px; /* 비디오를 확대하기 위해 조정 */
  left: -50px; /* 비디오를 확대하기 위해 조정 */
  width: calc(100% + 100px); /* 원래 크기보다 크게 설정 */
  height: calc(100% + 100px); /* 원래 크기보다 크게 설정 */
  object-fit: cover;
}

#background video.blur {
  filter: blur(5px); /* 블러 효과 적용 */
}

#main_page {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  height: 100%;
  transition: opacity 0.5s;
}

.main-content {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 80%;  /* 고정된 너비 */
  max-width: 2400px;  /* 최대 너비 설정 */
  height: 77%;
  max-height: 1000px;  /* 최대 높이 설정 */
  transform: translate(-50%, -50%);
  z-index: 998;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 20px;
  color: black;
  overflow: auto;  /* 내용이 넘칠 경우 스크롤바 표시 */
}

@media (max-width: 768px) {
  .main-content {
    width: 80%;  /* 모바일에서 너비 조정 */
    height: 80%;  /* 모바일에서 높이 조정 */
    max-width: none;  /* 최대 너비 제한 해제 */
    max-height: none;  /* 최대 높이 제한 해제 */
    padding: 10px;
  }
}
</style>

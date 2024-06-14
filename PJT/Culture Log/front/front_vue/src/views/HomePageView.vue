<template>
  <div class="homepage">
    <!-- 로그인 한 유저일 경우  -->
    <div v-if="!isModalOpen" class="welcome-message">
      <div v-if="store.isLogin === true" class="fade-in">
      <h3 style="margin-bottom: 40px;">
        안녕하세요, {{ store.now_user }} 님! 👋<br>
      </h3>
      <div class="fade-in">
        <h4>
          {{ welcome }}
        </h4>
        <h4 class="fade-in">
          날씨와 어울리는 영화와 책을 추천해드리겠습니다!
        </h4>
        <button 
          @click="openModal()" 
          style="animation: fadeIn 5s ease-out">
          How are you feeling?
        </button>

      </div>
      
      
      </div>
      <!-- 로그인 한 유저가 아닐 경우  -->
      <div v-else class="fade-in">
        <h3>
          어서오세요. 오늘은 기분 좋은 일이 생길거에요!
        </h3>
        <h4 class="fade-in">
          날씨와 어울리는 영화와 책을 추천해드리겠습니다!
        </h4>
        <button @click="openModal()" class="fade-in">          
          How are you feeling?
        </button>
      </div>
          
    </div>
  </div> 
</template>
  
<script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/counter';
  import { useWeatherStore } from '@/stores/weather';

  const store = useAuthStore()
  const weather_store = useWeatherStore();
  const welcome =ref(null)
  onMounted(() => {
    const weather_store = useWeatherStore();
    const weatherDescriptions = {
    'Clear': '오늘은 맑고 화창하네요! 🌞',
    'Clouds': '오늘은 구름이 많고 흐릴 수도 있겠네요. 가벼운 산책은 어떠실까요? 😀',
    'Rain': '지금 비가 내리고 있네요! 💧',
    'Snow': '지금 눈이 내리고 있네요! 따뜻하게 입고 나가세요!🧣',
    'Thunderstorm': '천둥번개가 치는 날씨입니다. 안전에 유의하세요! ⚡',
    'Fog': '안개가 짙은 날씨입니다. 운전 시 조심하세요! 🚗',
    'Mist': '옅은 안개가 낀 날씨입니다. 우산을 챙겨주세요!🌂'
  }
    welcome.value = weatherDescriptions[weather_store.weather]
  });

  // Vue Router 인스턴스 생성
  const router = useRouter();

  // 모달의 열림/닫힘 상태를 관리하는 변수
  const isModalOpen = ref(false);

  // 모달을 열기 위한 함수
  const openModal = () => {
    isModalOpen.value = true
    // SelectMood 페이지로 이동
    router.push({ name: 'selectmood' });
  };

</script>
  
<style scoped>
  .homepage{
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 600px;
    min-height: 400px;
  }
  
  .welcome-message {
    text-align: center;
  }
  
  .fade-in {
    animation: fadeIn 2s ease-out;
  }

  button{
    margin-top: 20px;
    width: 100%;
    max-width: 300px;
    padding: 12px;
    border: none;
    border-radius: 4px;
    background-color: #000000;
    color: white;
    font-size: 20px;
    cursor: pointer;
    transition: background-color 0.3s;

  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
  
<!-- MainComponent.vue -->
<template>
    <main class="fade-in">
      <h2>오늘의 기분은 어떠신가요?</h2>
      <div class="mood_list" v-if="showModal !== true">
        <div v-for="mood in moods"
          class="moods" 
          :key="mood.name" 
          @click="goToRecommend(mood)">
          <img :src="mood.image" />
          <p style="font-weight: 400;">{{ mood.name }}</p>
        </div>
      </div>
      <Modal v-if="selectedMood" :mood = selectedMood.name :weather=weather />
    </main>
  </template>
  
  <script setup>
  import { ref, defineProps  } from 'vue'
  import { useRouter } from 'vue-router'
  import Modal from '@/components/Modal.vue'
  import { useMoodStore  } from '@/stores/mood';
  const router = useRouter();

  // 현재 날씨 prop 받기
  defineProps({
    weather: String,
  })
  
  const moodStore = useMoodStore()

  const selectedMood = ref(null);
  
  const goToRecommend = (mood) => {
    selectedMood.value=mood
    moodStore.mood = mood
  };

  // 모달 띄우기를 위한 상태 설정 
  const showModal = ref(false);
  
  // 기분에 따라 분류하여 객체 리스트 생성 
  const moods = [
    { name: 'HAPPY', image: '/moods/smile.png', description: 'Feeling happy and joyful.' },
    { name: 'SOSO', image: '/moods/soso.png', description: 'Feeling neutral or indifferent.' },
    { name: 'SAD', image: '/moods/sad.png', description: 'Feeling sad and down.' },
    { name: 'ANGRY', image: '/moods/angry.png', description: 'Feeling angry and irritated.' },
    { name: 'EXHAUSTED', image: '/moods/exhausted.png', description: 'Feeling confused and exhausted.' }
  ];

  </script>
  

  <style scoped>

  main {
    top:0
  }
  
  /* 감정 리스트 */
  .mood_list {
    display: flex;
    justify-content: space-around;
    padding : 0px 10px;
  }
  /* 애니메이션 적용 */
  .fade-in {
    animation: fadeIn 2s ease-out;
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
  .moods{
    cursor: pointer;
    transition: transform 0.3s ease; /* 애니메이션을 부드럽게 하기 위한 설정 */
  }
  .moods:hover {
      transform: scale(1.1); /* 커서가 가면 1.1배로 커지도록 설정 */
  }



  /* 각 감정들 정렬해두기 */
  .mood_list div {
    text-align: center;
    margin-right: 20px;
  }
  
  .mood_list img {
    width: 80px;
    height: 80px;
  }
  
  .mood_list p {
    margin-top: 10px;
    font-size: 16px;
  }
  
  /* 전체 Home View 구성  */
  main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  
  </style>
  
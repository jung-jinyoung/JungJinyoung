<template>
  <div v-if="show" class="modal">
    <div class="modal_content">
      <p style="font-size: 20px; margin-bottom: 0; font-weight: bolder;">TODAY</p>
      <p class="today ">
        <span>기분 {{ todayMood }}</span>  
        <span>날씨 {{ todayWeather }}</span>
      </p>
      <p 
        v-if="greeting"
        style="margin:10px 40px;
        padding:5px 10px ;  
        background-color: rgba(110, 110, 110, 0.22);">
        {{ greeting }}
      </p>
      <p 
        v-else
        style="margin:10px 40px;
        padding:5px 10px ;  
        background-color: rgba(110, 110, 110, 0.22);"

      >hello :)</p>
      <button 
      @click="goRecommend(mood)"
      style="animation: fadeIn 5s ease-out"
      class="btn"
      >
      Recommend
    </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, onMounted,defineEmits } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const mood = ref(null)
const weather = ref(null)

const router = useRouter();
const selectedMood = ref('');
const show = ref(true)


const greeting = ref(null)

const props = defineProps({
mood: String,
weather: String
});


mood.value = props.mood
weather.value =props.weather
const moods = {
  'HAPPY': '😆',
  'SOSO' : '🙂',
  'SAD' : '😢',
  'ANGRY' : '😡',
  'EXHAUSTED' : '🥴'
}
const weatherDescriptions = {
    'Clear': '🌞',
    'Clouds': '⛅',
    'Rain': '💧',
    'Snow': '⛄',
    'Thunderstorm': '⚡',
    'Fog': '💨',
    'Mist': '🌂'
  }
const todayMood = ref(null)
const todayWeather = ref(null)
onMounted(() => {
  axios({
    method : 'post',
    url:'http://127.0.0.1:8000/api/v1/cultures/greeting/',
    data: {
      mood : mood.value,
      weather : weather.value
    }
  })
    .then((response)=>{
      const now = mood.value
      todayMood.value = moods[now]
      todayWeather.value = weatherDescriptions[weather.value]
      greeting.value = response.data.greeting
    })
    .catch((error)=>{console.log(error)})
})

// recommend 페이지로 이동 하면서 mood와 weather 정보 넘겨주기
const goRecommend = (mood) => {
  router.push({ name: 'recommend', params: {mood: mood}})
}
</script>


<style scoped>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 800px;  /* Increase width */
  width: 100%;
  height: 100%;
  height: 400px; /* Increase height */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.modal_content{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px dashed rgb(85, 85, 85);
  border-radius: 10px;
  height: 100%;
  height:300px;
  padding:30px 50px
}
.today {
  margin-top: 15px ;
  display: flex; 
  text-align: center; 
  justify-content: center; 
  align-items: center; 
  gap:15px
}
.today span{
  padding:5px 10px ;
  border-radius: 50%;
  border: 1px dashed rgb(85, 85, 85);
}

.btn {
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
</style>

import { defineStore } from 'pinia'
import { useGeolocation } from './geologation'
import { ref,computed } from 'vue'
import axios from 'axios'

export const useWeatherStore = defineStore('Weather', () => {
  const { lat, lon, isPositionReady, getCurrentPosition } = useGeolocation()
  // 현재 위치 정보를 가져오는 액션
  function CurrentLocation() {
    getCurrentPosition()
  }
  const weatherAPIKey = import.meta.env.VITE_WEATHER_API_KEY

  // 현재 위치와 날씨 정보 초기화
  const city = ref(null)
  const weather = ref(null)
  
  // 비동기적 처리 
  const getInformation = function(lat, lon) {
    
    axios({
      method : 'get',
      url : `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${weatherAPIKey}`,
    })
      .then( res=>{
        city.value = res.data.name
        weather.value = res.data.weather[0].main
      } )
  }
  weather.value='Rain'

  // 날씨 조건에 따른 숫자 매핑 
  const numberListOfWeather = {
    'Clear' : [0, 1, 2],
    'Clouds' : [3, 4, 5],
    'Rain': [6, 7, 8],
    'Snow': [9, 10, 11],
    'Thunderstorm': [12, 13],
    'Fog' : [14, 15],
    'Mist' : [14, 15]
  }

  // 해당 날씨 value 에서 랜덤으로 가져오기
  const getRandomElement = function(arr){
    return arr[Math.floor(Math.random() * arr.length )]
  }

  // 날씨에 따라 가져온 숫자로 동영상 번호 출력하기
  const weatherNumber = computed (() =>{
    console.log(weather.value)
    // if (weather.value && numberListOfWeather[weather.value]){
    if (weather.value && numberListOfWeather[weather.value]){
      return getRandomElement(numberListOfWeather[weather.value])
    } else { return Math.floor(Math.random() * 5) + 16} // 위치가 거절되거나 에러 발생시 기본 배경화면들 중 랜덤 재생
  })


  return { lat, lon, isPositionReady, CurrentLocation, city, weather, // 위치 및 날씨 관련 
            getInformation, numberListOfWeather, getRandomElement, weatherNumber  // 배경화면 지정을 위한 리턴값
          
  }}, 
{ persist: true })

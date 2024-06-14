import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import '@/assets/font.css'



const app = createApp(App)

// Pinia 설정
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// 라우터 설정
app.use(router)

// 앱 마운트
app.mount('#app')

// // 위치 정보 가져와서 기상 정보 업데이트
// if ("geolocation" in navigator) {
//   navigator.geolocation.getCurrentPosition(
//     position => {
//       // 위치 정보를 가져온 후에 앱의 상태를 업데이트
//       useWeatherStore().fetchWeatherData(position.coords.latitude, position.coords.longitude)
//     },
//     error => {
//       console.error("Error getting geolocation:", error)
//     }
//   )
// } else {
//   console.error("Geolocation is not supported by this browser.")
// }

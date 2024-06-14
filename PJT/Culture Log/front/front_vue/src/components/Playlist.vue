<!-- src/components/playlist.vue -->
<template>
  <div class="playlist-section">
    <div>
      <h3>책과 함께 듣기 좋은 플레이리스트🔊</h3>
    </div>
    <div class="genre">
      <div class="choose">
        <select v-model="selectedGenre" @change="getRandomPlaylist">
          <option value="">장르 선택</option>
          <option v-for="genre in uniqueGenres" :key="genre" :value="genre">{{ genre }}</option>
        </select>
        <div style="margin-top: 10px;">  
          <button @click="recommendSongs">다른 노래 추천받기</button>
        </div>
      </div>
      <div>
        <iframe v-if="selectedPlaylistUrl" width="560" height="315" :src="selectedPlaylistUrl" frameborder="0" allowfullscreen></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const selectedGenre = ref('')
const playlists = ref([])
const selectedPlaylistUrl = ref('')

// 전체 플레이리스트 조회하기
onMounted(() => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/api/v1/cultures/playlist/'
  })
    .then(response => {
      playlists.value = response.data
    })
    .catch(error => {
      console.error('Error fetching playlists:', error)
    })
})

// 고유한 장르 목록 얻기
const uniqueGenres = computed(() => {
  const genres = playlists.value.map(playlist => playlist.genre)
  return [...new Set(genres)]
})

// 장르 선택에 따른 임의의 플레이리스트 가져오기
const getRandomPlaylist = () => {
  if (selectedGenre.value) {
    const genrePlaylists = playlists.value.filter(playlist => playlist.genre === selectedGenre.value)
    if (genrePlaylists.length > 0) {
      const randomIndex = Math.floor(Math.random() * genrePlaylists.length)
      const videoUrl = genrePlaylists[randomIndex].url
      selectedPlaylistUrl.value = convertToEmbedUrl(videoUrl)
    } else {
      selectedPlaylistUrl.value = ''
    }
  } else {
    selectedPlaylistUrl.value = ''
  }
}

// YouTube URL을 embed URL로 변환
const convertToEmbedUrl = (url) => {
  const videoIdMatch = url.match(/(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)/)
  return videoIdMatch ? `https://www.youtube.com/embed/${videoIdMatch[1]}` : ''
}

// 다른 노래 추천받기
const recommendSongs = () => {
  getRandomPlaylist()
}
</script>

<style scoped>
.genre {
  margin-bottom: 20px;
}

.choose {
  margin-bottom: 20px;
}
</style>

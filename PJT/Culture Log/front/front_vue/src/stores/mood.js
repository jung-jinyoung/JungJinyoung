import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMoodStore = defineStore('Mood', () => {
    const mood = ref(null)

    return { mood };
  }, { persist: true });
  
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useUsersStore } from './users'

import axios from 'axios'

export const useAuthStore = defineStore('Auth', () => {
  const API_URL = 'http://127.0.0.1:8000';
  const token = ref(null);

  const getToken = () => {
    return token.value;
  };

  const isLogin = computed(() => {
    return token.value !== null;
  });

  const router = useRouter()

  const signUp = function (payload) {
    const { username, password1, password2 } = payload;

    axios.post(`${API_URL}/accounts/signup/`, { username, password1, password2 })
      .then((response) => {
        const userStore = useUsersStore();
        userStore.get_users();
        window.alert('Welcome to our Site! 🤗');
        const password = password1;
        logIn({ username, password });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const now_user = ref(null);

  const logIn = function (payload) {
    const { username, password } = payload;

    axios.post(`${API_URL}/accounts/login/`, { username, password })
      .then((response) => {
        now_user.value = username;
        token.value = response.data.key;
        router.push({ name: 'HomePage' });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const logOut = function () {
    axios.post(`${API_URL}/accounts/logout/`)
      .then((response) => {
        now_user.value = null;
        token.value = null;
        window.alert('bye bye ❣');
        router.push({ name: 'HomePage' });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return { API_URL, signUp, logIn, token, isLogin, logOut, now_user, getToken };
}, { persist: true });

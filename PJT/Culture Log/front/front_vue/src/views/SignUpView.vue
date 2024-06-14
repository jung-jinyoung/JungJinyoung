<template>
    <div class="signup">
      <div class="signup_container">

        <h2>Hello :)</h2>
        <form @submit.prevent="signUp">
          <div class="input_container">
            <input type="text" v-model.trim="username" id="username" placeholder="username">
          </div>
          <div class="input_container">
            <input type="password" v-model.trim="password1" id="password1" placeholder="password">
          </div>
          <div class="input_container">
            <input type="password" v-model.trim="password2" id="password2" placeholder="rewrite password">
          </div>
          <input type="submit"  value="SignUp">
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/counter'
  
  const username = ref(null) 
  const password1 = ref(null)
  const password2 = ref(null)
  const store = useAuthStore()
  
  const signUp = function () {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value
    }
    store.signUp(payload)
  }
  
  </script>
  
  <style>
  .signup{
    display: flex; 
    justify-content: center; 
    margin-top: 100px;
  }

  .signup_container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: white;
    width: 60%;
    min-width: 250px;
    height: 100%;
    height: 400px;
    border: 1px solid rgb(99, 99, 99);
    border-radius: 10px;
  }

  .signup_container input[type="submit"] {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 4px;
    background-color: #000000;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .login_container input[type="submit"]:hover {
    background-color: #858585;
  }
  </style>
  
<template>
  <div class="login">
    <div class= "login_container">
      <h2>Welcome :)</h2>
      <form @submit.prevent="logIn">
        <div class="input_container">
          <input type="text" v-model.trim="username" id="username" placeholder="username">
        </div>
        <div class="input_container">
          <input type="password" v-model.trim="password" id="password" placeholder="password">
        </div>
        <input type="submit" value="Login">
      </form>
    </div>

  </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/counter'
  
  const username = ref(null)
  const password = ref(null)
  const store = useAuthStore()
  
  const logIn = function () {
    const payload = {
      username: username.value,
      password: password.value
    }
    store.logIn(payload)
  }
  
  </script>
  
  <style>
  .login{
    display: flex; 
    justify-content: center; 
    margin-top: 100px;
  }

  .login_container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: white;
    width: 50%;
    height: 100%;
    min-width: 250px;
    height: 400px;
    border: 1px solid rgb(99, 99, 99);
    border-radius: 10px;
  }

  h2{  
    margin-bottom: 20px;
    font-size: 24px;
    color: #333;
  }

  .input_container {
    width: 100%;
    margin-bottom: 20px;
  }
  .input_container input[type="text"],
  .input_container input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
  }

  .input_container input[type="text"]:focus,
  .input_container input[type="password"]:focus {
    border-color: #000000;
  }

  .login_container input[type="submit"] {
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
  
<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <div>
          <label for="email">Email:</label>
          <input type="email" v-model="email" required>
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" v-model="password" required>
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
      };
    },
    methods: {
      async login() {
        try {
          await axios.post('http://localhost:3000/login', { email: this.email, password: this.password });
          alert('Login successful');
          
        } catch (error) {
          alert('Login failed');
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add your styles here */
  </style>
  
import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';

const app = createApp(App);

app.config.globalProperties.$http = axios.create({
  baseURL: 'http://localhost:3000'
});
app.use(axios);
app.mount('#app');

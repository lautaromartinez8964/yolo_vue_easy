// filepath: /home/janeg/fastapi_vue_easy/services/frontend/src/main.js
import { createApp } from "vue";
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

// --- 样式导入 ---
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import '@fortawesome/fontawesome-free/css/all.min.css';

// --- Axios 全局配置 ---
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';

// --- Axios 响应拦截器 ---
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const originalRequest = error.config;
      if (!originalRequest._retry) {
        originalRequest._retry = true;
        store.dispatch('logOut');
        router.push('/login');
      }
    }
    return Promise.reject(error);
  }
);

// --- Vue 应用初始化 (标准模式) ---

// 1. 只创建一次应用实例
const app = createApp(App);

// 2. 只在这里按顺序安装插件
app.use(store);
app.use(router); // router 只在这里被 use() 一次

// 3. 只挂载一次应用
app.mount("#app");
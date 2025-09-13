import 'bootstrap/dist/css/bootstrap.css'
import { createApp } from 'vue'
import axios from 'axios'



import App from './App.vue'
import router from './router'

const app = createApp(App); //创建了Vue应用实例

axios.defaults.withCredentials = true;

axios.defaults.baseURL = 'http://localhost:5000/';  // axios请求的基础URL，指向本地运行的FastAPI后端

app.use(router); //将路由器插件集成到应用中
app.mount("#app");

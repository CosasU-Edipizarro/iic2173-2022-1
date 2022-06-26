import { createApp } from 'vue'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import store from "./store";
import router from "./router";
import "./assets/css/nucleo-icons.css";
import "./assets/css/nucleo-svg.css";
import SoftUIDashboard from "./soft-ui-dashboard";


// window.hostname = 'http://localhost:8000'
// window.hostname = process.env.API_URL
// window.hostname = 'http://api.iic2173-g19.xyz'
window.hostname = 'http://192.168.1.81:8000'

// window.hostname = 'https://30zwhcjsc2.execute-api.us-east-2.amazonaws.com/test'



createApp(App)
    .use(VueCookies, { expire: '7d' })
    .use(store)
    .use(router)
    .use(SoftUIDashboard)
    .mount('#app')

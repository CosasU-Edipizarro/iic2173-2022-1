import { createApp } from 'vue'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import store from "./store";
import router from "./router";
import "./assets/css/nucleo-icons.css";
import "./assets/css/nucleo-svg.css";
import SoftUIDashboard from "./soft-ui-dashboard";

// window.hostname = 'http://localhost'
window.hostname = 'https://api.iic2173-g19.xyz'
// window.hostname = 'https://letythd4le.execute-api.us-east-2.amazonaws.com'


createApp(App)
    .use(VueCookies, { expire: '7d' })
    .use(store)
    .use(router)
    .use(SoftUIDashboard)
    .mount('#app')

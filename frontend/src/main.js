import { createApp } from 'vue'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import store from "./store";
import router from "./router";
import "./assets/css/nucleo-icons.css";
import "./assets/css/nucleo-svg.css";
import SoftUIDashboard from "./soft-ui-dashboard";


// window.hostname = 'https://30zwhcjsc2.execute-api.us-east-2.amazonaws.com/test'

window.hostname = 'http://api.iic2173-g19.xyz'
window.auth_hostname = 'http://auth.iic2173-g19.xyz'
window.chat_hostname = 'http://chat.iic2173-g19.xyz'
window.ws_hostname = 'ws://chat.iic2173-g19.xyz'
window.sentiment = 'https://30zwhcjsc2.execute-api.us-east-2.amazonaws.com/test/comprehendLambda'

// window.hostname = 'http://192.168.1.81:8000'
// window.auth_hostname = 'http://192.168.1.81:8080'
// window.chat_hostname = 'http://192.168.1.81:8088'
// window.ws_hostname = 'ws://192.168.1.81:8088'


createApp(App)
    .use(VueCookies, { expire: '7d' })
    .use(store)
    .use(router)
    .use(SoftUIDashboard)
    .mount('#app')

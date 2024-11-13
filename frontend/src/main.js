import {createApp} from 'vue';
import {createRouter, createWebHistory} from 'vue-router';

import App from '@/App.vue';

import ChatBotView from '@/views/ChatBotView.vue';

import '@/styles/style.css';

const routes = [
  {path: '/', name: 'root', component: ChatBotView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.use(router);
app.mount('#app');

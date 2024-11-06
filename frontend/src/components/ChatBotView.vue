<template>
  <h1>Franklin</h1>

  <button @click="askFranklin()">Send Message</button>

  <p>{{ franklinResponse }}</p>
  <p>{{ chatBotStore.conversation }}</p>
</template>

<script setup>

import { ref } from 'vue';

import { chatBotStore } from '@/stores/ChatBotStore';

const franklinResponse = ref('Hello World??');

async function askFranklin() {
  console.log("Chatbot Hello?")
  try {
    console.log(await chatBotStore.sendMessage());
  }
  catch (error) {
    console.log("Franklin Send Message: " + error);
  }
}

</script>

<style scoped>

.read-the-docs {
  color: #888;
}

</style>

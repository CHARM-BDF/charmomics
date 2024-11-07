<template>
  <h1>Franklin</h1>

  <button @click="askFranklin()">Send Message</button>

  <p>{{ chatBotStore.conversation }}</p>
</template>

<script setup>

import { chatBotStore } from '@/stores/chatBotStore.js';

async function askFranklin() {
  try {
    await chatBotStore.sendMessage()
  } catch (error) {
    console.log("Franklin Send Message: " + error);
  }
}

</script>

<style scoped>

.read-the-docs {
  color: #888;
}

</style>

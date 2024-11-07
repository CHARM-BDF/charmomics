<template>
  <h1>Franklin</h1>

  <p>{{ chatBotStore.conversation }}</p>

  <input v-model="userPrompt" />

  <button @click="askFranklin()">Send Message</button>
</template>

<script setup>

import { ref } from 'vue';

import { chatBotStore } from '@/stores/chatBotStore.js';

let userPrompt = ref("");

async function askFranklin() {
  
  const prompt = {
    "sender": "user",
    "message": userPrompt.value
  }

  console.log(prompt)

  try {
    await chatBotStore.sendPrompt(prompt)
  } catch (error) {
    console.log("Franklin Send Prompt: " + error);
  }
}

</script>

<style scoped>

input {
  height: 30px;
  width: 450px;
  border: solid;
  border-width: 3px;
  border-color: gainsboro;
  border-radius: 7px;
  margin-right: 10px;
}

</style>

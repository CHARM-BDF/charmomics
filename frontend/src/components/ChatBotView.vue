<template>
  <h1>Franklin</h1>

  <ChatBotSection
    :conversation="chatBotStore.conversation"
  />

  <input class="promptInput" v-model="userPrompt" />

  <button class="sendMessageButton" @click="askFranklin()">Send Message</button>
</template>

<script setup>

import { onMounted, ref } from 'vue';

import { chatBotStore } from '@/stores/chatBotStore.js';

import ChatBotSection from './ChatBot/ChatBotSection.vue';

let userPrompt = ref("");

async function askFranklin() {
  
  const message = {
    "user": "developer",
    "message": userPrompt.value
  }

  this.userPrompt = "";

  try {
    await chatBotStore.sendMessage(message)
    
  } catch (error) {
    console.log("Franklin Send Prompt: " + error);
  }
}

onMounted(async () => {
  await chatBotStore.getConversation();
})

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

.promptInput {
  margin-top: .5rem;
}

.sendMessageButton {
  margin-top: .5rem;
}

</style>

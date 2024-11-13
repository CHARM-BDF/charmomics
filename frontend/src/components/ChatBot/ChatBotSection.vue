<template>
  <div class="conversationSection">
    <ChatBotMessage
      v-for="message in props.conversation"
      :key="message.message"
      :user="message.user"
      :message="message.message"
    />
  </div>
</template>

<script setup>

import ChatBotMessage from '@/components/ChatBot/ChatBotMessage.vue';

const props = defineProps({
  conversation: {
    type: Array,
    default() {
      return [];
    },
  },
});

</script>

<style setup>

.conversationSection {
    display: grid;
    grid-template-rows: auto;
    height: 100%;
    overflow: scroll;
}

</style>

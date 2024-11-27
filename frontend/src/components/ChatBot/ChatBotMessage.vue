<template>
  <div
    class="chatBubble"
    :class="isUser"
  >
    {{ message }}
  </div>
</template>

<script setup>

import {computed} from 'vue';

const props = defineProps({
  user: {
    type: String,
    default: '',
  },
  message: {
    type: String,
    default: '',
  },
});

const isUser = computed({
  get() {
    if (props.user == 'assistant') {
      return 'assistantBubble';
    }

    return 'rightBubble';
  },
});

</script>

<style scoped>

.chatBubble {
  padding: .5rem;
  margin: .25rem;
  
  white-space: pre-line;
}

.assistantBubble {
  text-align: left;
  justify-self: start;
}

.rightBubble {
  background-color: #F9F9F9;
  border: none;
  border-width: .115rem;
  border-radius: .5rem;
  text-align: left;
  max-width: 75%;
  justify-self: end;
  padding: .5rem 1rem .5rem 1rem;
}

</style>

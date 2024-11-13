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
      return 'leftBubble';
    }

    return 'rightBubble';
  },
});

</script>

<style scoped>

.chatBubble {
    padding: .5rem;
    margin: .25rem;
    border: solid;
    border-width: .115rem;
    border-radius: .5rem;
    white-space: pre-line;
}

.leftBubble {
    background-color: salmon;
    text-align: left;
    max-width: 75%;
    justify-self: start;
}

.rightBubble {
    background-color: aquamarine;
    text-align: left;
    max-width: 75%;
    justify-self: end;
}

</style>

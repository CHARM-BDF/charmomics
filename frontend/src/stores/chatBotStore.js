import {reactive} from 'vue';

import ChatBotModel from '@/models/chatBotModel.js';

export const chatBotStore = {
  conversation: reactive([]),

  async getConversation() {
    const conversation = await ChatBotModel.getConversation();

    Object.assign(this.conversation, conversation);
  },

  async sendMessage(message) {
    this.conversation.push(message);

    const botResponse = await ChatBotModel.sendMessage(message);

    this.conversation.push(botResponse);
  },
};

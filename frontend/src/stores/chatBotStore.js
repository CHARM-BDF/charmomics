import { reactive } from 'vue';

import Requests from '@/requests.js';

export const chatBotStore = reactive({
    conversation: {},

    async sendPrompt(data) {
        const baseURL = '/api';
        const urlQuery = '/query';
        
        const conversationResponse = await Requests.postForm(baseURL+ urlQuery, data);
        
        Object.assign(this.conversation, conversationResponse)
    }
});

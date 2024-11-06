import { reactive } from 'vue';

import Requests from '@/requests.js';

export const chatBotStore = reactive({
    conversation: {},

    async sendMessage() {
        const baseURL = '/api';
        const urlQuery = '/';
        const conversationResponse = await Requests.get(baseURL+ urlQuery);
        Object.assign(this.conversation, conversationResponse)
        

        // return await Requests.get(baseURL + urlQuery)
    },

});

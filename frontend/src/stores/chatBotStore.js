import { reactive } from 'vue';

import Requests from '@/requests.js';

export const chatBotStore = reactive({
    conversation: [],

    async getConversation() {
        const baseURL = '/api';
        const urlQuery = '/conversation';

        const fetchedConversation = await Requests.get(baseURL + urlQuery);

        console.log(fetchedConversation)

        Object.assign(this.conversation, fetchedConversation);
    },

    async sendMessage(data) {
        const baseURL = '/api';
        const urlQuery = '/query';

        this.conversation.push(data)

        console.log(data)
        
        const conversationResponse = await Requests.postForm(baseURL+ urlQuery, data);

        this.conversation.push(conversationResponse);
    }
});

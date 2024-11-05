import { reactive } from 'vue';

import Requests from '@/requests';

export const chatBotStore = reactive({
    conversationMessages: [],

    async sendMessage() {
        const baseURL = '/api/query';
        const urlQuery = '/';

        
    },

})
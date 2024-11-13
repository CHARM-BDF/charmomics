import Requests from '@/requests.js';

export default {
  async getConversation() {
    const baseURL = '/api';
    const urlQuery = '/conversation';

    const response = await Requests.get(baseURL + urlQuery);

    return response;
  },
  async sendMessage(data) {
    const baseURL = '/api';
    const urlQuery = '/query';

    const response = await Requests.postForm(baseURL+ urlQuery, data);

    return response;
  },
};

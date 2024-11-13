import {afterEach, beforeAll, describe, expect, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import ChatBotView from '@/views/ChatBotView.vue';
import ChatBotSection from '@/components/ChatBot/ChatBotSection.vue';

import ChatBotModel from '@/models/chatBotModel.js';

function getMountedComponent() {
  return shallowMount(ChatBotView);
};

describe('ChatBotView.vue', () => {
  let sandbox;

  beforeAll(() => {
    sandbox = sinon.createSandbox();

    sandbox.stub(ChatBotModel, 'getConversation').resolves(messageFixtureData);
  });

  afterEach(() => {
    sandbox.reset();
  });

  it('should contain three messages in the conversation prop', async () => {
    const view = getMountedComponent();
    const chatBotSectionComponent = view.findComponent(ChatBotSection);

    await view.vm.$nextTick();

    expect(chatBotSectionComponent.vm.conversation.length).to.equal(3);
  });

  it('should add a message when the clicks send message button', async () => {
    const view = getMountedComponent();
    const chatBotSectionComponent = view.findComponent(ChatBotSection);

    await view.vm.$nextTick();

    expect(chatBotSectionComponent.vm.conversation.length).to.equal(3);

    view.vm.userPrompt = 'Hello!';

    const chatBotSendMessageButton =  view.find('[data-test=chat-bot-send-message-button]');

    chatBotSendMessageButton.trigger('click');

    await view.vm.$nextTick();

    expect(chatBotSectionComponent.vm.conversation.length).to.equal(4);
  });
});

const messageFixtureData = [
  {user: 'assistant', message: 'Hello'},
  {user: 'developer', message: 'How are you?'},
  {user: 'assistant', message: 'I am good, how are you?'},
];

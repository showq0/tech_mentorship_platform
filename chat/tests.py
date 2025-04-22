import time
import logging
from django.test import TestCase
from mentorship.models import User, Mentorship
from chat.models import Message, Conversation

logging.basicConfig(
    filename='user_chats_performance.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='test123', role='mentor')
        self.user2 = User.objects.create_user(username='user2', password='test123', role='mentee')
        self.user3 = User.objects.create_user(username='user3', password='test123', role='mentee')

        self.mentorship1 = Mentorship.objects.create(mentor=self.user1, mentee=self.user2)
        self.mentorship2 = Mentorship.objects.create(mentor=self.user1, mentee=self.user3)

        self.conversation1 = Conversation.objects.create(mentorship=self.mentorship1)
        self.conversation2 = Conversation.objects.create(mentorship=self.mentorship2)

        Message.objects.create(
            conversation=self.conversation1,
            sender=self.user1,
            content="Hello",
            is_read=False
        )
        Message.objects.create(
            conversation=self.conversation1,
            sender=self.user2,
            content="Hi",
            is_read=True
        )
        Message.objects.create(
            conversation=self.conversation2,
            sender=self.user3,
            content="Yo",
            is_read=False
        )

    def test_get_chat_partners(self):
        start_time = time.time()
        chat_partners = Message.get_user_chats(self.user1)
        end_time = time.time()

        response_time = end_time - start_time

        logging.info(f"Response time for user_chat v2 (user: {self.user1.username}): {response_time:.6f} seconds")

        self.assertIn(self.user2, chat_partners)
        self.assertIn(self.user3, chat_partners)
        self.assertNotIn(self.user1, chat_partners)
        self.assertEqual(len(chat_partners), 2)

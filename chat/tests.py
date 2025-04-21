import time
import logging
from django.test import TestCase
from mentorship.models import User
from chat.models import Message

logging.basicConfig(
    filename='user_chats_performance.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='test123')
        self.user2 = User.objects.create_user(username='user2', password='test123')
        self.user3 = User.objects.create_user(username='user3', password='test123')

        Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello", is_read=False)
        Message.objects.create(sender=self.user2, receiver=self.user1, content="Hi", is_read=True)
        Message.objects.create(sender=self.user3, receiver=self.user1, content="Yo", is_read=False)

    def test_get_chat_partners(self):
        start_time = time.time()
        chat_partners = Message.get_chat_partners(self.user1)
        end_time = time.time()

        response_time = end_time - start_time

        # Log response time
        logging.info(f"Response time for user_chat v1 (user: {self.user1.username}): {response_time:.6f} seconds")

        self.assertIn(self.user2, chat_partners)
        self.assertIn(self.user3, chat_partners)
        self.assertNotIn(self.user1, chat_partners)
        self.assertEqual(chat_partners.count(), 2)

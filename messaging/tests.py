from django.test import TestCase
from django.contrib.auth.models import User
from messaging.models import Message

# Create your tests here.
class MessageTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("John Doe", "johndoe@gmail.com", "johndoe")
        self.testUser1 = User.objects.create_user("Jane Doe", "janedoe@gmail.com", "janedoe")
        Message.objects.create(sender=self.testUser, receiver=self.testUser1, content="test message content")
    
    def tearDown(self):
        self.testUser.delete()
        self.testUser1.delete()

    def test_message_retrieve_by_sender(self):
        msg = Message.objects.get(sender=self.testUser)
        self.assertEqual(msg.receiver, self.testUser1)
        self.assertEqual(msg.content, "test message content")

    def test_message_retrieve_by_receiver(self):
        msg = Message.objects.get(receiver=self.testUser1)
        self.assertEqual(msg.sender, self.testUser)
        self.assertEqual(msg.content, "test message content")
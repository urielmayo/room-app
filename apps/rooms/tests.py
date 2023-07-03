from django.test import TestCase, Client
from .models import Room, Message
from apps.users.models import User
from django.urls import reverse


# Create your tests here.
class RoomsTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin@mail.com', 'admin123')

        self.test_room_1 = Room.objects.create(name='Test Room 1')
        self.test_room_2 = Room.objects.create(name='This is another TeST')

        self.test_message_1 = Message.objects.create(
            sender=self.admin,
            room=self.test_room_1,
            content='This is a test message',
        )

    def test_model_relations(self):
        self.assertEqual(
            self.admin.messages.first(),
            self.test_message_1,
        )
        self.assertEqual(
            self.test_room_1.messages.first(),
            self.test_message_1,
        )

    def test_room_list_view(self):
        client = Client()
        response = client.get(reverse('rooms:list'))
        self.assertEqual(200, response.status_code)

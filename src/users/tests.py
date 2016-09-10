import json

from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.utils import timezone

from users.models import User
from users.serializers import UserSerializer, UserUpdateSerializer


class TestUserModel(TestCase):

    def test_user_create(self):
        user = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        self.assertIsInstance(user, User)
        self.assertIsNotNone(user.profile)
        self.assertIsNotNone(user.date_joined)

    def test_user_update(self):
        user = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        user.email = 'anotheruser@tshape.com'
        user.set_password('tshape1')
        user.username = 'anotheruser'
        user.first_name = 'ang'
        user.last_name = 'ie'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = False
        date = timezone.now()
        user.date_joined = date
        user.save()
        self.assertEqual(User.objects.get(pk=user.id), user)

        self.assertEqual(user.get_full_name(), 'ang ie')
        self.assertEqual(user.get_short_name(), 'ang')
        self.assertEqual(str(user), 'anotheruser@tshape.com')

    def test_user_send_email(self):
        user = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        user.email_user(
            'Subject here', 'Here is the message.',
            'from@example.com', fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')

    def test_user_validations(self):
        user = User(password='try$h1s')
        err_msg = "{'email': ['This field cannot be blank.']}"
        with self.assertRaisesMessage(ValidationError, err_msg):
            user.save()

        User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        user = User(
            email='test1@tshape.com', password='try$h1s')
        err_msg = 'A user with that email already exists.'
        with self.assertRaisesMessage(ValidationError, err_msg):
            user.save()


class TestUserAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        self.user_2 = User.objects.create(
            email='test2@tshape.com', password='try$h1s')

    def test_user_get(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        expected = UserSerializer(users, many=True).data
        self.assertEqual(response.data, expected)

    def test_user_post(self):
        data = {'email': 'rob@tshape.com', 'password': 'test123'}
        response = self.client.post(
            '/api/users/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        user = User.objects.filter(email='rob@tshape.com').first()
        expected = UserSerializer(user).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['email'], data['email'])

    def test_user_put(self):
        data = {'email': 'angie@tshape.com', 'is_staff': True}
        response = self.client.put(
            '/api/users/{}/'.format(self.user_1.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(pk=self.user_1.id)
        expected = UserUpdateSerializer(user).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['is_staff'], data['is_staff'])

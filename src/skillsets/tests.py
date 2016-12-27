import json

from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from skillsets.models import Skillset
from skillsets.serializers import SkillsetSerializer
from users.models import User


class TestSkillsetModel(TestCase):

    def test_skillset_create(self):
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        self.assertIsInstance(skillset, Skillset)
        self.assertEqual(Skillset.objects.first(), skillset)
        self.assertIsNotNone(skillset.created_at)
        self.assertIsNotNone(skillset.updated_at)

    def test_skillset_update(self):
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=5)
        skillset.name = 'javascript'
        skillset.description = 'front end'
        skillset.verified = False
        skillset.weight = 10
        skillset.save()
        self.assertEqual(Skillset.objects.first(), skillset)
        self.assertEqual(str(skillset), 'javascript')

    def test_skillset_validations(self):
        Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        skillset = Skillset(
            name='python', description='best ever', verified=True, weight=10)
        err_msg = 'A skillset with that name already exists.'
        with self.assertRaisesMessage(ValidationError, err_msg):
            skillset.save()


class TestSkillsetAPI(TestCase):

    def setUp(self):
        password = 'mypassword123'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)
        self.skillset_1 = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        self.skillset_2 = Skillset.objects.create(
            name='html', description='front end', verified=True, weight=10)

    def test_skillset_get(self):
        response = self.client.get('/api/skillsets/')
        self.assertEqual(response.status_code, 200)
        skillsets = Skillset.objects.all()
        expected = SkillsetSerializer(skillsets, many=True).data
        self.assertEqual(response.data, expected)

    def test_skillset_post(self):
        data = {'name': 'javascript', 'description': 'front end'}
        response = self.client.post(
            '/api/skillsets/',
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        skillset = Skillset.objects.filter(name='javascript').first()
        expected = SkillsetSerializer(skillset).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])

    def test_skillset_put(self):
        data = {'name': 'ruby', 'verified': False}
        response = self.client.put(
            '/api/skillsets/{}/'.format(self.skillset_1.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        skillset = Skillset.objects.get(pk=self.skillset_1.id)
        expected = SkillsetSerializer(skillset).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['verified'], data['verified'])

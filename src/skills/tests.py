import json

from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from skills.models import Skill
from skills.serializers import SkillSerializer
from skillsets.models import Skillset
from users.models import User


class TestSkillModel(TestCase):

    def test_skill_create(self):
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        skill = Skill.objects.create(
            name='loops', verified=True, skillset_id=skillset.id, weight=5)
        self.assertIsInstance(skill, Skill)
        self.assertEqual(Skill.objects.first(), skill)
        self.assertIsNotNone(skill.created_at)
        self.assertIsNotNone(skill.updated_at)

    def test_skill_update(self):
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        skill = Skill.objects.create(
            name='loops', verified=True, skillset_id=skillset.id, weight=5)
        skill.name = 'ang'
        skill.description = 'Chief Nerd Officer'
        skill.verified = False
        skill.weight = 10
        skill.save()
        self.assertEqual(Skill.objects.first(), skill)
        self.assertEqual(str(skill), 'ang')

    def test_skills_skillsets(self):
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        skill = Skill.objects.create(
            name='loops', verified=True, skillset_id=skillset.id, weight=5)
        self.assertEqual(skill.skillset, skillset)

    def test_skills_validations(self):
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        skill = Skill(name='loops', verified=True, skillset_id=skillset.id)
        err_msg = 'Verified skills must have a weight.'
        with self.assertRaisesMessage(ValidationError, err_msg):
            skill.save()


class TestSkillAPI(TestCase):

    def setUp(self):
        password = 'mypassword123'
        my_admin = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.client = Client()
        self.client.login(username=my_admin.username, password=password)
        self.skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        self.skill_1 = Skill.objects.create(
            name='loops', verified=True,
            skillset_id=self.skillset.id, weight=5)
        self.skill_2 = Skill.objects.create(
            name='meta programming', verified=True,
            skillset_id=self.skillset.id, weight=5)

    def test_skill_get(self):
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 200)
        skills = Skill.objects.all()
        expected = SkillSerializer(skills, many=True).data
        self.assertEqual(response.data, expected)

    def test_skillset_skill_get(self):
        response = self.client.get(
            '/api/skillsets/{}/skills/'.format(self.skillset.id))
        self.assertEqual(response.status_code, 200)
        skills = Skill.objects.all()
        expected = SkillSerializer(skills, many=True).data
        self.assertEqual(response.data, expected)

    def test_skill_post(self):
        data = {'name': 'pep 8', 'description': 'zen of python',
                'skillset_id': self.skillset.id}
        response = self.client.post(
            '/api/skills/',
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        skillset = Skill.objects.filter(name='pep 8').first()
        expected = SkillSerializer(skillset).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['skillset_id'], data['skillset_id'])

    def test_skillset_skills_post(self):
        data = {'name': 'list comprehensions', 'description': 'efficient ones',
                'skillset_id': self.skillset.id}
        response = self.client.post(
            '/api/skillsets/{}/skills/'.format(self.skillset.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        skillset = Skill.objects.filter(name='list comprehensions').first()
        expected = SkillSerializer(skillset).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['skillset_id'], data['skillset_id'])

    def test_skill_put(self):
        data = {'name': 'generators', 'verified': False, 'weight': None}
        response = self.client.put(
            '/api/skills/{}/'.format(self.skill_1.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        skill = Skill.objects.get(pk=self.skill_1.id)
        expected = SkillSerializer(skill).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['verified'], data['verified'])
        self.assertEqual(response.data['weight'], data['weight'])

    def test_skillset_skills_put(self):
        data = {'name': 'generators', 'verified': False, 'weight': None}
        response = self.client.put(
            '/api/skillsets/{}/skills/{}/'.format(
                self.skillset.id, self.skill_1.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        skill = Skill.objects.get(pk=self.skill_1.id)
        expected = SkillSerializer(skill).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['verified'], data['verified'])
        self.assertEqual(response.data['weight'], data['weight'])

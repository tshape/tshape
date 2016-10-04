import json

from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from profiles.models import Profile, ProfileSkillset, ProfileSkill
from profiles.serializers import ProfileSerializer

from skills.models import Skill
from skills.serializers import ProfileSkillSerializer
from skillsets.models import Skillset
from skillsets.serializers import ProfileSkillsetSerializer
from users.models import User


class TestProfileModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test1@tshape.com', password='try$h1s')

    def test_profile_create(self):
        self.assertIsNotNone(self.user.profile)
        self.assertIsInstance(self.user.profile, Profile)
        self.assertIsNotNone(self.user.profile.created_at)
        self.assertIsNotNone(self.user.profile.updated_at)

    def test_profile_update(self):
        profile = self.user.profile
        profile.first_name = 'ang'
        profile.last_name = 'ie'
        profile.title = 'CNO'
        profile.description = 'Chief Nerd Officer'
        profile.years_experience = 100
        profile.save()
        self.assertEqual(Profile.objects.first(), profile)
        self.assertEqual(str(self.user.profile), 'ang ie')

    def test_profile_skills_skillsets(self):
        profile = self.user.profile
        self.assertEqual(len(profile.skillsets.all()), 0)
        self.assertEqual(len(profile.skills.all()), 0)

        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        ProfileSkillset.objects.create(
            profile_id=profile.user_id,
            skillset_id=skillset.id, profile_weight=10)
        self.assertEqual(len(profile.skillsets.all()), 1)
        self.assertEqual(profile.skillsets.first(), skillset)
        self.assertEqual(profile.skillset_ids, [skillset.id])

        skill = Skill.objects.create(
            name='loops', verified=True, skillset_id=skillset.id, weight=5)
        ProfileSkill.objects.create(
            profile_id=profile.user_id, skill_id=skill.id, profile_weight=5)
        self.assertEqual(len(profile.skills.all()), 1)
        self.assertEqual(profile.skills.first(), skill)
        self.assertEqual(profile.skill_ids, [skill.id])

    def test_profile_skills_validations(self):
        profile = self.user.profile
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=100)
        self.assertEqual(Skillset.objects.count(), 1)

        skill = Skill.objects.create(
            name='loops', verified=True, weight=1, skillset_id=skillset.id)
        profile_skill = ProfileSkill(
            profile_id=profile.user_id, skill_id=skill.id, profile_weight=1)
        err_msg = 'Corresponding skillset must be attached to profile before skill.'
        with self.assertRaisesMessage(ValidationError, err_msg):
            profile_skill.save()

        ProfileSkillset.objects.create(
            profile_id=profile.user_id, skillset_id=skillset.id)
        ProfileSkill.objects.create(
            profile_id=profile.user_id, skill_id=skill.id, profile_weight=1)
        self.assertEqual(ProfileSkillset.objects.count(), 1)
        self.assertEqual(ProfileSkill.objects.count(), 1)

        skill_2 = Skill.objects.create(
            name='meta', verified=False, weight=1, skillset_id=skillset.id)
        profile_skill_2 = ProfileSkill(
            profile_id=profile.user_id, skill_id=skill_2.id, profile_weight=1)
        err_msg = 'A profile skill in that skillset with that weight already exists.'
        with self.assertRaisesMessage(ValidationError, err_msg):
            profile_skill_2.save()

        for i in range(2, 11):
            test_skill = Skill.objects.create(
                name='test {}'.format(i), verified=True,
                weight=i, skillset_id=skillset.id)
            ProfileSkill.objects.create(
                profile_id=profile.user_id,
                skill_id=test_skill.id, profile_weight=i)

        skill_11 = Skill.objects.create(
            name='test 11', verified=True, weight=11, skillset_id=skillset.id)
        profile_skill_11 = ProfileSkill(
            profile_id=profile.user_id,
            skill_id=skill_11.id, profile_weight=11)
        err_msg = 'User cannot have more than 10 skills for a one skillset'
        with self.assertRaisesMessage(ValidationError, err_msg):
            profile_skill_11.save()


class TestProfileAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        self.user_2 = User.objects.create(
            email='test2@tshape.com', password='try$h1s')

    def test_profile_get(self):
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, 200)
        profiles = Profile.objects.all()
        expected = ProfileSerializer(profiles, many=True).data
        self.assertEqual(response.data, expected)

    def test_profile_put(self):
        data = {'first_name': 'angie', 'years_experience': 5}
        response = self.client.put(
            '/api/profiles/{}/'.format(self.user_1.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(pk=self.user_1.id)
        expected = ProfileSerializer(profile).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(
            response.data['years_experience'], data['years_experience'])


class TestProfileSkillsetAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        self.user_2 = User.objects.create(
            email='test2@tshape.com', password='try$h1s')
        self.skillset_1 = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        self.skillset_2 = Skillset.objects.create(
            name='html', description='front end', verified=True, weight=10)
        self.profile_skillset_1 = ProfileSkillset.objects.create(
            profile=self.user_1.profile, skillset=self.skillset_1)
        self.profile_skillset_2 = ProfileSkillset.objects.create(
            profile=self.user_1.profile, skillset=self.skillset_2)
        self.profile_skillset_3 = ProfileSkillset.objects.create(
            profile=self.user_2.profile, skillset=self.skillset_1)

    def test_profile_skillset_get(self):
        response = self.client.get(
            '/api/profiles/{}/skillsets/'.format(self.user_1.id))
        self.assertEqual(response.status_code, 200)
        profile_skillsets = ProfileSkillset.objects.filter(
            profile=self.user_1.profile)
        expected = ProfileSkillsetSerializer(profile_skillsets, many=True).data
        self.assertEqual(response.data, expected)

    def test_profile_skillset_post(self):
        data = {'profile_id': self.user_2.id,
                'skillset_id': self.skillset_2.id}
        response = self.client.post(
            '/api/profiles/{}/skillsets/'.format(self.user_2.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        profile_skillset = ProfileSkillset.objects.filter(
            profile=self.user_2.profile, skillset=self.skillset_2).first()
        expected = ProfileSkillsetSerializer(profile_skillset).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['id'], data['skillset_id'])

    def test_profile_skillset_put(self):
        data = {'profile_weight': 8}
        response = self.client.put(
            '/api/profiles/{}/skillsets/{}/'.format(
                self.user_1.id, self.skillset_1.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        profile_skillset = ProfileSkillset.objects.filter(
            profile=self.user_1.profile, skillset=self.skillset_1).first()
        expected = ProfileSkillsetSerializer(profile_skillset).data
        self.assertEqual(response.data, expected)
        self.assertEqual(
            response.data['profile_weight'], data['profile_weight'])


class TestProfileSkillAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create(
            email='test1@tshape.com', password='try$h1s')
        self.user_2 = User.objects.create(
            email='test2@tshape.com', password='try$h1s')
        self.skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=10)
        self.skill_1 = Skill.objects.create(
            name='loops', verified=True,
            skillset_id=self.skillset.id, weight=5)
        self.skill_2 = Skill.objects.create(
            name='meta programming', verified=False,
            skillset_id=self.skillset.id)
        ProfileSkillset.objects.create(
            profile=self.user_1.profile, skillset=self.skillset)
        ProfileSkillset.objects.create(
            profile=self.user_2.profile, skillset=self.skillset)
        self.profile_skill_1 = ProfileSkill.objects.create(
            profile=self.user_1.profile, skill=self.skill_1)
        self.profile_skill_2 = ProfileSkill.objects.create(
            profile=self.user_1.profile, skill=self.skill_2, profile_weight=1)
        self.profile_skill_3 = ProfileSkill.objects.create(
            profile=self.user_2.profile, skill=self.skill_1)

    def test_profile_skill_get(self):
        response = self.client.get(
            '/api/profiles/{}/skills/'.format(self.user_1.id))
        self.assertEqual(response.status_code, 200)
        profile_skills = ProfileSkill.objects.filter(
            profile=self.user_1.profile)
        expected = ProfileSkillSerializer(profile_skills, many=True).data
        self.assertEqual(response.data, expected)

    def test_profile_skillset_skill_get(self):
        response = self.client.get(
            '/api/profiles/{}/skillsets/{}/skills/'.format(
                self.user_1.id, self.skillset.id))
        self.assertEqual(response.status_code, 200)
        profile_skills = ProfileSkill.objects.filter(
            profile=self.user_1.profile, skill__skillset_id=self.skillset.id)
        expected = ProfileSkillSerializer(profile_skills, many=True).data
        self.assertEqual(response.data, expected)

    def test_profile_skill_post(self):
        data = {'profile_id': self.user_2.id,
                'skill_id': self.skill_2.id, 'profile_weight': 2}
        response = self.client.post(
            '/api/profiles/{}/skills/'.format(self.user_2.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        profile_skill = ProfileSkill.objects.filter(
            profile=self.user_2.profile, skill=self.skill_2).first()
        expected = ProfileSkillSerializer(profile_skill).data
        self.assertEqual(response.data, expected)
        self.assertEqual(response.data['id'], data['skill_id'])
        self.assertEqual(
            response.data['profile_weight'], data['profile_weight'])

    def test_profile_skill_put(self):
        data = {'profile_weight': 8}
        response = self.client.put(
            '/api/profiles/{}/skills/{}/'.format(
                self.user_1.id, self.skill_2.id),
            json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        profile_skill = ProfileSkill.objects.filter(
            profile=self.user_1.profile, skill=self.skill_2).first()
        expected = ProfileSkillSerializer(profile_skill).data
        self.assertEqual(response.data, expected)
        self.assertEqual(
            response.data['profile_weight'], data['profile_weight'])

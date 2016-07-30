from django.test import TestCase

from profiles.models import Profile
from skills.models import Skill
from skillsets.models import Skillset
from users.models import User


class TestProfileModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test1@tshape.com', password='try$h1s')

    def test_profile_create(self):
        self.assertIsNotNone(self.user.profile)
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_update(self):
        profile = self.user.profile
        self.assertEqual(profile.first_name, '')
        self.assertEqual(profile.last_name, '')
        self.assertEqual(profile.title, '')
        self.assertEqual(profile.description, '')
        self.assertEqual(profile.years_experience, None)

        profile.first_name = 'ang'
        profile.last_name = 'ie'
        profile.title = 'CNO'
        profile.description = 'Chief Nerd Officer'
        profile.years_experience = 100
        profile.save()

        self.assertEqual(profile.first_name, 'ang')
        self.assertEqual(profile.last_name, 'ie')
        self.assertEqual(profile.title, 'CNO')
        self.assertEqual(profile.description, 'Chief Nerd Officer')
        self.assertEqual(profile.years_experience, 100)
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)

    def test_profile_skills_skillsets(self):
        profile = self.user.profile
        self.assertEqual(len(profile.skillsets.all()), 0)
        self.assertEqual(len(profile.skills.all()), 0)

        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=100)
        profile.skillsets.set([skillset])
        profile.save()
        self.assertEqual(len(profile.skillsets.all()), 1)
        self.assertEqual(profile.skillsets.first(), skillset)
        self.assertEqual(profile.skillset_ids, [skillset.id])

        skill = Skill.objects.create(
            name='generators', verified=True, skillset_id=skillset.id)
        profile.skills.set([skill])
        profile.save()
        self.assertEqual(len(profile.skills.all()), 1)
        self.assertEqual(profile.skills.first(), skill)
        self.assertEqual(profile.skill_ids, [skill.id])

    def test_profile_skills_validations(self):
        profile = self.user.profile
        skillset = Skillset.objects.create(
            name='python', description='best ever', verified=True, weight=100)
        self.assertEqual(len(Skillset.objects.all()), 1)

        skill = Skill.objects.create(
            name='generators', verified=True, skillset_id=skillset.id)
        profile.skills.set([skill])
        self.assertRaisesMessage(profile.save(),
            '{"skills": _("Corresponding skillset must be attached to profile before skill."")}')

import random

from django.core.management.base import BaseCommand
from faker import Faker

from profiles.models import Profile
from skills.models import Skill
from skillsets.models import Skillset
from users.models import User

faker = Faker()
faker.seed(10)


class Command(BaseCommand):

    help = 'Seed the database with fake data'

    def handle(self, *args, **options):
        add_skillsets()
        add_skills()
        add_users()
        add_profiles()
        add_profile_skillsets()

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database!'))


def add_skillsets():
    skillsets = [
        'JavaScript', 'Python', 'Ruby', 'Java', 'GO', 'Perl', 'C++', 'C',
        'Objective C', 'Swift', 'Algorithms', 'Data Structures',
        'Machine Learning', 'SQL', 'NOSQL', 'Big Data'
    ]
    for x in range(len(skillsets)):
        Skillset.objects.create(name=skillsets[x], description=faker.text(),
                                verified=bool(random.getrandbits(1)))


def add_skills():
    skillsets = Skillset.objects.all()
    for skillset in skillsets:
        for x in range(10):
            try:
                Skill.objects.create(skillset_id=skillset, name=faker.company(),
                                     description=faker.text(),
                                     verified=True)
            except:
                pass
        for x in range(10):
            try:
                Skill.objects.create(skillset_id=skillset, name=faker.company(),
                                     description=faker.text(),
                                     verified=False)
            except:
                pass


def add_users():
    for x in range(20):
        email = faker.email()
        try:
            User.objects.create(email=email, password=faker.password())
        except Exception as e:
            print(e)


def add_profiles():
    users = User.objects.all()
    for user in users:
        profile = user.profile
        profile.title = faker.job()
        profile.description = faker.text()
        profile.years_experience = random.randrange(1, 10)
        profile.save()


def add_profile_skillsets():
    profiles = Profile.objects.all()
    skillsets = Skillset.objects.all()
    for profile in profiles:
        profile_skillsets = random.sample(set(skillsets), 8)
        for profile_skillset in profile_skillsets:
            profile_skills = random.sample(set(profile_skillset.skills.all()), 10)
            profile.skills.add(*profile_skills)
            profile.save()

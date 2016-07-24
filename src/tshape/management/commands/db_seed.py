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
    try:
        Skillset.objects.bulk_create([
            Skillset(name=skillsets[i], description=faker.text(),
                     verified=bool(random.getrandbits(1)))
            for i in range(len(skillsets))
            ])
    except:
        print('error creating skillsets')


def add_skills():
    skillsets = Skillset.objects.all()
    slice_index = int(len(skillsets) / 2)
    skills = []
    try:
        for skillset in skillsets[:slice_index]:
            skills.extend([
                Skill(skillset=skillset, name=faker.company(),
                      description=faker.text(), verified=True)
                for i in range(10)
                ])
    except Exception as e:
        print('error creating verified skills!')
        print(e)
    try:
        for skillset in skillsets[slice_index:]:
            skills.extend([
                Skill(skillset=skillset, name=faker.company(),
                      description=faker.text(), verified=False)
                for i in range(10)
                ])
    except Exception as e:
        print('error creating unverified skills!')
        print(e)
    try:
        Skill.objects.bulk_create(skills)
    except Exception as e:
        print('error with skills bulk create')
        print(e)


def add_users():
        email = faker.email()
        try:
            User.objects.create(email=email, password=faker.password())
        except Exception as e:
            print(e)


def add_profiles():
    # figure out how to do a bulk update here
    users = User.objects.all()
    for user in users:
        profile = user.profile
        profile.title = faker.job()
        profile.description = faker.text()
        profile.years_experience = random.randrange(1, 10)
        profile.save()


def add_profile_skillsets():
    # figure out how to do a bulk update here
    profiles = Profile.objects.all()
    skillsets = Skillset.objects.all()
    for profile in profiles:
        profile_skillsets = random.sample(set(skillsets), 8)
        profile.skillsets.set(profile_skillsets)
        skills = []
        for skillset in profile_skillsets:
            skills.extend(random.sample(set(skillset.skills.all()), 10))
        profile.skills.set(skills)

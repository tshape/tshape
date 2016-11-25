import os

from django.core.management.base import BaseCommand

from skills.models import Skill
from skillsets.models import Skillset
from tshape.management import commands


class Command(BaseCommand):

    help = "Dump a set of skills for a skillset in the database"

    def add_arguments(self, parser):
        parser.add_argument("--skillset", nargs="*", type=str)

    def handle(self, *args, **options):
        skillnames = options.get("skillset")
        for skillname in skillnames:
            add_data(skillname)

        self.stdout.write(
            self.style.SUCCESS('Successfully dumped data into the database!'))


def add_data(skillname):
    skill = skillname.upper()
    skill_dict = getattr(commands, "{}_SKILLS".format(skill))

    dump_skill_dict(skillname, skill_dict)


def dump_skill_dict(skillname, skill_dict):
    for ss, ss_skills in skill_dict.items():
        new_skills = []
        skillset = Skillset.objects.filter(name=skillname).first()
        Skill.objects.filter(skillset_id=skillset.id).delete()
        for skills, skill_attrs in ss_skills.items():
            for attrs in skill_attrs:
                new_skills.append(
                    Skill(skillset_id=skillset.id, verified=True, **attrs))
        Skill.objects.bulk_create(new_skills)

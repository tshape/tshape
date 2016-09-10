from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from skills.models import Skill
from skillsets.models import Skillset
from tshape.models import BaseModel


class Profile(BaseModel):

    class Meta:
        db_table = 'profiles'
        ordering = ('last_name',)
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=50)
    title = models.CharField(_('title'), max_length=280, blank=True)
    description = models.TextField(_('description'), blank=True)
    years_experience = models.IntegerField(
        _('years of experience'), blank=True, null=True)
    skills = models.ManyToManyField(
        Skill, verbose_name=_('skills'), through='ProfileSkill')
    skillsets = models.ManyToManyField(
        Skillset, verbose_name=_('skillsets'), through='ProfileSkillset')

    @property
    def skillset_ids(self):
        return [skillset.id for skillset in self.skillsets.all()]

    @property
    def skill_ids(self):
        return [skill.id for skill in self.skills.all()]

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class ProfileSkill(BaseModel):

    class Meta:
        db_table = 'profile_skills'
        verbose_name = _('profile skill')
        verbose_name_plural = _('profile skills')
        unique_together = ('profile', 'skill',)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=False)
    profile_weight = models.IntegerField(null=False)

    def clean(self):
        if not self.id:
            existing = ProfileSkill.objects.filter(
                profile=self.profile,
                skill__skillset_id=self.skill.skillset_id,
                profile_weight=self.profile_weight)
            if existing:
                raise ValidationError(
                    {'profile_skills': _(
                        'A profile skill in that skillset with that weight already exists.')})

            profile_skillset = ProfileSkillset.objects.filter(
                profile_id=self.profile.user_id,
                skillset_id=self.skill.skillset_id)
            if not profile_skillset:
                raise ValidationError(
                    {'skills': _(
                        'Corresponding skillset must be attached to profile before skill.')})

            profile_skills = ProfileSkill.objects.filter(
                profile_id=self.profile.user_id)
            num_skills = sum(
                1 for profile_skill in profile_skills
                if profile_skill.skill.skillset_id == self.skill.skillset_id)
            if num_skills >= 10:
                raise ValidationError({'skills': _(
                    'User cannot have more than 10 skills for a one skillset.'
                    )})

    def save(self, *args, **kwargs):
        skill = Skill.objects.get(pk=self.skill_id)
        if skill.verified:
            self.profile_weight = skill.weight
        self.full_clean()
        super(ProfileSkill, self).save(*args, **kwargs)


class ProfileSkillset(BaseModel):

    class Meta:
        db_table = 'profile_skillsets'
        verbose_name = _('profile skillset')
        verbose_name_plural = _('profile skillsets')
        unique_together = (('profile', 'skillset',),
                           ('profile', 'profile_weight',))

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False)
    skillset = models.ForeignKey(
        Skillset, on_delete=models.CASCADE, null=False)
    profile_weight = models.IntegerField(null=True, blank=True)

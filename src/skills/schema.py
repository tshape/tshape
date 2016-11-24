from django_filters import FilterSet
from graphene_django import DjangoObjectType
import graphene

from profiles.models import Profile as ProfileModel
from skills.models import Skill as SkillModel
from skillsets.models import Skillset as SkillsetModel
from tshape.utils import assign_attrs
from users.models import User as UserModel

__all__ = ['Skill', 'SkillFilter', 'SkillQuery',
           'CreateSkill', 'UpdateSkill', 'DeleteSkill']


class Skill(DjangoObjectType):

    class Meta:
        model = SkillModel
        filter_fields = ['id', 'name', 'description',
                         'verified', 'weight', 'skillset_id']
        filter_order_by = ['id', 'name', 'description',
                           'verified', 'weight', 'skillset_id']


class SkillFilter(FilterSet):

    class Meta:
        model = SkillModel
        fields = ['id', 'name', 'description',
                  'verified', 'weight', 'skillset_id']


class SkillQuery(graphene.AbstractType):
    skill = graphene.Field(Skill)
    skills = graphene.List(Skill)

    @graphene.resolve_only_args
    def resolve_skill(self):
        return SkillModel.objects.first()

    @graphene.resolve_only_args
    def resolve_skills(self):
        return SkillModel.objects.all()


# def create_skill(name, description, skillset_id):
#     new_skill = Skill(
#         name=name,
#         description=description,
#         skillset_id=skillset_id
#     )
#     new_skill.save()
#     return new_skill


class CreateSkill(graphene.Mutation):

    class Input:
        name = graphene.String(required=True)
        description = graphene.String()
        verified = graphene.Boolean()
        weight = graphene.Int()
        skillset_id = graphene.Int(required=True)

    skill = graphene.Field(Skill)

    def mutate(self, args, context, info):
        name = args.get('name')
        description = args.get('description')
        skillset_id = args.get('skillset_id')
        new_skill = SkillModel(name, description, skillset_id)
        new_skill.save()
        return CreateSkill(skill=new_skill)


class UpdateSkill(graphene.Mutation):

    class Input:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        verified = graphene.Boolean()
        weight = graphene.Int()
        skillset_id = graphene.Int()

    skill = graphene.Field(Skill)

    def mutate(self, args, context, info):
        id = args.get('id')
        skill = SkillModel.objects.get(pk=id)
        keys = ['name', 'description', 'verified', 'weight', 'skillset_id']
        attr_map = {
            k: v for k, v in args.items()
            if k in keys and v is not None}
        skill = assign_attrs(attr_map, skill)
        skill.save()
        return UpdateSkill(skill=skill)


class DeleteSkill(graphene.Mutation):

    class Input:
        id = graphene.Int(required=True)

    skill = graphene.Field(Skill)

    def mutate(self, args, context, info):
        id = args.get('id')
        skill = SkillModel.objects.get(pk=id)
        skill.delete()
        return DeleteSkill(skill=skill)

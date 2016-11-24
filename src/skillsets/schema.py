from django_filters import FilterSet
from graphene_django import DjangoObjectType
import graphene

from profiles.models import Profile as ProfileModel
from skills.models import Skill as SkillModel
from skillsets.models import Skillset as SkillsetModel
from tshape.utils import assign_attrs
from users.models import User as UserModel

__all__ = ['Skillset', 'SkillsetFilter', 'SkillsetQuery',
           'CreateSkillset', 'UpdateSkillset', 'DeleteSkillset']


class Skillset(DjangoObjectType):

    class Meta:
        model = SkillsetModel
        filter_fields = ['id', 'name', 'description', 'verified', 'weight']
        filter_order_by = ['id', 'name', 'description', 'verified', 'weight']


class SkillsetFilter(FilterSet):

    class Meta:
        model = SkillsetModel
        fields = ['id', 'name', 'description', 'verified', 'weight']


class SkillsetQuery(graphene.AbstractType):
    skillset = graphene.Field(Skillset)
    skillsets = graphene.List(Skillset)

    @graphene.resolve_only_args
    def resolve_skillset(self):
        return SkillsetModel.objects.first()

    @graphene.resolve_only_args
    def resolve_skillsets(self):
        return SkillsetModel.objects.all()


class CreateSkillset(graphene.Mutation):

    class Input:
        name = graphene.String(required=True)
        description = graphene.String()
        verified = graphene.Boolean()
        weight = graphene.Int()

    skillset = graphene.Field(Skillset)

    def mutate(self, args, context, info):
        name = args.get('name')
        description = args.get('description')
        verified = args.get('verified')
        weight = args.get('weight')
        skillset = SkillsetModel(
            name=name, description=description,
            weight=weight, verified=verified)
        skillset.save()
        return CreateSkillset(skillset=skillset)


class UpdateSkillset(graphene.Mutation):

    class Input:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        verified = graphene.Boolean()
        weight = graphene.Int()

    skillset = graphene.Field(Skillset)

    def mutate(self, args, context, info):
        id = args.get('id')
        skillset = SkillsetModel.objects.get(pk=id)
        keys = ['name', 'description', 'verified', 'weight']
        attr_map = {
            k: v for k, v in args.items()
            if k in keys and v is not None}
        skillset = assign_attrs(attr_map, skillset)
        # TODO: add validation for user id
        skillset.save()
        return UpdateSkillset(skillset=skillset)


class DeleteSkillset(graphene.Mutation):

    class Input:
        id = graphene.Int(required=True)

    skillset = graphene.Field(Skillset)

    def mutate(self, args, context, info):
        id = args.get('id')
        skillset = SkillsetModel.objects.get(pk=id)
        skillset.delete()
        return DeleteSkillset(skillset=skillset)

from django_filters import FilterSet
from graphene_django import DjangoObjectType
import graphene

from profiles.models import Profile as ProfileModel
from skills.models import Skill as SkillModel
from skillsets.models import Skillset as SkillsetModel
from tshape.utils import assign_attrs
from users.models import User as UserModel

__all__ = ['Profile', 'ProfileFilter', 'ProfileQuery',
           'UpdateProfile', 'DeleteProfile']


class Profile(DjangoObjectType):

    class Meta:
        model = ProfileModel
        filter_fields = [
            'user_id', 'first_name', 'last_name',
            'title', 'description', 'years_experience']
        filter_order_by = [
            'user_id', 'first_name', 'last_name',
            'title', 'description', 'years_experience']

    user_id = graphene.Int()


class ProfileFilter(FilterSet):

    class Meta:
        model = ProfileModel
        fields = ['user_id', 'first_name', 'last_name',
                  'title', 'description', 'years_experience']


class ProfileQuery(graphene.AbstractType):
    profile = graphene.Field(Profile)
    profiles = graphene.List(Profile)

    @graphene.resolve_only_args
    def resolve_profile(self):
        return ProfileModel.objects.first()

    @graphene.resolve_only_args
    def resolve_profiles(self):
        return ProfileModel.objects.all()


class UpdateProfile(graphene.Mutation):

    class Input:
        user_id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    profile = graphene.Field(Profile)

    def mutate(self, args, context, info):
        user_id = args.get('user_id')
        profile = ProfileModel.objects.get(pk=user_id)
        keys = ['first_name', 'last_name', 'title',
                'description', 'years_experience']
        attr_map = {
            k: v for k, v in args.items()
            if k in keys and v is not None}
        profile = assign_attrs(attr_map, profile)
        profile.save()
        return UpdateProfile(profile=profile)


class DeleteProfile(graphene.Mutation):

    class Input:
        user_id = graphene.Int(required=True)

    profile = graphene.Field(Profile)

    def mutate(self, args, context, info):
        user_id = args.get('user_id')
        profile = ProfileModel.objects.get(pk=user_id)
        profile.delete()
        return DeleteProfile(profile=profile)

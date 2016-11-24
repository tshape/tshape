from django_filters import FilterSet
from graphene_django import DjangoObjectType
import graphene

from profiles.models import Profile as ProfileModel
from tshape.utils import assign_attrs
from users.models import User as UserModel

__all__ = ['User', 'UserFilter', 'UserQuery']


class User(DjangoObjectType):

    class Meta:
        model = UserModel
        filter_fields = [
            'id', 'email', 'is_active', 'is_staff',
            'date_joined', 'first_name', 'last_name']
        filter_order_by = [
            'id', 'email', 'date_joined', 'first_name',
            'last_name']


class UserFilter(FilterSet):

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'is_active', 'is_staff',
                  'date_joined', 'first_name', 'last_name']


class UserQuery(graphene.AbstractType):
    user = graphene.Field(User)
    users = graphene.List(User)

    @graphene.resolve_only_args
    def resolve_user(self):
        return UserModel.objects.first()

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()


class CreateUser(graphene.Mutation):

    class Input:
        email = graphene.String(required=True)

    user = graphene.Field(User)

    def mutate(self, args, context, info):
        user = UserModel(args.get('email'))
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):

    class Input:
        id = graphene.Int(required=True)
        email = graphene.String(required=True)
        is_active = graphene.Boolean()

    user = graphene.Field(User)

    def mutate(self, args, context, info):
        id = args.get('id')
        user = UserModel.objects.get(pk=id)
        if not user:
            print("raise exception here")
            print("or return 404?")
        keys = ['email', 'is_active']
        attr_map = {
            k: v for k, v in args.items()
            if k in keys and v is not None}
        user = assign_attrs(attr_map, user)
        # id = input.get('id', None)
        # email = input.get('email', None)
        # first_name = input.get('first_name', None)
        # last_name = input.get('last_name', None)
        # is_active = input.get('is_active', None)
        # TODO: add validation for user id
        # if email is not None:
        #     user.email = email
        # if first_name is not None:
        #     user.first_name = first_name
        # if last_name is not None:
        #     user.last_name = last_name
        # if is_active is not None:
        #     user.is_active = is_active
        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):

    class Input:
        id = graphene.Int(required=True)

    user = graphene.Field(User)

    def mutate(self, args, context, info):
        id = args.get('id')
        user = UserModel.objects.get(pk=id)
        user.delete()
        return DeleteUser(user=user)

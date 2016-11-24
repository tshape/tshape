import graphene

from profiles.schema import ProfileQuery, UpdateProfile, DeleteProfile
from skills.schema import SkillQuery, CreateSkill, UpdateSkill, DeleteSkill
from skillsets.schema import (
    SkillsetQuery, CreateSkillset, UpdateSkillset, DeleteSkillset
)
from users.schema import UserQuery, CreateUser, UpdateUser, DeleteUser


class Query(graphene.ObjectType, ProfileQuery, SkillQuery,
            SkillsetQuery, UserQuery):
    pass


class Mutation(graphene.ObjectType):

    update_profile = UpdateProfile.Field()
    delete_profile = DeleteProfile.Field()
    create_skill = CreateSkill.Field()
    update_skill = UpdateSkill.Field()
    delete_skill = DeleteSkill.Field()
    create_skillset = CreateSkillset.Field()
    update_skillset = UpdateSkillset.Field()
    delete_skillset = DeleteSkillset.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

from at_queue.core.at_component import ATComponent
from at_queue.utils.decorators import authorized_method
from at_queue.utils.decorators import component_method
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from at_user_ng.apps.accounts.serializers import MeSerializer
from at_user_ng.core.models import UserData

User = get_user_model()


class ATUser(ATComponent):

    @component_method
    async def verify_token(self, token: str) -> int:
        try:
            token = await Token.objects.aget(key=token)
            return token.user_id
        except Token.DoesNotExist:
            raise ValueError("Invalid token")

    @authorized_method
    async def me(self, auth_token: str) -> UserData:
        try:
            token = await Token.objects.select_related('user').aget(key=auth_token)
            instance = token.user
            serializer = MeSerializer(instance)
            data = await serializer.adata
            return UserData(**data)
        except Token.DoesNotExist:
            raise ValueError("Invalid token")

from adrf import viewsets
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from at_user_ng.apps.accounts.serializers import MeSerializer
from at_user_ng.apps.accounts.serializers import SignInSerializer

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet):

    @action(
        detail=False,
        methods=['post'],
        serializer_class=SignInSerializer,
        permission_classes=[permissions.AllowAny]
    )
    async def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        data = await serializer.adata
        return Response(data=data)

    @action(
        detail=False,
        methods=['get'],
        serializer_class=MeSerializer,
        permission_classes=[permissions.IsAuthenticated]
    )
    async def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        data = await serializer.adata
        return Response(data=data)

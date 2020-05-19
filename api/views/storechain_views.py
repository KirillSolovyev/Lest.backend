from rest_framework.viewsets import ModelViewSet
from .. import serializers
from ..models import StoreChain
from ..common import permissions


class StoreChainListView(ModelViewSet):
    serializer_class = serializers.StoreChainSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        return StoreChain.objects.all()[offset:amount + offset]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (permissions.IsAdmin,)
        return super(self.__class__, self).get_permissions()


class StoreChainView(ModelViewSet):
    serializer_class = serializers.StoreChainSerializer
    queryset = StoreChain.objects.all()

    def get_permissions(self):
        if self.action in ("update", "destroy"):
            self.permission_classes = (permissions.IsAdmin,)
        return super(self.__class__, self).get_permissions()

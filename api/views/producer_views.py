from rest_framework.viewsets import ModelViewSet
from api import serializers
from ..models import Producer
from ..common import permissions


class ProducerListView(ModelViewSet):
    serializer_class = serializers.ProducerSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        return Producer.objects.all()[offset:amount + offset]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (permissions.IsAdmin,)
        return super(self.__class__, self).get_permissions()


class ProducerView(ModelViewSet):
    serializer_class = serializers.ProducerSerializer
    queryset = Producer.objects.all()

    def get_permissions(self):
        if self.action in ("partial_update", "destroy"):
            self.permission_classes = (permissions.IsAdmin,)
        return super(self.__class__, self).get_permissions()

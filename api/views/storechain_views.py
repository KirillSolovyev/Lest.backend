from rest_framework.viewsets import ModelViewSet
from api import serializers
from api.models import StoreChain


class StoreChainListView(ModelViewSet):
    serializer_class = serializers.StoreChainSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        return StoreChain.objects.all()[offset:amount + offset]


class StoreChainView(ModelViewSet):
    serializer_class = serializers.StoreChainSerializer
    queryset = StoreChain.objects.all()

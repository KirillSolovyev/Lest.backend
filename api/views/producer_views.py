from rest_framework.viewsets import ModelViewSet
from api import serializers
from api.models import Producer


class ProducerListView(ModelViewSet):
    serializer_class = serializers.ProducerSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        return Producer.objects.all()[offset:amount + offset]


class ProducerView(ModelViewSet):
    serializer_class = serializers.ProducerSerializer
    queryset = Producer.objects.all()


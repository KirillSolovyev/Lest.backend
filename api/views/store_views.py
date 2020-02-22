from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from api import serializers
from api.models import Store, StoreChain


class StoreListView(ModelViewSet):
    serializer_class = serializers.StoreSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        store_chain_id = self.request.data.get("store_chain_id", None)
        if store_chain_id:
            return Store.objects.filter(producer__id=store_chain_id)[offset:amount + offset]
        else:
            return Store.objects.all()[offset:amount + offset]

    def perform_create(self, serializer):
        store_chain = get_object_or_404(StoreChain, pk=self.request.data.get("store_chain_id"))
        return serializer.save(store_chain=store_chain)


class StoreView(ModelViewSet):
    serializer_class = serializers.StoreSerializer
    queryset = Store.objects.all()

    def perform_update(self, serializer):
        store_chain_id = self.request.data.get("store_chain_id", None)
        if store_chain_id:
            store_chain = get_object_or_404(StoreChain, pk=store_chain_id)
            return serializer.save(store_chain = store_chain)
        else:
            return serializer.save()

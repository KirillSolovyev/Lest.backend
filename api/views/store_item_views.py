from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from api import serializers
from api.models import StoreItem, Product, Store


class StoreItemListView(ModelViewSet):
    serializer_class = serializers.StoreItemSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        store_id = self.request.data.get("store_id", None)
        product_id = self.request.data.get("product_id", None)
        barcode = self.request.data.get("barcode", None)
        to_filter = {}
        if store_id:
            to_filter["store__id"] = store_id
        if product_id:
            to_filter["product__id"] = product_id
        if barcode:
            to_filter["product__barcode"] = barcode
        return StoreItem.objects.filter(**to_filter)[offset:amount + offset]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get("product_id"))
        store = get_object_or_404(Store, pk=self.request.data.get("store_id"))
        return serializer.save(product=product, store=store)


class StoreItemView(ModelViewSet):
    serializer_class = serializers.StoreItemSerializer
    queryset = StoreItem.objects.all()

    def perform_update(self, serializer):
        product_id = self.request.data.get("product_id", None)
        store_id = self.request.data.get("store_id", None)
        if product_id and store_id:
            product = get_object_or_404(Product, pk=product_id)
            store = get_object_or_404(Store, pk=store_id)
            return serializer.save(product=product, store=store)
        elif store_id:
            store = get_object_or_404(Store, pk=store_id)
            return serializer.save(store=store)
        elif product_id:
            product = get_object_or_404(Product, pk=product_id)
            return serializer.save(product=product)
        else:
            return serializer.save()

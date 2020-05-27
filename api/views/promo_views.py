from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from ..common import permissions
from ..models import Promo
from ..serializers import PromoSerializer, StoreChain
from ..common.errors import ErrorCode


class PromoListView(ModelViewSet):
    serializer_class = PromoSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        store_chain_id = self.request.data.get("store_chain_id", False)
        search_str = self.request.data.get("search_str", False)
        to_filter = {}
        if search_str:
            to_filter["text__icontains"] = search_str
        if store_chain_id:
            to_filter["store_chain__id"] = store_chain_id
        return Promo.objects.filter(**to_filter)[offset:offset+amount]

    def perform_create(self, serializer):
        store_chain_id = self.request.data.get("store_chain_id")
        store_chain = get_object_or_404(StoreChain, pk=store_chain_id)
        return serializer.save(store_chain=store_chain)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (permissions.IsAdmin, permissions.IsStoreChain)
        return super(self.__class__, self).get_permissions()


class PromoView(ModelViewSet):
    serializer_class = PromoSerializer
    queryset = Promo.objects.all()

    def get_permissions(self):
        if self.action in ("partial_update", "destroy"):
            self.permission_classes = (permissions.IsAdmin, permissions.IsStoreChain)
        return super(self.__class__, self).get_permissions()

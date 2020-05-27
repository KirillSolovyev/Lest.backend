from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from ..common import permissions
from ..models import Discount, StoreItem
from ..serializers import DiscountSerializer
from ..common.errors import ErrorCode


class DiscountListView(ModelViewSet):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        store_chain_id = self.request.data.get("store_chain_id", False)
        to_filter = {}
        if store_chain_id:
            to_filter["store_item__store_chain__pk"] = store_chain_id

        return Discount.objects.filter(**to_filter)[offset:offset+amount]

    def create(self, request):
        store_item_id = request.data.get("store_item_id", False)
        new_price = request.data.get("new_price", False)
        if not store_item_id or not new_price:
            return Response({"error": ErrorCode.INCOMPLETE_DATA.value}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(new_price, float) and not isinstance(new_price, int):
            return Response({"error": ErrorCode.INVALID_DATA.value}, status=status.HTTP_400_BAD_REQUEST)

        store_item = StoreItem.objects.filter(pk=store_item_id)
        if not store_item.exists():
            return Response({"error": ErrorCode.NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)

        store_item = store_item.first()
        discount = Discount.objects.create(store_item=store_item, old_price=store_item.price)
        store_item.price = new_price
        store_item.save()
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (permissions.IsAdmin, permissions.IsStoreChain)
        return super(self.__class__, self).get_permissions()


class DiscountView(ModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()

    # def get_permissions(self):
    #     if self.action in ("partial_update", "destroy"):
    #         self.permission_classes = (permissions.IsAdmin, permissions.IsStoreChain)
    #     return super(self.__class__, self).get_permissions()
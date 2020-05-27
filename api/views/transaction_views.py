from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from api import serializers
from ..common.errors import ErrorCode

from ..models import StoreItem, Store, Transaction, TransactionItem
from django.contrib.auth import get_user_model


class ProceedTransactionView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        if user is None:
            return Response({"error": ErrorCode.NOT_LOGGED_IN.value}, status=status.HTTP_404_NOT_FOUND)
        vendor = Store.objects.filter(pk=request.data.get("store_id"))
        if not vendor:
            return Response({"error": ErrorCode.STORE_NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)
        vendor = vendor.first()
        store_items = request.data.get("store_items", False)
        if not isinstance(store_items, list) or not len(store_items) > 0:
            return Response({"error": ErrorCode.INVALID_DATA.value}, status=status.HTTP_400_BAD_REQUEST)
        transaction = {"vendor_name": vendor.name, "transaction_amount": 0}
        trans_items = []
        for item in store_items:
            store_item = StoreItem.objects.filter(pk=item["store_item_id"])
            if not store_item:
                return Response({"error": ErrorCode.STORE_ITEM_NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)
            store_item = store_item.first()
            transaction["transaction_amount"] += store_item.price * item["amount"]
            trans_items.append({
                "store_item": store_item,
                "store_item_name": store_item.product.name,
                "price": store_item.price,
                "amount": item["amount"]
            })

        #TODO: Perform transaction and handle the response

        return self.transaction_success(transaction, trans_items, user, vendor)

    def transaction_success(self, transaction, trans_items, user, vendor):
        trans_ser = serializers.TransactionSerializer(data=transaction)
        if trans_ser.is_valid():
            saved_transaction = trans_ser.save(user=user, vendor=vendor)
            for item in trans_items:
                store_item = item["store_item"]
                item_serializer = serializers.TransactionItemSerializer(data=item)
                if item_serializer.is_valid():
                    item_serializer.save(transaction=saved_transaction, store_item=store_item)
            return Response(trans_ser.data)
        else:
            return Response(trans_ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def transaction_fail(self):
        pass


class TransactionListView(ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        to_filter = {
            "user": self.request.user
        }
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        from_date = self.request.data.get("from_date")
        to_date = self.request.data.get("to_date")
        if to_date is not None:
            to_filter["date__lte"] = datetime.strptime(to_date, "%d.%m.%Y")
        elif from_date is not None:
            to_filter["date__gte"] = datetime.strptime(from_date, "%d.%m.%Y")
        return Transaction.objects.filter(**to_filter)[offset:offset+amount]


class TransactionView(ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TransactionSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            transaction = Transaction.objects.get(pk=pk)
            serializer = serializers.TransactionSerializer(transaction)
            return Response(serializer.data)
        except:
            return Response({"error": ErrorCode.NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)


class TransactionItemListView(ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TransactionItemSerializer

    def list(self, request, *args, **kwargs):
        transaction_id = request.data.get("transaction_id", False)
        if transaction_id:
            transaction_items = TransactionItem.objects.filter(transaction__id=transaction_id)
            serializer = serializers.TransactionItemSerializer(transaction_items, many=True)
            return Response(serializer.data)
        return Response({"error": ErrorCode.INVALID_DATA.value}, status=status.HTTP_400_BAD_REQUEST)

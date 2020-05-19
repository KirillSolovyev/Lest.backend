import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Transaction, TransactionItem, User, Store, StoreItem, StoreChain, Product, Producer, ProductCategory
from ..serializers import TransactionSerializer, TransactionItemSerializer
from ..common.errors import ErrorCode


class TransactionParentTest(APITestCase):
    store = None
    store_item = None

    def setUp(self):
        user = User.objects.create_user("+12345678910", "test_password")
        self.client.force_authenticate(user=user)
        store_chain = StoreChain.objects.create(name="Test Store")
        self.store = Store.objects.create(address="Zhibek Zholy", store_chain=store_chain, long=1.0, lat=1.0)
        producer = Producer.objects.create(name="Test Producer")
        product_category = ProductCategory.objects.create(name="Test")
        product = Product.objects.create(producer=producer, name="Test Product", composition="Test", barcode=123456789, category=product_category)
        self.store_item = StoreItem.objects.create(product=product, store=self.store, price=100)

    def proceed_transaction(self, store_id, store_item_id):
        body = {
            "store_id": store_id,
            "store_items": [
                {
                    "store_item_id": store_item_id,
                    "amount": 2
                },
            ]
        }
        url = reverse("proceed_transaction")
        return self.client.put(url, json.dumps(body), content_type="application/json")


class TransactionTest(TransactionParentTest):
    def test_proceed_transaction(self):
        response = self.proceed_transaction(self.store.pk, self.store_item.pk)
        transaction = Transaction.objects.get(vendor=self.store)
        serializer = TransactionSerializer(transaction)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_store_proceed_transaction(self):
        response = self.proceed_transaction(1000, self.store_item.pk)
        self.assertEqual(response.data["error"], ErrorCode.STORE_NOT_FOUND.value)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_found_store_item_proceed_transaction(self):
        response = self.proceed_transaction(self.store.pk, 100)
        self.assertEqual(response.data["error"], ErrorCode.STORE_ITEM_NOT_FOUND.value)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_store_items_empty_array_proceed_transaction(self):
        body = {
            "store_id": self.store.pk,
            "store_items": []
        }
        url = reverse("proceed_transaction")
        response = self.client.put(url, json.dumps(body), content_type="application/json")
        self.assertEqual(response.data["error"], ErrorCode.INVALID_DATA.value)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_transaction_list(self):
        for i in range(0, 5):
            self.proceed_transaction(self.store.pk, self.store_item.pk)
        url = reverse("user_transactions")
        response = self.client.post(url)
        serializer = TransactionSerializer(Transaction.objects.all()[0:10], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_offset_amount_transaction_list(self):
        for i in range(0, 20):
            self.proceed_transaction(self.store.pk, self.store_item.pk)
        url = reverse("user_transactions")
        body = {"amount": 7, "offset": 5}
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        serializer = TransactionSerializer(Transaction.objects.all()[5:12], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction(self):
        transaction = self.proceed_transaction(self.store.pk, self.store_item.pk).data
        url = reverse("get_transaction", kwargs={"pk": transaction["id"]})
        response = self.client.get(url)
        self.assertEqual(response.data, transaction)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TransactionItemTest(TransactionParentTest):
    def test_get_transaction_items(self):
        url = reverse("user_transaction_items")
        transaction = self.proceed_transaction(self.store.pk, self.store_item.pk).data
        body = {"transaction_id": transaction["id"]}
        response = self.client.post(url, json.dumps(body), content_type="application/json")
        transaction_items = TransactionItem.objects.filter(transaction__id=transaction["id"])
        serializer = TransactionItemSerializer(transaction_items, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

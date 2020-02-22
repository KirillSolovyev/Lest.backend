import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from ...models import Producer, Product, Store, StoreChain, StoreItem
from ..serializers import ProductSerializer, ProducerSerializer, StoreChainSerializer

client = Client()


class ProducerApiTest(TestCase):
    def setUp(self):
        self.url = reverse("producer_list")
        self.url_single = reverse("producer", kwargs={"pk": 1})
        for i in range(5):
            Producer.objects.create(name="Producer{}".format(i))

    def test_post_producers(self):
        body = {"amount": 2, "offset": 2}
        response = self.client.post(self.url, json.dumps(body), format="json", content_type="application/json")
        producers = Producer.objects.all()[2:4]
        serializer = ProducerSerializer(producers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_producers(self):
        body = {"name": "#Test"}
        response = self.client.put(self.url, json.dumps(body), format="json", content_type="application/json")
        producer = get_object_or_404(Producer, name="#Test")
        serializer = ProducerSerializer(producer)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data_creation_producers(self):
        body = {}
        response = self.client.put(self.url, json.dumps(body), format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_producer(self):
        response = self.client.get(self.url_single)
        producer = get_object_or_404(Producer, pk=1)
        serializer = ProducerSerializer(producer)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_producer(self):
        response = self.client.delete(self.url_single)
        producer = self.client.get(self.url_single)
        self.assertEqual(producer.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_producer(self):
        body = {"name": "CHANGED"}
        response = self.client.put(self.url_single, json.dumps(body), format="json", content_type="application/json")
        producer = get_object_or_404(Producer, pk=1)
        serializer = ProducerSerializer(producer)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_data_update_producer(self):
        body = {"name": ""}
        response = self.client.put(self.url_single, json.dumps(body), format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_field_update_producer(self):
        body = {"#field": "no effect"}
        producer = get_object_or_404(Producer, pk=1)
        serializer = ProducerSerializer(producer)
        response = self.client.put(self.url_single, json.dumps(body), format="json", content_type="application/json")
        self.assertEqual(response.data, serializer.data)


class ProductApiTest(TestCase):
    def setUp(self):
        self.url_list = reverse("product_list")
        self.url = reverse("product", kwargs={"pk": 1})
        self.producer = Producer.objects.create(name="Producer")
        for i in range(5):
            Product.objects.create(
                name="Product{}".format(i),
                composition="Desc{}".format(i),
                producer=self.producer,
                barcode="{}".format(i)
            )

    def test_get_products(self):
        body = {"amount": 2, "offset": 2, "producer_id": self.producer.pk}
        response = self.client.post(self.url_list, json.dumps(body), format="json", content_type="application/json")
        products = Product.objects.all()[2:4]
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)

    # def test_create_product(self):
    #     body = {"name": "CHANGED", "composition": "Hellllo", "producer_id": self.producer.pk}
    #     response = self.client.put(self.url_list, json.dumps(body), format="json", content_type="application/json")
    #     product = get_object_or_404(Product, name="CHANGED")
    #     serializer = ProductSerializer(product)
    #     self.assertEqual(response.data, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data_create_product(self):
        body = {}
        response = self.client.put(self.url_list, json.dumps(body), format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_product(self):
    #     new_producer = Producer.objects.create(name="#New prod")
    #     body = {"name": "Changed", "producer_id": new_producer.pk}
    #     response = self.client.put(self.url, json.dumps(body), format="json", content_type="application/json")
    #     product = get_object_or_404(Product, pk=1)
    #     serializer = ProductSerializer(product)
    #     self.assertEqual(response.data["name"], serializer.data["name"])
    #     self.assertEqual(response.data["producer_id"], serializer.data["producer_id"])

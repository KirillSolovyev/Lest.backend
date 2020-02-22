import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Product, Producer, StoreChain, StoreItem, Store


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ["id", "name"]


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)


class ProductSerializer(serializers.ModelSerializer):
    producer = serializers.CharField(read_only=True, source="producer.name")
    producer_id = serializers.IntegerField(read_only=True, source="producer.id")
    image = Base64ImageField()

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Length of name must be at least 3")
        return value

    class Meta:
        model = Product
        fields = ["id", "barcode", "name", "composition", "image", "producer", "producer_id"]


class StoreChainSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Length of name must be at least 3")
        return value

    class Meta:
        model = StoreChain
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    store_chain = serializers.CharField(read_only=True, source="store_chain.name")
    store_chain_id = serializers.IntegerField(read_only=True, source="store_chain.id")

    class Meta:
        model = Store
        fields = ["id", "address", "name", "long", "lat", "store_chain", "store_chain_id"]


class StoreItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True, source="product.name")
    product_id = serializers.IntegerField(read_only=True, source="product.id")
    store = serializers.CharField(read_only=True, source="store.name")
    store_id = serializers.IntegerField(read_only=True, source="store.id")

    class Meta:
        model = StoreItem
        fields = ["id", "amount", "price", "product", "product_id", "store", "store_id"]

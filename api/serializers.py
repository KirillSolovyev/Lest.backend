import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Product, Producer, StoreChain, StoreItem, Store, \
                    Transaction, TransactionItem, User, ProductCategory, \
                    Promo, Discount


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


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    producer = serializers.CharField(read_only=True, source="producer.name")
    producer_id = serializers.IntegerField(read_only=True, source="producer.id")
    category_id = serializers.IntegerField(read_only=True, source="category.id")
    image = Base64ImageField()

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Length of name must be at least 3")
        return value

    class Meta:
        model = Product
        fields = ["id", "barcode", "name", "composition", "image", "producer", "producer_id", "category_id"]


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
    product = ProductSerializer(read_only=True)
    store = serializers.CharField(read_only=True, source="store.name")
    store_id = serializers.IntegerField(read_only=True, source="store.id")
    discount = serializers.FloatField(read_only=True, source="discount.old_price")

    class Meta:
        model = StoreItem
        fields = ["id", "price", "product", "store", "store_id", "discount"]


class TransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True, source="user.id")
    vendor_id = serializers.IntegerField(read_only=True, source="vendor.id")

    class Meta:
        model = Transaction
        fields = ["id", "transaction_amount", "vendor_id", "vendor_name", "user_id"]


class TransactionItemSerializer(serializers.ModelSerializer):
    transaction_id = serializers.IntegerField(read_only=True, source="translation.id")
    store_item_id = serializers.IntegerField(read_only=True, source="store_item.id")

    class Meta:
        model = TransactionItem
        fields = ["id", "transaction_id", "store_item_id", "store_item_name", "amount", "price"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "name"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(validated_data.get("phone_number"), validated_data.get("password"))


class PromoSerializer(serializers.ModelSerializer):
    store_chain = StoreChainSerializer(read_only=True)

    class Meta:
        model = Promo
        fields = ("id", "text", "store_chain")


class DiscountSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(read_only=True, source="store_item.price")
    store_chain = StoreChainSerializer(read_only=True, source="store_item.store.store_chain")
    product = ProductSerializer(read_only=True, source="store_item.product")

    class Meta:
        model = Discount
        fields = ("id", "old_price", "price", "store_chain", "product")

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .. import serializers
from ..models import ProductCategory
from ..common.errors import ErrorCode


class ProductCategoryListView(ModelViewSet):
    serializer_class = serializers.ProductCategorySerializer

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        return ProductCategory.objects.all()[offset:offset + amount]


class ProductCategoryView(ModelViewSet):
    serializer_class = serializers.ProductCategorySerializer
    queryset = ProductCategory.objects.all()
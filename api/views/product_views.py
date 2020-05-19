from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .. import serializers
from ..models import Product, Producer
from ..common import permissions
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class ProductListView(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    parser_class = (MultiPartParser, FormParser, FileUploadParser)

    def get_queryset(self):
        amount = self.request.data.get("amount", 10)
        offset = self.request.data.get("offset", 0)
        producer_id = self.request.data.get("producer_id", None)
        if producer_id:
            return Product.objects.filter(producer__id=producer_id)[offset:amount + offset]
        else:
            return Product.objects.all()[offset:amount + offset]

    def perform_create(self, serializer):
        producer = get_object_or_404(Producer, pk=self.request.data.get("producer_id"))
        return serializer.save(producer=producer)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (permissions.IsAdmin, permissions.IsPartnerWorker, permissions.IsPartner)
        return super(self.__class__, self).get_permissions()


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.data.get("image", None) and instance.image:
            instance.image.delete()
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        producer_id = self.request.data.get("producer_id", None)
        if producer_id:
            producer = get_object_or_404(Producer, pk=producer_id)
            return serializer.save(producer=producer)
        else:
            return serializer.save()

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()

    def get_permissions(self):
        if self.action in ("update", "destroy"):
            self.permission_classes = (permissions.IsAdmin,)
        return super(self.__class__, self).get_permissions()

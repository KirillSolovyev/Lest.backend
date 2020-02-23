from django.contrib import admin
from .models import Producer, Product, Store, StoreItem, StoreChain, Transaction, TransactionItem

admin.site.register(StoreChain)
admin.site.register(StoreItem)
admin.site.register(Producer)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
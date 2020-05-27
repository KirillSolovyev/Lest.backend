from django.contrib import admin
from .models import Producer, Product, Store, StoreItem, StoreChain, Transaction, \
                    TransactionItem, PhoneOTP, User, ProductCategory, Promo, Discount

admin.site.register(StoreChain)
admin.site.register(StoreItem)
admin.site.register(Producer)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(PhoneOTP)
admin.site.register(User)
admin.site.register(Promo)
admin.site.register(Discount)
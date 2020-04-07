"""projectX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import settings
from api.views import product_views, producer_views, storechain_views, store_views, store_item_views, transaction_views, auth_views

paths = {
    "ProducerListView": producer_views.ProducerListView.as_view({'post': 'list', 'put': 'create'}),
    "ProducerView": producer_views.ProducerView.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}),
    "ProductListView": product_views.ProductListView.as_view({'post': 'list', 'put': 'create'}),
    "ProductView": product_views.ProductView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
    "StoreChainListView": storechain_views.StoreChainListView.as_view({'post': 'list', 'put': 'create'}),
    "StoreChainView": storechain_views.StoreChainView.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}),
    "StoreListView": store_views.StoreListView.as_view({'post': 'list', 'put': 'create'}),
    "StoreView": store_views.StoreView.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}),
    "StoreItemListView": store_item_views.StoreItemListView.as_view({'post': 'list', 'put': 'create'}),
    "StoreItemView": store_item_views.StoreItemView.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'}),
    "UserTransactionListView": transaction_views.TransactionListView.as_view({'post': 'list'})
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('producers/', paths["ProducerListView"], name='producer_list'),
    path('producers/<int:pk>/', paths["ProducerView"], name="producer"),
    path('products/', paths["ProductListView"], name='product_list'),
    path('products/<int:pk>/', paths["ProductView"], name='product'),
    path('storechains/', paths["StoreChainListView"], name='store_chain_list'),
    path('storechains/<int:pk>/', paths["StoreChainView"], name='store_chain'),
    path('stores/', paths["StoreListView"], name='store_list'),
    path('stores/<int:pk>/', paths["StoreView"], name='store'),
    path('store/items/', paths["StoreItemListView"], name='store_item_list'),
    path('store/items/<int:pk>/', paths["StoreItemView"], name='store_item'),
    path('transactions/proceed/', transaction_views.ProceedTransactionView.as_view(), name='proceed_transaction'),
    path('transactions/', paths["UserTransactionListView"], name="user_transactions"),
    path('login/', auth_views.AuthView.as_view(), name='login'),
    path('registration/', auth_views.RegistrationView.as_view(), name="registration"),
    path('validate/phone/', auth_views.ValidatePhoneOTPView.as_view(), name="validate_phone")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

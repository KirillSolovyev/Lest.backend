from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator

from .managers import UserManager
from .common.roles import Role


class StaffUsersManager(models.Manager):
    def get_queryset(self):
        return super(StaffUsersManager, self).get_queryset().filter(is_staff=True)


class VerifiedUsersManager(models.Manager):
    def get_queryset(self):
        return super(VerifiedUsersManager, self).get_queryset().filter(is_verified=True)


class AdultUsersManager(models.Manager):
    def get_queryset(self):
        return super(AdultUsersManager, self).get_queryset().filter(age__gt=18)


class AdminUsersManager(models.Manager):
    def get_queryset(self):
        return super(AdminUsersManager, self).get_queryset().filter(role=Role.ADMIN.value)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.IntegerField(default=Role.USER.value)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    staff_users = StaffUsersManager()
    verified_users = VerifiedUsersManager()
    adult_users = AdultUsersManager()
    admin_users = AdminUsersManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    key = models.CharField(max_length=100, unique=True, blank=True)
    verified = models.BooleanField(default=False)
    reset_pass = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number + " otp: " + self.key


class Producer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    composition = models.CharField(max_length=255, blank=True)
    producer = models.ForeignKey(Producer, related_name="products", on_delete=models.PROTECT)
    barcode = models.BigIntegerField()
    category = models.ForeignKey(ProductCategory, related_name="products", on_delete=models.PROTECT)
    image = models.ImageField(upload_to="images/products", blank=True)

    def __str__(self):
        return self.name + " " + self.producer.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["barcode"], name="product_barcode")
        ]


class StoreChain(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/store_chains", blank=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    store_chain = models.ForeignKey(StoreChain, related_name="stores", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return self.store_chain.name + " " + self.address


class StoreItem(models.Model):
    price = models.FloatField()
    product = models.ForeignKey(Product, related_name="store_items", on_delete=models.PROTECT)
    store = models.ForeignKey(Store, related_name="store_items", on_delete=models.CASCADE)

    def __str__(self):
        return self.store.__str__() + " " + self.product.__str__()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'store'], name="one_product_per_store")
        ]


class Promo(models.Model):
    store_chain = models.ForeignKey(StoreChain, related_name="promos", on_delete=models.PROTECT)
    text = models.CharField(max_length=150)

    def __str__(self):
        return self.store_chain.name + ": " + self.text


class Discount(models.Model):
    store_item = models.OneToOneField(StoreItem, related_name="discount", on_delete=models.PROTECT)
    old_price = models.FloatField()

    def __str__(self):
        return self.store_item.__str__() + " old price:" + str(self.old_price)


class Transaction(models.Model):
    user = models.ForeignKey(User, related_name="transactions", on_delete=models.PROTECT)
    vendor = models.ForeignKey(Store, related_name="+", on_delete=models.SET(-1))
    vendor_name = models.CharField(max_length=150, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.vendor_name + " " + str(self.transaction_amount) + " " + self.get_formatted_date('%d.%m.%y %H:%M:%S')

    def get_formatted_date(self, format_str):
        return self.date.strftime(format_str)


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, related_name="transaction_items", on_delete=models.CASCADE)
    store_item = models.ForeignKey(StoreItem, related_name="+", on_delete=models.SET(-1))
    store_item_name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.store_item_name + ": " + str(self.amount) + " x " + str(self.price) + "$"


class AbstractPromoCampaign(models.Model):
    store_chain = models.ForeignKey(StoreChain, related_name="%(class)s_promo_campaign", on_delete=models.PROTECT)
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField()
    description = models.CharField(max_length=150)

    class Meta:
        abstract = True


class PartnerCampaign(AbstractPromoCampaign):
    conditions = models.CharField(max_length=100)


class PaidCampaign(AbstractPromoCampaign):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

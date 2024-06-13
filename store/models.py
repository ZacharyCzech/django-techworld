from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        customer = self.model(email=email, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name='customer_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customer_set', blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return super().has_module_perms(app_label)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=1, null=True, blank=True)
    image = models.ImageField(upload_to='upload/product/')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {str(self.id)}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'Order Item - {str(self.id)}'

import re

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Addition(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.price})"


class RegularPizza(models.Model):
    name = models.CharField(max_length=64)
    sm_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    lg_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="reg_pizzas")

    def __str__(self):
        return re.sub(r'[^\w]', '', self.name).replace(' ', '-')


class SicilianPizza(models.Model):
    name = models.CharField(max_length=64)
    sm_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    lg_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="sic_pizzas")

    def __str__(self):
        return re.sub(r'[^\w]', '', self.name).replace(' ', '-')


class Sub(models.Model):
    name = models.CharField(max_length=64)
    sm_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    lg_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    additions = models.ManyToManyField(Addition, blank=True, related_name="subs")

    def __str__(self):
        return re.sub(r'[^\w]', '', self.name).replace(' ', '-')


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return re.sub(r'[^\w]', '', self.name).replace(' ', '-')


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return re.sub(r'[^\w]', '', self.name).replace(' ', '-')


class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    sm_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    lg_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return re.sub(r'[^\w]', '', self.name).replace(' ', '-')


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}: {self.total_price}'


class CartItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    size = models.CharField(max_length=16, blank=True, null=True)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="cart_items")
    additions = models.ManyToManyField(Addition, blank=True, related_name="cart_items")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pending = models.BooleanField(default=False)
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, related_name="cart_items")

    def __str__(self):
        return f'{self.user}: {self.item} ({self.price})'

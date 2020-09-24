from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=225)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(blank=True)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return "Sold {} - {} items for {}".format(self.product.name, self.quantity, self.total_price)

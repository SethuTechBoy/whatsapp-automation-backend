from django.db import models


STEP_CHOICES = [
    ("START", "Start"),
    ("LANGUAGE_SELECTED", "Language Selected"),
    ("PRODUCT_SELECTED", "Product Selected"),
    ("WATCHING_DEMO", "Watching Demo"),
    ("VIEWING_DETAILS", "Viewing Details"),
    ("PAYMENT_SELECTION", "Payment Selection"),
    ("PAYMENT_PENDING", "Payment Pending"),
    ("ORDER_CONFIRMED", "Order Confirmed"),
]


class Customer(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=20, default="EN")
    current_step = models.CharField(
        max_length=50,
        choices=STEP_CHOICES,
        default="START"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    youtube_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

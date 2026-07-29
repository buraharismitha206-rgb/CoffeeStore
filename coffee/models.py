from django.db import models

class CoffeeOrder(models.Model):

    customer_name = models.CharField(max_length=100)

    email = models.EmailField()

    coffee_name = models.CharField(max_length=100)

    amount = models.IntegerField()

    razorpay_order_id = models.CharField(max_length=200)

    razorpay_payment_id = models.CharField(max_length=200, blank=True)

    razorpay_signature = models.CharField(max_length=300, blank=True)

    payment_status = models.CharField(max_length=30, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

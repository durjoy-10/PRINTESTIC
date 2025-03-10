from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Product Model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('T-Shirts', 'T-Shirts'),
        ('Shirt', 'Shirt'),
        ('Hoodie', 'Hoodie'),
        ('Jersey', 'Jersey'),
        ('Panjabi', 'Panjabi'),
        ('Pant', 'Pant'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    size = models.CharField(max_length=50)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = PhoneNumberField(default='+1234567890')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

# OrderItem Model (to track multiple products in an order)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    def total_price(self):
        return self.quantity * self.product.price

# Review and Offer Models (unchanged)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name}"

class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()

    def __str__(self):
        return f"Offer on {self.product.name}"
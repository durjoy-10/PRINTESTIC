from django.contrib import admin
from .models import Product, Order, Review, Offer

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Offer)

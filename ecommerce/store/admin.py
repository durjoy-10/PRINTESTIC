from django.contrib import admin
from .models import Product, Order, OrderItem, Review, Offer

# Inline Admin for OrderItem
class OrderItemInline(admin.TabularInline):  # or admin.StackedInline
    model = OrderItem
    extra = 1  # Number of empty forms to display
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return f"${obj.quantity * obj.product.price}"
    total_price.short_description = 'Total Price'

# Custom Admin Class for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'products_and_quantities', 'total_order_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'customer_phone')  # Allow searching by customer name or phone number
    inlines = [OrderItemInline]  # Add the inline for OrderItem

    # Method to display product names and quantities
    def products_and_quantities(self, obj):
        items = obj.items.all()
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in items])
    products_and_quantities.short_description = 'Products & Quantities'

    # Method to calculate the total price of the entire order
    def total_order_price(self, obj):
        total = sum(item.quantity * item.product.price for item in obj.items.all())
        return f"${total}"
    total_order_price.short_description = 'Total Order Price'

# Register models with the admin site
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
admin.site.register(Offer)
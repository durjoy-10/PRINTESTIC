from django.contrib import admin
from .models import Product, ProductSize, Order, OrderItem, Review, Offer

# Inline Admin for ProductSize
class ProductSizeInline(admin.TabularInline):  # or admin.StackedInline
    model = ProductSize
    extra = 1  # Number of empty forms to display

# Custom Admin Class for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description', 'available_stock')
    list_filter = ('category',)
    search_fields = ('name', 'description')  # Allow searching by product name or description
    inlines = [ProductSizeInline]  # Add the inline for ProductSize

    # Method to display available stock (sum of all sizes' stock)
    def available_stock(self, obj):
        return sum(size.stock for size in obj.sizes.all())
    available_stock.short_description = 'Available Stock'

# Inline Admin for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return f"${obj.quantity * obj.product.price}"
    total_price.short_description = 'Total Price'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'customer_phone', 'customer_address', 'products_and_quantities', 'total_order_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    inlines = [OrderItemInline]

    def products_and_quantities(self, obj):
        items = obj.items.all()
        return ", ".join([f"{item.product.name} (Size: {item.size}, x{item.quantity})" for item in items])
    products_and_quantities.short_description = 'Products & Quantities'

    def total_order_price(self, obj):
        total = sum(item.quantity * item.product.price for item in obj.items.all())
        return f"${total}"
    total_order_price.short_description = 'Total Order Price'

    def customer_email(self, obj):
        return obj.customer_email
    customer_email.short_description = 'Customer Email'

    def customer_address(self, obj):
        return obj.address
    customer_address.short_description = 'Customer Address'

# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
admin.site.register(Offer)
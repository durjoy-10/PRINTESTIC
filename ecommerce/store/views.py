from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, Review, Offer
from django.http import HttpResponse

# Home Page
def home(request):
    shirts = Product.objects.filter(category="Shirt")
    t_shirts = Product.objects.filter(category="T-Shirts")
    hoodies = Product.objects.filter(category="Hoodie")
    jerseys = Product.objects.filter(category="Jersey")
    panjabis = Product.objects.filter(category="Panjabi")
    pants = Product.objects.filter(category="Pant")

    context = {
        'shirts': shirts,
        't_shirts': t_shirts,
        'hoodies': hoodies,
        'jerseys': jerseys,
        'panjabis': panjabis,
        'pants': pants,
    }
    return render(request, 'store/home.html', context)

# Product Details Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Place Order
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        email = request.POST.get('email', '')  # Email is optional
        phone = request.POST['phone']
        address = request.POST['address']
        quantity = int(request.POST['quantity'])

        # Check if requested quantity is available
        if quantity > product.stock:
            return HttpResponse("Error: Not enough stock available.")

        # Create and save the order
        Order.objects.create(
            product=product,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            address=address,
            quantity=quantity
        )

        # Reduce stock
        product.stock -= quantity
        product.save()

        # Redirect to order success page
        return redirect('order_success')

    return render(request, 'store/place_order.html', {'product': product})

# Order Success Page
def order_success(request):
    return render(request, 'store/order_success.html')

# Add Review
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        name = request.POST['name']
        rating = int(request.POST['rating'])
        comment = request.POST['comment']

        # Create and save the review
        Review.objects.create(product=product, name=name, rating=rating, comment=comment)

        # Redirect back to the product detail page
        return redirect('product_detail', product_id=product.id)

    return render(request, 'store/add_review.html', {'product': product})

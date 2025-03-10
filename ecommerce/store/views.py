from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, Review, Offer

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
        email = request.POST['email']
        phone = request.POST['phone']  # New field
        address = request.POST['address']
        quantity = int(request.POST['quantity'])

        # Create and save the order
        Order.objects.create(
            product=product,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,  # Store the phone number
            address=address,
            quantity=quantity
        )

        return redirect('home')

    return render(request, 'store/place_order.html', {'product': product})

# Add Review
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = request.POST['name']
        rating = int(request.POST['rating'])
        comment = request.POST['comment']

        Review.objects.create(product=product, name=name, rating=rating, comment=comment)
        return redirect('product_detail', product_id=product.id)

    return render(request, 'store/add_review.html', {'product': product})

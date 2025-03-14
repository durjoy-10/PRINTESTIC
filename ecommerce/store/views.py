from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, Review,OrderItem,Offer,ProductSize
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
    sizes = product.sizes.all()
    return render(request, 'store/product_detail.html', {'product': product, 'sizes': sizes})


#Place_order
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    all_products = Product.objects.all()
    sizes = product.sizes.all()

    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        email = request.POST.get('email', '')  # Email is optional
        phone = request.POST['phone']
        address = request.POST['address']
        size = request.POST['size']
        quantity = int(request.POST['quantity'])

        # Check if requested quantity is available for the selected size
        selected_size = product.sizes.filter(size=size).first()
        if not selected_size or quantity > selected_size.stock:
            return HttpResponse("Error: Not enough stock available for the selected size.")

        # Create the Order
        order = Order.objects.create(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            address=address
        )

        # Create the OrderItem for the initial product
        OrderItem.objects.create(
            order=order,
            product=product,
            size=size,
            quantity=quantity
        )

        # Reduce stock for the selected size
        selected_size.stock -= quantity
        selected_size.save()

        # Handle additional sizes (if any)
        additional_sizes = request.POST.getlist('additional_sizes')
        additional_quantities = request.POST.getlist('additional_quantities')

        for size, qty in zip(additional_sizes, additional_quantities):
            additional_quantity = int(qty)
            additional_size = product.sizes.filter(size=size).first()

            # Check if requested quantity is available for the selected size
            if not additional_size or additional_quantity > additional_size.stock:
                return HttpResponse(f"Error: Not enough stock available for {product.name} (Size: {size}).")

            # Create the OrderItem for the additional size
            OrderItem.objects.create(
                order=order,
                product=product,
                size=size,
                quantity=additional_quantity
            )

            # Reduce stock for the additional size
            additional_size.stock -= additional_quantity
            additional_size.save()

        # Redirect to order success page
        return redirect('order_success')

    context = {
        'product': product,
        'all_products': all_products,
        'sizes': sizes,
    }
    return render(request, 'store/place_order.html', context)


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
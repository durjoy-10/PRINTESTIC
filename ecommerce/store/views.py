from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, Review,OrderItem,Offer
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


#Place_order
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    all_products = Product.objects.all()

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
            quantity=quantity
        )

        # Reduce stock for the initial product
        product.stock -= quantity
        product.save()

        # Handle additional products (if any)
        additional_products = request.POST.getlist('additional_products')
        additional_quantities = request.POST.getlist('additional_quantities')

        for prod_id, qty in zip(additional_products, additional_quantities):
            additional_product = Product.objects.get(id=prod_id)
            additional_quantity = int(qty)

            # Check if requested quantity is available
            if additional_quantity > additional_product.stock:
                return HttpResponse(f"Error: Not enough stock available for {additional_product.name}.")

            # Create the OrderItem for the additional product
            OrderItem.objects.create(
                order=order,
                product=additional_product,
                quantity=additional_quantity
            )

            # Reduce stock for the additional product
            additional_product.stock -= additional_quantity
            additional_product.save()

        # Redirect to order success page
        return redirect('order_success')

    context = {
        'product': product,
        'all_products': all_products,
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
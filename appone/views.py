from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage  # Import Paginator and EmptyPage
from .models import Product, Productshop  # Import Product and Productshop models
from .forms import SignupForm, LoginForm

def cg(request):
    return render(request, 'about.html')

def cg1(request):
    return render(request, 'cart.html')

def cg2(request):
    return render(request, 'checkout.html')

def cg3(request):
    return render(request, 'contact-us.html')

def cg4(request):
    return render(request, 'gallery.html')

def cg5(request):
    products = Product.objects.all()  # Retrieve all products
    return render(request, 'index.html', {'products': products})

def cg6(request):
    return render(request, 'my-account.html')

def cg7(request):
    return render(request, 'shop-detail.html')

def shop(request):
    ordering = request.GET.get('ordering')
    productshop = Productshop.objects.all()

    if ordering:
        productshop = productshop.order_by(ordering)

    page = request.GET.get('page', 1)
    PRODUCTS_PER_PAGE = 10  # Set the number of products per page

    product_paginator = Paginator(productshop, PRODUCTS_PER_PAGE)

    try:
        productshop = product_paginator.page(page)
    except EmptyPage:
        productshop = product_paginator.page(product_paginator.num_pages)

    return render(request, 'shop.html', {'productshop': productshop, 'page_obj': productshop, 'is_paginated': True, 'paginator': product_paginator})

def cg9(request):
    return render(request, 'wishlist.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the homepage after login
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully signed up!')
                return redirect('index')  # Redirect to the homepage after signup
    else:
        form = SignupForm()
    return render(request, 'login.html', {'form': form})

def cg11(request):
    return render(request, 's1.html')

def cg12(request):
    return render(request, 's2.html')

def cg13(request):
    return render(request, 's3.html')


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from django.http import JsonResponse

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

    return JsonResponse({
        'success': True,
        'product': product.name,
        'quantity': cart_item.quantity,
        'total_price': total_price
    })

@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart.html', {'cart': cart})

def shop_view(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'productshop': products})

def db1(request):
    return render(request, 'dashboard.html')

def db2(request):
    return render(request, 'map.html')

def db6(request):
    return render(request, 'notifications.html')

def db3(request):
    return render(request, 'tables.html')




    
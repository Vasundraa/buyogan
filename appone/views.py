from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Product, Productshop, Cart, CartItem, Payment
from .forms import SignupForm, LoginForm
from django.conf import settings
import razorpay

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
    products = Product.objects.all()
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
    PRODUCTS_PER_PAGE = 10

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
                return redirect('index')
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
                return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'login.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

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
    if request.method == 'POST':
        amount = 1000  # Example amount, you can set it dynamically based on your requirements
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({'amount': amount * 100, 'currency': 'INR', 'payment_capture': '1'})

        payment = Payment(order_id=order['id'], amount=amount)
        payment.save()

        context = {
            'order_id': order['id'],
            'amount': amount * 100,  # Multiply by 100 to convert to paisa (Razorpay expects amount in paisa)
            'razorpay_key': settings.RAZORPAY_KEY_ID,
        }
        return render(request, 'payment.html', context)
    return render(request, 'p-dashboard.html')

@login_required
def payment_process(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            payment = Payment.objects.get(order_id=order_id)
            payment.payment_id = payment_id
            payment.status = 'paid'
            payment.save()

            messages.success(request, "Payment was successful.")
            return redirect("suc")  
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed.")
            return redirect("fai")  
    else:
        return HttpResponseBadRequest("Invalid request method.")
    

def db2(request):
    return render(request, 'map.html')


def db3(request):
    return render(request, 'p-schedule.html')

def db6(request):
    return render(request, 'p-order.html')

def suc(request):
    return render(request, 'success.html')

def fai(request):
    return render(request, 'failure.html')

def ow1(request):
    return render(request, 'o-dashboard.html')

def ow2(request):
    return render(request, 'o-schedule.html')

def ow3(request):
    return render(request, 'o-order.html')
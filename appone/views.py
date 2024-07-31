from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import SignupForm, LoginForm
from django.conf import settings
import razorpay
from django.utils.timezone import now
from datetime import timedelta
from datetime import datetime
import calendar
from .forms import WasteRequestForm
from appone.management.commands.calculate_avg_waste import Command as WasteAvgCommand
from .forms import FeedbackForm

def cg(request):
    return render(request, 'about.html')

def cg1(request):
    return render(request, 'cart.html')

def cg2(request):
    return render(request, 'checkout.html')

def cg3(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for your feedback!')
            return redirect('contact-us')  # Ensure 'contact-us' is the correct name for your URL pattern
        else:
            # Display the exact errors from the form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = FeedbackForm()

    return render(request, 'contact-us.html', {'form': form})

def cg4(request):
    return render(request, 'gallery.html')

def cg5(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def cg6(request):
    return render(request, 'my-account.html')

import random

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Get 10 random products
    product_ids = list(Product.objects.values_list('id', flat=True))
    random.shuffle(product_ids)
    random_product_ids = product_ids[:10]
    random_products = Product.objects.filter(id__in=random_product_ids)
    
    return render(request, 'shop-detail.html', {'product': product, 'random_products': random_products})

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
    category_id = request.GET.get('category')
    ordering = request.GET.get('ordering')
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    if ordering:
        products = products.order_by(ordering)

    categories = Category.objects.all()
    
    page = request.GET.get('page', 1)
    PRODUCTS_PER_PAGE = 10

    product_paginator = Paginator(products, PRODUCTS_PER_PAGE)

    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    context = {
        'categories': categories,
        'productshop': products,
        'page_obj': products,
        'is_paginated': True,
        'paginator': product_paginator,
        'selected_category': category_id
    }

    return render(request, 'shop.html', context)
'''
def db1(request):
    if request.method == 'POST':
        amount = 1000 
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({'amount': amount * 100, 'currency': 'INR', 'payment_capture': '1'})

        payment = Payment(order_id=order['id'], amount=amount)
        payment.save()

        context = {
            'order_id': order['id'],
            'amount': amount * 100,  
            'razorpay_key': settings.RAZORPAY_KEY_ID,
        }
        return render(request, 'payment.html', context)
    return render(request, 'p-dashboard.html')
'''

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

def get_last_four_months_data():
    now = timezone.now()
    current_year = now.year
    current_month = now.month

    # Calculate the last four months excluding the current month
    months = [(current_year, current_month - i) for i in range(1, 5)]
    
    # Adjust months and years if crossing year boundaries
    months = [(y, m) for y, m in months if m > 0]  # Remove negative months
    months += [(current_year - 1, m + 12) for y, m in months if m <= 0]  # Handle year transition
    
    # Fetch data for the months
    data = []
    labels = []
    for year, month in months:
        try:
            item = PlasticItem.objects.get(date__year=year, date__month=month)
            data.append(item.total)
        except PlasticItem.DoesNotExist:
            data.append(0)
        
        # Format month and year into 'Month Year'
        month_name = calendar.month_abbr[month % 12]  # month % 12 handles the transition from Dec to Jan
        year = year if month > 0 else year - 1
        labels.append(f"{month_name} {year}")

    return data, labels

def get_current_month_data():
    now = timezone.now()
    try:
        item = PlasticItem.objects.get(date__year=now.year, date__month=now.month)
        return item.total, item.date
    except PlasticItem.DoesNotExist:
        return 0, None

def get_previous_month_data():
    now = timezone.now()
    prev_month = now.month - 1
    prev_year = now.year

    if prev_month <= 0:
        prev_month = 12
        prev_year -= 1

    try:
        item = PlasticItem.objects.get(date__year=prev_year, date__month=prev_month)
        return item.total
    except PlasticItem.DoesNotExist:
        return 0
    
def get_current_month_field_data():
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Initialize counts
    counts = {
        'PET': 0,
        'HDPE': 0,
        'PVC': 0,
        'ORGANIC': 0,
        'OTHER': 0
    }

    # Get items for the current month
    items = PlasticItem.objects.filter(date__year=current_year, date__month=current_month)

    # Sum counts for each field
    for item in items:
        counts['PET'] += item.pet
        counts['HDPE'] += item.hdpe
        counts['PVC'] += item.pvc
        counts['ORGANIC'] += item.organic
        counts['OTHER'] += item.other

    return counts

def db1(request):
    plastic_item = PlasticItem.get_or_create_for_current_month()
    data, labels = get_last_four_months_data()
    current_month_data, last_updated = get_current_month_data()
    previous_month_data = get_previous_month_data()
    field_data = get_current_month_field_data()

    # Calculate percentage increase
    if previous_month_data > 0:
        percentage_increase = ((current_month_data - previous_month_data) / previous_month_data) * 100
    else:
        percentage_increase = 0

    # Determine increase or decrease
    increase_sign = '+' if percentage_increase >= 0 else '-'
    percentage_increase_abs = abs(percentage_increase)
    
    # Format percentage increase
    percentage_increase_str = f"{increase_sign}{percentage_increase_abs:.0f}%"
    
    # Format last updated date
    last_updated_str = last_updated.strftime("%b %d, %Y") if last_updated else "No data available"

    # Calculate average values for the last 4 months
    waste_avg_command = WasteAvgCommand()
    monthly_averages = waste_avg_command.calculate_averages()
    months_labels = [avg['month'] for avg in monthly_averages]
    avg_values = [avg['average'] for avg in monthly_averages]

    context = {
        'plastic_item': plastic_item,
        'data': data,
        'labels': labels,
        'current_month_data': current_month_data,
        'last_updated': last_updated_str,
        'percentage_increase': percentage_increase_str,
        'field_data': field_data, 
        'months_labels': months_labels,
        'avg_values': avg_values,
           
              }
    return render(request, 'dashboard.html', context)

def db3(request):
    current_date = now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Filter deliveries for the current week
    deliveries = Delivery.objects.filter(date__range=[start_of_week, end_of_week])
    
    context = {
        'delivery': deliveries,
    }
    return render(request, 'schedule.html', context)

def db6(request):
    if request.method == 'POST':
        form = WasteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your request has been placed successfully!')
            return redirect('order')  # Replace 'order' with your form's URL name
        else:
            # Print form errors to the console
            print("Form is not valid")
            print("Form errors:", form.errors)
    else:
        form = WasteRequestForm()

    return render(request, 'order.html', {'form': form})

def suc(request):
    return render(request, 'success.html')

def fai(request):
    return render(request, 'failure.html')

def ma(request):
    return render(request, 'maporgi.html')
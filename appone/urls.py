from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('about/', views.cg, name='about'),
    path('cart/', views.cg1, name='cart'),
    path('checkout/', views.cg2, name='checkout'),
    path('contact-us/', views.cg3, name='contact-us'),
    path('gallery/', views.cg4, name='gallery'),
    path('', views.cg5, name='index'),
    path('my-account/', views.cg6, name='my-account'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('shop/',views.shop_view,name='shop'), 
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),     
    path('cart/', views.cart_view, name='cart'),      
    path('wishlist/', views.cg9, name='wishlist'),
    path('login', views.login_view, name='login'),  # New URL pattern for login
    path('signup/', views.signup_view, name='signup'),  # New URL pattern for signup
    path('dashboard/', views.db1, name='dashboard'),
    #path('payment_process/', views.payment_process, name='payment_process'),  # Add this line for payment process
    path('map/', views.db2, name='map'), 
    path('order/', views.db6, name='order'),     
    path('schedule/', views.db3, name='schedule'),   
    path('accounts/', include('django.contrib.auth.urls')), 
    path('maporgi/', views.ma, name='maporgi'), 
 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

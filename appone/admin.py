from django.contrib import admin

# Register your models here.
from.models import Product,Productshop,Cart,CartItem,Payment
admin.site.register(Product)
admin.site.register(Productshop)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)


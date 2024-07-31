from django.contrib import admin

# Register your models here.
from.models import *


admin.site.register(Category)


admin.site.register(Product)

admin.site.register(Delivery)



class PlasticItemAdmin(admin.ModelAdmin):
    list_display = ('pet', 'hdpe', 'pvc', 'other', 'organic', 'total', 'date')
    readonly_fields = ('total', 'date')

    def get_queryset(self, request):
        """ Show all records, regardless of the month. """
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        """ Ensure only one instance per month is saved. """
        if not change:  # If it's a new object
            instance = PlasticItem.get_or_create_for_current_month()
            # Update instance with new data
            instance.pet = obj.pet
            instance.hdpe = obj.hdpe
            instance.pvc = obj.pvc
            instance.other = obj.other
            instance.organic = obj.organic
            instance.save()
        else:
            super().save_model(request, obj, form, change)

admin.site.register(PlasticItem, PlasticItemAdmin)

class WasteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_name', 'phone_number', 'email_id', 'waste_type', 'amount_needed', 'request_date')
    list_filter = ('waste_type', 'request_date')
    search_fields = ('name', 'organization_name', 'email_id', 'waste_type')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly
        return [field.name for field in self.model._meta.get_fields()]

admin.site.register(WasteRequest, WasteRequestAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')  # Include submitted_at here
    list_filter = ('submitted_at',)  # Optionally, add a filter by date
    search_fields = ('name', 'email', 'subject', 'message')
    
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly
        return [field.name for field in self.model._meta.get_fields()]
    
admin.site.register(Feedback, FeedbackAdmin)

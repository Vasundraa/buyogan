from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WasteRequest, PlasticItem

@receiver(post_save, sender=WasteRequest)
def update_plastic_item(sender, instance, **kwargs):
    # Get the current month and year
    year, month = PlasticItem.get_current_month()
    
    # Get or create the PlasticItem for the current month
    plastic_item, created = PlasticItem.objects.get_or_create(
        date__year=year,
        date__month=month,
        defaults={'pet': 0, 'hdpe': 0, 'pvc': 0, 'other': 0, 'organic': 0}
    )
    
    # Update the fields based on the waste_type
    if instance.waste_type == 'PET':
        plastic_item.pet = max(plastic_item.pet - instance.amount_needed, 0)
    elif instance.waste_type == 'HDPE':
        plastic_item.hdpe = max(plastic_item.hdpe - instance.amount_needed, 0)
    elif instance.waste_type == 'PVC':
        plastic_item.pvc = max(plastic_item.pvc - instance.amount_needed, 0)
    elif instance.waste_type == 'Organic':
        plastic_item.organic = max(plastic_item.organic - instance.amount_needed, 0)
    elif instance.waste_type == 'Others':
        plastic_item.other = max(plastic_item.other - instance.amount_needed, 0)

    # Save the updated PlasticItem
    plastic_item.save()

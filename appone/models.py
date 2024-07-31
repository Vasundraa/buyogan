from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    is_new = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',null=True)
    organisation_name = models.CharField(max_length=255)
    quantities = models.PositiveIntegerField()
    contact_details = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")]
    )

    def __str__(self):
        return self.name

   

class Delivery(models.Model):
    name = models.CharField(max_length=100)  
    area = models.CharField(max_length=100)  
    district = models.CharField(max_length=100) 
    date = models.DateField()  
    truck_no = models.CharField(max_length=20)  

    def __str__(self):
        return f"{self.name} - {self.truck_no}"



class PlasticItem(models.Model):
    pet = models.PositiveIntegerField(default=0)    
    hdpe = models.PositiveIntegerField(default=0)   
    pvc = models.PositiveIntegerField(default=0)    
    other = models.PositiveIntegerField(default=0)  
    organic = models.PositiveIntegerField(default=0) 
    date = models.DateField(auto_now_add=True)       

    @property
    def total(self):
        return self.pet + self.hdpe + self.pvc + self.other + self.organic

    def __str__(self):
        return f"PET: {self.pet}, HDPE: {self.hdpe}, PVC: {self.pvc}, Other: {self.other}, Organic: {self.organic}, Total: {self.total}, Date: {self.date}"

    @classmethod
    def get_current_month(cls):
        now = timezone.now()
        return now.year, now.month

    @classmethod
    def get_or_create_for_current_month(cls):
        year, month = cls.get_current_month()
        return cls.objects.get_or_create(
            date__year=year,
            date__month=month,
            defaults={'pet': 0, 'hdpe': 0, 'pvc': 0, 'other': 0, 'organic': 0}
        )[0]



class WasteRequest(models.Model):
    WASTE_TYPE_CHOICES = [
        ('PET', 'PET'),
        ('HDPE', 'HDPE'),
        ('PVC', 'PVC'),
        ('Organic', 'Organic'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    organization_name = models.CharField(max_length=100, verbose_name="Organization Name")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    email_id = models.EmailField(verbose_name="Email ID")
    waste_type = models.CharField(
        max_length=50,
        choices=WASTE_TYPE_CHOICES,
        verbose_name="Type of Waste Needed"
    )
    amount_needed = models.PositiveIntegerField(verbose_name="Amount of Waste Needed (kg)")
    request_date = models.DateField(auto_now_add=True, verbose_name="Request Date")

    def __str__(self):
        return f"{self.name} - {self.organization_name} - {self.waste_type} ({self.amount_needed} kg)-{self.request_date}"


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")

    def __str__(self):
        return f"{self.name} - {self.subject}"
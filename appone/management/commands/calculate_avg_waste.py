from django.core.management.base import BaseCommand
from django.utils import timezone
from appone.models import WasteRequest
from datetime import datetime, timedelta
from django.db.models import Avg

class Command(BaseCommand):
    help = 'Calculate the average amount_needed for each of the last 4 months, excluding the current month'

    def handle(self, *args, **kwargs):
        averages = self.calculate_averages()
        for avg in averages:
            print(f"Month: {avg['month']}, Average amount_needed: {avg['average']}")

    def calculate_averages(self):
        # Get the current date and calculate the first day of the current month
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        
        # Calculate the end of the 4-month period
        end_date = first_day_of_current_month - timedelta(days=1)
        
        # Calculate the start of the 4-month period
        start_date = end_date - timedelta(days=120)  # 4 months approximately
        
        # Generate the list of the last 4 months excluding the current month
        months = []
        for i in range(4):
            month_start = end_date - timedelta(days=30*i)
            month_start = month_start.replace(day=1)  # Set to the first day of the month
            month_end = month_start.replace(day=28) + timedelta(days=4)  # Go to the end of the month
            month_end = month_end - timedelta(days=month_end.day)
            months.append((month_start, month_end))
        
        averages = []
        for start_date, end_date in months:
            month_label = start_date.strftime('%b %Y')
            
            # Query WasteRequest data for each month
            waste_requests = WasteRequest.objects.filter(
                request_date__range=[start_date, end_date]
            )
            
            # Calculate average amount_needed
            avg_amount_needed = waste_requests.aggregate(Avg('amount_needed'))['amount_needed__avg']
            averages.append({'month': month_label, 'average': avg_amount_needed or 0})
        
        return averages

from django.utils import timezone
from datetime import timedelta

from random import randint

def calculate_time_ago(created_at):
        now = timezone.now()
        diff = now - created_at

        seconds = diff.total_seconds()
        if seconds < 60:
            return "Just now"
        minutes = seconds // 60

        if minutes < 60:
            return f"{int(minutes)} {'s' if minutes>=2 else ''} ago"
        hours = minutes // 60
        if hours < 24:
            return f"{int(hours)} hour{'s' if hours >= 2 else ''} ago"
        days = hours // 24
        if days < 7:
            return f"{int(days)} day{'s' if days >= 2 else ''} ago"
        weeks = days // 7
        if weeks < 5:
            return f"{int(weeks)} week{'s' if weeks >= 2 else ''} ago"
        months = days // 30
        if months <12:
            return f"{int(months)} month{'s' if months <=2 else ''} ago"
        years = days // 365
        return f"{int(years)} year{'s' if years<=2 else ''} ago"

def generate_random_otp():
    return randint(1111,9999)

def default_expire_time():
    return timezone.now() + timedelta(minutes=4)
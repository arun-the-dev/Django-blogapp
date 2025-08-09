from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from .models import Otp

@shared_task
def delete_expired_otps():
    now = timezone.now()
    count, _ = Otp.objects.filter(expire_at__lt=now, is_used=False).delete()
    print(f"[CELERY TASK] Deleted {count} expired OTPs")

@shared_task
def send_otp_email(email,otp):
    return send_mail(
        "Password Reset otp",
        f"Blog app OTP : {otp} ,this only valid for 4 minutes, thanking you",
        from_email="rocky@gmail.com",
        recipient_list=[email],
        fail_silently=True
    )
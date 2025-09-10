from django.conf import settings
from django.core.mail import send_mail
import random
from datetime import timedelta, datetime



def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user, otp):
    subject = 'Verify Your Email - OTP'
    message = f'''
Hello { user.username},

Welcome! Please use the following OTP to verify your email address:

OTP: {otp }

This OTP will expire in 1 minutes.

If you didn't create this account, please ignore this email.

Best regards,
Sentra Exam
    '''.strip()
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
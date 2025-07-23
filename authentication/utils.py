import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTP, User

class EmailService:
    @staticmethod
    def send_otp_email(user_email, otp_code):
        """
        Mock email service - prints OTP instead of sending actual email
        In production, replace this with actual email service
        """
        subject = "Your OTP Code"
        message = f"""
        Your OTP code is: {otp_code}
        
        This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.
        
        If you didn't request this code, please ignore this email.
        """
        
        print(f"\n{'='*50}")
        print(f"📧 MOCK EMAIL SERVICE")
        print(f"{'='*50}")
        print(f"To: {user_email}")
        print(f"Subject: {subject}")
        print(f"OTP Code: {otp_code}")
        print(f"Expires: {settings.OTP_EXPIRY_MINUTES} minutes")
        print(f"{'='*50}\n")
        
        return True

class OTPService:
    @staticmethod
    def generate_and_send_otp(user):
        """Generate OTP and send via email"""
        OTP.objects.filter(user=user, is_used=False).update(is_used=True)
        
        otp_code = OTP.generate_otp()
        otp = OTP.objects.create(user=user, code=otp_code)
        
        EmailService.send_otp_email(user.email, otp_code)
        
        return otp
    
    @staticmethod
    def verify_otp(user, otp_code):
        """Verify OTP code"""
        try:
            otp = OTP.objects.get(
                user=user,
                code=otp_code,
                is_used=False
            )
            
            if otp.is_expired():
                return False, "OTP has expired."
            
            if otp.attempts >= settings.MAX_OTP_ATTEMPTS:
                otp.is_used = True
                otp.save()
                return False, "Maximum OTP attempts exceeded."
            
            otp.is_used = True
            otp.save()
            
            user.is_email_verified = True
            user.save()
            
            return True, "OTP verified successfully."
            
        except OTP.DoesNotExist:
            active_otps = OTP.objects.filter(user=user, is_used=False)
            for active_otp in active_otps:
                active_otp.attempts += 1
                active_otp.save()
            
            return False, "Invalid OTP code."

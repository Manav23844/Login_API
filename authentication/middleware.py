from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import RateLimitLog
import json

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limits = {
            '/api/request-otp': {'requests': 5, 'window': 300},  
            '/api/verify-otp': {'requests': 10, 'window': 300},  
            '/api/register': {'requests': 3, 'window': 3600},    
        }

    def __call__(self, request):
        if request.path in self.rate_limits:
            if not self.check_rate_limit(request):
                return JsonResponse({
                    'error': 'Rate limit exceeded. Please try again later.'
                }, status=429)
        
        response = self.get_response(request)
        return response

    def check_rate_limit(self, request):
        ip_address = self.get_client_ip(request)
        endpoint = request.path
        rate_limit = self.rate_limits[endpoint]
        
        window_start = timezone.now() - timedelta(seconds=rate_limit['window'])
        
        RateLimitLog.objects.filter(
            window_start__lt=window_start
        ).delete()
        
        log, created = RateLimitLog.objects.get_or_create(
            ip_address=ip_address,
            endpoint=endpoint,
            defaults={'request_count': 1}
        )
        
        if not created:
            if log.request_count >= rate_limit['requests']:
                return False
            log.request_count += 1
            log.save()
        
        return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add cache control headers to prevent storing sensitive pages
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

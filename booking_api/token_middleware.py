from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

class HardcodedTokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
            if token == 'abc123xyz456token':
                user, _ = User.objects.get_or_create(username='hardcoded_token_user')
                request.user = user

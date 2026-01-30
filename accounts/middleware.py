from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        request.user = AnonymousUser()

        try:
            auth = self.jwt_auth.authenticate(request)
            if auth:
                request.user, request.auth = auth
        except Exception:
            pass

        return self.get_response(request)
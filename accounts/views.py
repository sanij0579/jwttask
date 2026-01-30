from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, LoginSerializer


# ---------- JWT TOKEN GENERATOR ----------
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


# ---------- SIGNUP ----------
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid():
            # helpful for debugging & interview explanation
            return Response(
                {
                    "message": "Signup failed",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                "message": "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )


# ---------- LOGIN ----------
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        tokens = get_tokens(user)

        return Response(
            {
                "message": "Login successful",
                "tokens": tokens
            },
            status=status.HTTP_200_OK
        )


# ---------- PROTECTED PROFILE ----------
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "email": request.user.email,
                "username": request.user.username
            },
            status=status.HTTP_200_OK
        )
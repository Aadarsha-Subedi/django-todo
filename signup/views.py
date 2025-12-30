from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, VerifySignupSerializer, LoginSerializer

from django.contrib.auth import authenticate

from .models import User, OTP

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils.utils import generate_otp
from .tasks import send_signup_verification_email


# Create your views here.
@api_view(["POST"])
def verify_signup(request):
    verify_signup_serializer = VerifySignupSerializer(data=request.data)

    if not verify_signup_serializer.is_valid():
        return Response(verify_signup_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    generated_otp = generate_otp()
    send_signup_verification_email.delay(verify_signup_serializer.validated_data['email'], generated_otp)

    otp = OTP.objects.create(email=verify_signup_serializer.validated_data['email'],
                             otp=generated_otp)
    otp.save()

    return Response(
        {
            "message":
            "User successfully signed up. Enter the OTP code sent in your email to continue."
        },
        status=status.HTTP_201_CREATED)


@api_view(["POST"])
def signup(request):
    signup_serializer = SignupSerializer(data=request.data)

    if not signup_serializer.is_valid():
        return Response(signup_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(email=signup_serializer.validated_data['email'])
    user.set_password(signup_serializer.validated_data['password'])
    user.save()

    return Response({"message": "You have successfully signed up!"},
                    status=status.HTTP_201_CREATED)

@api_view(["POST"])
def login(request):

    login_serializer = LoginSerializer(data=request.data)

    if not login_serializer.is_valid():
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = login_serializer.validated_data['email']
    password = login_serializer.validated_data['password']
    user = authenticate(username=email, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    return Response({"message": "Login successful", "access_token": str(access_token), "refresh_token": str(refresh_token)  }, status=status.HTTP_200_OK)

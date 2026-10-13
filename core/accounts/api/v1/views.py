from django.shortcuts import get_object_or_404
from rest_framework import generics
from accounts.models import User
from .serialaizers import (
    UserSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ReSendActivationSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage
from threading import Thread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


class RegistrationView(generics.GenericAPIView):

    serializer_class = UserSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "email": email,
            }
            user_object = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_object)
            message = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "sadeghmarfeat@gmail.com",
                to=[email],
            )
            Thread(
                target=message.send,
                daemon=True,
            ).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomLogoutTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(
            {"detail": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()

        return Response(
            {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class VerifyOTPView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            token = jwt.decode(
                self.kwargs["token"], settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token["user_id"]
        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.InvalidTokenError:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(id=user_id)
        if user_obj.is_verified:
            return Response(
                {"detail": "User is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user_obj.is_verified = True
            user_obj.save()
            return Response(
                {"detail": "User activated successfully."}, status=status.HTTP_200_OK
            )


class ReSendActivationView(generics.GenericAPIView):
    serializer_class = ReSendActivationSerializer

    @swagger_auto_schema(request_body=ReSendActivationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user_object = get_object_or_404(User, email=email)
        if user_object.is_verified:
            return Response(
                {"detail": "User is already active."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken.for_user(user_object)
        message = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "sadeghmarfeat@gmail.com",
            to=[email],
        )
        Thread(target=message.send, daemon=True).start()
        return Response(
            {"detail": "Activation email sent successfully."}, status=status.HTTP_200_OK
        )

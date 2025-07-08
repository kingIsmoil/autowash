from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics,serializers,status
from .serializers import *
from .models import CustomUser,EmailConfirmation
from drf_yasg.utils import swagger_auto_schema
from .permission import *

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsSuperUser]

    @swagger_auto_schema(tags=['Authenticate User'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ConfirmEmailView(APIView):
    @swagger_auto_schema(tags=['Authenticate User'])
    def get(self, request, token):  
        try:
            confirm = EmailConfirmation.objects.get(token=token)
            user = confirm.user
            user.is_email_confirmed = True
            user.is_active = True
            user.save()
            confirm.delete()
            return Response({"message": "Email confirmed."})
        except EmailConfirmation.DoesNotExist:
            return Response({"error": "Invalid or expired token."}, status=400)
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=LoginSerializer, tags=['Authenticate User'])
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                'id': user.id,
                'email': user.email
                }
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    @swagger_auto_schema(request_body=LogoutSerializer, tags=['Authenticate User'])
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"},
                                    status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer, tags=['Authenticate User'])
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Письмо для сброса пароля отправлено."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView( APIView):
    @swagger_auto_schema(request_body = ResetPasswordSerializer,tags=['Authenticate User'])
    def post(self, request, token):
        serializer = ResetPasswordSerializer(data={**request.data, "token": token})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пароль успешно обновлён."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
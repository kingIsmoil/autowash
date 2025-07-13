from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from .models import CustomUser, EmailConfirmation,PasswordResetToken
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','fullname', 'phone_number','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        confirmation = EmailConfirmation.objects.create(user=user)
        self.send_confirmation_email(user.email, confirmation.token)
        return user

    def send_confirmation_email(self, email, token):
        confirm_link = f"http://92.255.79.122:8090/accounts/confirm-email/{token}/"
        send_mail(
            subject='Confirm your email',
            message=f'Click here to confirm: {confirm_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_email_confirmed:
            raise serializers.ValidationError("Email not confirmed.")
        data['user'] = user
        return data
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = f"http://92.255.79.122:8090/account/reset-password/{reset_token.token}/"
        send_mail(
            subject="Сброс пароля",
            message=f"Перейдите по ссылке для сброса пароля: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=6)

    def validate(self, data):
        try:
            token_obj = PasswordResetToken.objects.get(token=data['token'])
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Неверный или устаревший токен")

        if token_obj.is_expired():
            raise serializers.ValidationError("Токен истёк")

        self.user = token_obj.user
        return data

    def save(self):
        new_password = self.validated_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        PasswordResetToken.objects.filter(user=self.user).delete()

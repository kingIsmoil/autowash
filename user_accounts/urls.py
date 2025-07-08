from django.urls import path
from .views import RegisterView, ConfirmEmailView, LoginView, LogoutView,ForgotPasswordView,ResetPasswordView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('confirm-email/<uuid:token>/', ConfirmEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uuid:token>/', ResetPasswordView.as_view(), name='reset-password'),
]
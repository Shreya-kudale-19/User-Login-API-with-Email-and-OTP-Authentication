from django.urls import path
from .views import RegisterView, RequestOTPView,  VerifyOTPView, ResendOTPView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('verify-otp', VerifyOTPView.as_view()),
    path('request-otp/', RequestOTPView.as_view(), name='request_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
]

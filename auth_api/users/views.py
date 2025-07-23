# from django.shortcuts import render
# from django.utils import timezone
# from django.utils.crypto import get_random_string
# from datetime import timedelta



# # Create your views here.
# import random
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User, OTP
# from .serializers import RegisterSerializer
# from rest_framework_simplejwt.tokens import RefreshToken

# # Utility: Generate OTP
# def generate_otp():
#     return f"{random.randint(100000, 999999)}"

# # Utility: Create JWT token
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return str(refresh.access_token)

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Registration successful. Please verify your email."}, status=201)
#         return Response(serializer.errors, status=400)

# class RequestOTPView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         try:
#             user = User.objects.get(email=email)
#             otp_code = generate_otp()
#             OTP.objects.create(user=user, code=otp_code)
#             print(f"Mock Email to {email}: Your OTP is {otp_code}")  # MOCK EMAIL
#             return Response({"message": "OTP sent to your email."})
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=404)

# class VerifyOTPView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         code = request.data.get("otp")

#         try:
#             user = User.objects.get(email=email)
#             print("🔍 Verifying OTP...")
#             print("Email:", email)
#             print("OTP entered:", code)
#             print("User exists:", user.email)
#             print("All OTPs:", OTP.objects.filter(user=user).values_list("code", flat=True))

#             otp = OTP.objects.filter(user=user, code=code).last()
 
#             if otp:
#                 print("Latest OTP:", otp.code)
#                 print("Created at:", otp.created_at)
#                 print("Current time:", timezone.now())
#                 print("Is valid:", otp.is_valid())


#             if otp and otp.is_valid():
#                 user.is_verified = True
#                 user.save()
#                 token = get_tokens_for_user(user)
#                 return Response({"message": "Login successful.", "token": token})
#             return Response({"error": "Invalid or expired OTP"}, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=404)

# from .models import CustomUser
# from .utils import generate_otp, send_otp_mock  # Ensure these exist



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.utils import timezone
# from .models import CustomUser
# from .utils import generate_otp, send_otp_mock  # Ensure these exist

# class ResendOTPView(APIView):
#     def post(self, request):
#         email = request.data.get('email')

#         try:
#             user = CustomUser.objects.get(email=email)

#             # Basic rate limiting: Max 5 OTPs per hour
#             now = timezone.now()
#             if user.last_otp_sent and (now - user.last_otp_sent).seconds < 3600:
#                 if user.otp_resend_count >= 5:
#                     return Response({
#                         "status": "error",
#                         "message": "OTP resend limit exceeded. Try again later."
#                     })

#             # Generate and save new OTP
#             otp = generate_otp()
#             user.otp = otp
#             user.otp_created_at = now
#             user.last_otp_sent = now
#             user.otp_resend_count = user.otp_resend_count + 1 if user.otp_resend_count else 1
#             user.save()

#             send_otp_mock(user.email, otp)

#             return Response({
#                 "status": "success",
#                 "message": "OTP resent successfully."
#             })

#         except CustomUser.DoesNotExist:
#             return Response({
#                 "status": "error",
#                 "message": "Email not found."
#             })




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from django.core.mail import send_mail
import random

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['email'] = user.email

            # Mock email service: log or print OTP
            print(f"OTP for {user.email} is: {otp}")

            # In real case, use send_mail()
            # send_mail("Your OTP", f"OTP: {otp}", "from@example.com", [user.email])

            return Response({"message": "Registered successfully. OTP sent to email."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        entered_otp = request.data.get('otp')
        session_otp = request.session.get('otp')
        email = request.session.get('email')

        if entered_otp == session_otp:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return Response({"message": "OTP verified successfully."})
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    def post(self, request):
        email = request.session.get('email')
        if not email:
            return Response({"error": "Session expired or no email found"}, status=status.HTTP_400_BAD_REQUEST)

        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp

        print(f"Resent OTP for {email} is: {otp}")
        # send_mail("Your OTP", f"OTP: {otp}", "from@example.com", [email])

        return Response({"message": "OTP resent successfully."})



from django.utils.crypto import get_random_string
from django.core.cache import cache


class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate random 6-digit OTP
        otp = get_random_string(length=6, allowed_chars='0123456789')
        cache.set(email, otp, timeout=300)  # store for 5 minutes

        # Send email (mock)
        print(f"Sending OTP {otp} to {email}")

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
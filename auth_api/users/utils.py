import random
import string

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_mock(email, otp):
    print(f"Mock Email Sent to {email}: Your OTP is {otp}")

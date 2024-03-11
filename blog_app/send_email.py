from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = 'Verify Your Account'
    message = f'Your OTP for account verification is: {otp}'
    from_email = 'rahulthakur191999@gmail.com'  # Update with your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


# def is_otp_valid(self, otp_entered):
#     # Check if the entered OTP matches the stored OTP
#     if self.otp == otp_entered:
#         # Check if the OTP is expired (e.g., 5 minutes expiry duration)
#         expiry_duration = datetime.timedelta(minutes=5)
#         now = timezone.now()
#         if now <= self.otp_send_time + expiry_duration:
#             return True  # OTP is valid and not expired
#     return False  # OTP is invalid or expired


# def is_otp_expired(otp_send_time):
#     # Define expiry duration for OTP (e.g., 5 minutes)
#     expiry_duration = datetime.timedelta(minutes=5)
#     now = timezone.now()
#     return now > otp_send_time + expiry_duration

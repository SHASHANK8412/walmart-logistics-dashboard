import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from dotenv import load_dotenv
import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Load environment variables
load_dotenv()

# Initialize session state for OTPs if not exists
if 'otps' not in st.session_state:
    st.session_state.otps = {}

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def save_otp(user_id, otp, expiry_minutes=5):
    """Store OTP in session state with expiration time"""
    st.session_state.otps[user_id] = {
        'otp': otp,
        'expiry': time.time() + (expiry_minutes * 60)
    }

def verify_otp(user_id, submitted_otp):
    """Verify if submitted OTP is valid and not expired"""
    if user_id not in st.session_state.otps:
        return False, "OTP not found. Please request a new one."
    
    otp_data = st.session_state.otps[user_id]
    
    # Check if OTP is expired
    if time.time() > otp_data['expiry']:
        del st.session_state.otps[user_id]
        return False, "OTP has expired. Please request a new one."
    
    # Check if OTP matches
    if submitted_otp == otp_data['otp']:
        del st.session_state.otps[user_id]
        return True, "OTP verified successfully."
    
    return False, "Invalid OTP. Please try again."

def send_otp_email(email, otp):
    """Send OTP via email"""
    try:
        # Get email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        email_username = os.getenv("EMAIL_USERNAME", "")
        email_password = os.getenv("EMAIL_PASSWORD", "")
        
        # If email credentials are not set, simulate sending
        if not email_username or not email_password:
            st.warning("Email credentials not set. In production, configure SMTP settings.")
            return True, f"[DEVELOPMENT MODE] OTP {otp} would be sent to {email}"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = email_username
        message["To"] = email
        message["Subject"] = "Your Walmart Account Verification Code"
        
        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #0071ce;">Walmart Account Verification</h2>
                </div>
                <p>Hello,</p>
                <p>Thank you for registering with Walmart. To complete your registration, please use the following verification code:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-size: 24px; font-weight: bold; letter-spacing: 5px;">
                        {otp}
                    </div>
                </div>
                <p>This code will expire in 5 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <p>Thank you,<br>Walmart Support Team</p>
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; font-size: 12px; color: #777;">
                    &copy; 2025 Walmart Inc. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(body, "html"))
        
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_username, email_password)
        
        # Send email
        server.sendmail(email_username, email, message.as_string())
        server.quit()
        
        return True, "Verification code sent to your email."
    
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def send_otp_sms(phone_number, otp):
    """Send OTP via SMS using Twilio"""
    try:
        # Get Twilio configuration from environment variables
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER", "")
        
        # If Twilio credentials are not set, simulate sending
        if not twilio_account_sid or not twilio_auth_token or not twilio_phone_number:
            st.warning("Twilio credentials not set. In production, configure Twilio settings.")
            return True, f"[DEVELOPMENT MODE] OTP {otp} would be sent to {phone_number}"
        
        # Format phone number if needed
        if not phone_number.startswith('+'):
            phone_number = f"+{phone_number}"
        
        # Initialize Twilio client
        client = Client(twilio_account_sid, twilio_auth_token)
        
        # Send message
        message = client.messages.create(
            body=f"Your Walmart verification code is: {otp}. This code will expire in 5 minutes.",
            from_=twilio_phone_number,
            to=phone_number
        )
        
        return True, "Verification code sent to your phone."
    
    except TwilioRestException as e:
        return False, f"Failed to send SMS: {str(e)}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def send_otp(contact, otp, contact_type="email"):
    """Send OTP via specified channel (email or SMS)"""
    if contact_type.lower() == "email":
        return send_otp_email(contact, otp)
    elif contact_type.lower() == "phone":
        return send_otp_sms(contact, otp)
    else:
        return False, "Unsupported contact type. Use 'email' or 'phone'."

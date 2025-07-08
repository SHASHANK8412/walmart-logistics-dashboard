import streamlit as st
import pandas as pd
import hashlib
import json
import os
import datetime
import re
from utils.otp import generate_otp, send_otp, save_otp, verify_otp

# File paths
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

# Initialize session state for registration process
if 'registration_data' not in st.session_state:
    st.session_state.registration_data = {}
if 'registration_step' not in st.session_state:
    st.session_state.registration_step = "form"

# Initialize users data file if it doesn't exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({
            "users": [
                {
                    "username": "admin",
                    "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                    "email": "admin@walmart.com",
                    "name": "System Administrator",
                    "role": "admin",
                    "created_at": datetime.datetime.now().isoformat()
                }
            ]
        }, f, indent=4)

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {"users": []}

def save_users(users_data):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=4)

def hash_password(password):
    """Create SHA-256 hash of password"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Basic validation - can be enhanced for different country formats
    pattern = r'^\+?[0-9]{10,15}$'
    return re.match(pattern, phone) is not None

def register_user(username, password, email, name, phone=None, verified=False):
    """Register a new user"""
    users_data = load_users()
    
    # Check if username already exists
    if any(user["username"] == username for user in users_data["users"]):
        return False, "Username already exists"
    
    # Check if email already exists
    if any(user["email"] == email for user in users_data["users"]):
        return False, "Email already exists"
    
    # Check if phone already exists (if provided)
    if phone and any(user.get("phone") == phone for user in users_data["users"]):
        return False, "Phone number already exists"
    
    # Require verification unless explicitly bypassed
    if not verified:
        return False, "Account verification required"
    
    # Create new user
    new_user = {
        "username": username,
        "password_hash": hash_password(password),
        "email": email,
        "name": name,
        "role": "customer",  # Default role is customer
        "created_at": datetime.datetime.now().isoformat()
    }
    
    # Add phone if provided
    if phone:
        new_user["phone"] = phone
    
    users_data["users"].append(new_user)
    save_users(users_data)
    
    return True, "Registration successful"

def initiate_verification(username, password, email, name, phone=None, contact_type="email"):
    """Start the verification process for a new user registration"""
    # Validate email format if using email verification
    if contact_type == "email" and not validate_email(email):
        return False, "Invalid email format"
    
    # Validate phone format if using phone verification
    if contact_type == "phone":
        if not phone or not validate_phone(phone):
            return False, "Invalid phone number format"
    
    # Generate OTP
    otp = generate_otp(6)
    
    # Store registration data in session state
    st.session_state.registration_data = {
        "username": username,
        "password": password,
        "email": email,
        "name": name,
        "phone": phone,
        "contact_type": contact_type
    }
    
    # Save OTP with user email/phone as identifier
    contact = email if contact_type == "email" else phone
    save_otp(contact, otp)
    
    # Send OTP
    success, message = send_otp(contact, otp, contact_type)
    
    if success:
        st.session_state.registration_step = "verification"
        return True, message
    else:
        return False, message

def complete_registration(otp):
    """Verify OTP and complete registration"""
    if 'registration_data' not in st.session_state:
        return False, "Registration data not found. Please start over."
    
    reg_data = st.session_state.registration_data
    contact = reg_data["email"] if reg_data["contact_type"] == "email" else reg_data["phone"]
    
    # Verify OTP
    success, message = verify_otp(contact, otp)
    
    if success:
        # Register the user with verified flag
        reg_success, reg_message = register_user(
            reg_data["username"], 
            reg_data["password"], 
            reg_data["email"], 
            reg_data["name"], 
            reg_data.get("phone"),
            verified=True
        )
        
        # Reset registration state
        st.session_state.registration_step = "form"
        st.session_state.registration_data = {}
        
        return reg_success, reg_message
    else:
        return False, message

def login_user(username, password):
    """Authenticate a user"""
    users_data = load_users()
    
    for user in users_data["users"]:
        if user["username"] == username and user["password_hash"] == hash_password(password):
            return True, user
    
    return False, None

def is_authenticated():
    """Check if user is authenticated"""
    return 'user' in st.session_state and st.session_state.user is not None

def is_admin():
    """Check if current user is an admin"""
    return is_authenticated() and st.session_state.user.get('role') == 'admin'

def logout_user():
    """Log out the current user"""
    if 'user' in st.session_state:
        del st.session_state.user

def show_login_form():
    """Display login form"""
    with st.form("login_form"):
        st.markdown("### 🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if username and password:
                success, user = login_user(username, password)
                if success:
                    st.session_state.user = user
                    st.success(f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")

def show_registration_form():
    """Display registration form with OTP verification"""
    # Step 1: Registration form
    if st.session_state.registration_step == "form":
        with st.form("registration_form"):
            st.markdown("### 📝 Create an Account")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            
            # Contact method selection
            contact_method = st.radio(
                "Verification Method", 
                ["Email", "Phone"], 
                horizontal=True,
                help="Choose how you want to receive your verification code"
            )
            
            # Show phone field only if phone verification selected
            phone = None
            if contact_method == "Phone":
                phone = st.text_input(
                    "Phone Number",
                    placeholder="+1 (555) 123-4567",
                    help="Enter your phone number in international format (e.g., +1 for US)"
                )
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            password_confirm = st.text_input("Confirm Password", type="password")
            
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            submitted = st.form_submit_button("Register", use_container_width=True)
            
            if submitted:
                if not all([name, email, username, password, password_confirm]):
                    st.error("Please fill out all required fields")
                elif contact_method == "Phone" and not phone:
                    st.error("Please enter your phone number")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                elif not terms_accepted:
                    st.error("You must agree to the Terms of Service and Privacy Policy")
                else:
                    # Start verification process
                    contact_type = "email" if contact_method == "Email" else "phone"
                    success, message = initiate_verification(
                        username, password, email, name, phone, contact_type
                    )
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    # Step 2: OTP verification
    elif st.session_state.registration_step == "verification":
        reg_data = st.session_state.registration_data
        contact_type = reg_data["contact_type"]
        contact = reg_data["email"] if contact_type == "email" else reg_data["phone"]
        
        st.markdown("### 🔐 Account Verification")
        
        # Show verification info
        if contact_type == "email":
            st.info(f"We've sent a verification code to your email address: **{contact}**")
        else:
            st.info(f"We've sent a verification code to your phone number: **{contact}**")
            
        # OTP verification form
        with st.form("verification_form"):
            st.markdown("Please enter the 6-digit verification code:")
            
            # Create 6 side-by-side input boxes for OTP
            cols = st.columns(6)
            otp_digits = []
            
            for i, col in enumerate(cols):
                with col:
                    digit = st.text_input(
                        f"Digit {i+1}", 
                        max_chars=1,
                        key=f"otp_digit_{i}",
                        label_visibility="collapsed"
                    )
                    otp_digits.append(digit)
            
            # Combine digits into OTP
            otp = ''.join(otp_digits)
            
            # Form buttons
            col1, col2 = st.columns(2)
            with col1:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            with col2:
                verify = st.form_submit_button("Verify", use_container_width=True)
            
            if verify:
                if len(otp) != 6:
                    st.error("Please enter all 6 digits of the verification code")
                else:
                    # Verify OTP and complete registration
                    success, message = complete_registration(otp)
                    
                    if success:
                        st.success(message)
                        # Login the user automatically
                        login_success, user = login_user(reg_data["username"], reg_data["password"])
                        if login_success:
                            st.session_state.user = user
                            st.rerun()
                    else:
                        st.error(message)
            
            elif cancel:
                # Reset registration state
                st.session_state.registration_step = "form"
                st.session_state.registration_data = {}
                st.rerun()
        
        # Options below the form
        if st.button("Resend Code"):
            # Regenerate and send a new OTP
            otp = generate_otp(6)
            save_otp(contact, otp)
            success, message = send_otp(contact, otp, contact_type)
            
            if success:
                st.success("Verification code resent!")
            else:
                st.error(message)
                
        if st.button("Change Contact Information"):
            # Go back to the registration form
            st.session_state.registration_step = "form"
            st.session_state.registration_data = {}
            st.rerun()

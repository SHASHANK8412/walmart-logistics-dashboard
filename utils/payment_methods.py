"""
Payment Methods Module for Walmart Logistics Dashboard
Comprehensive payment processing system with multiple payment options
"""

import streamlit as st
import time
import datetime
import random
from typing import Dict, List, Tuple, Optional

class PaymentProcessor:
    """Handles all payment processing operations"""
    
    def __init__(self):
        self.supported_methods = {
            "credit_card": {
                "name": "Credit Card",
                "icon": "💳",
                "description": "Visa, MasterCard, American Express",
                "processing_fee": 0.029,  # 2.9%
                "processing_time": 1.5
            },
            "debit_card": {
                "name": "Debit Card",
                "icon": "💳",
                "description": "Bank debit cards",
                "processing_fee": 0.015,  # 1.5%
                "processing_time": 1.0
            },
            "paypal": {
                "name": "PayPal",
                "icon": "🅿️",
                "description": "PayPal account payment",
                "processing_fee": 0.035,  # 3.5%
                "processing_time": 2.0
            },
            "apple_pay": {
                "name": "Apple Pay",
                "icon": "🍎",
                "description": "Apple Pay digital wallet",
                "processing_fee": 0.025,  # 2.5%
                "processing_time": 0.8
            },
            "google_pay": {
                "name": "Google Pay",
                "icon": "🟢",
                "description": "Google Pay digital wallet",
                "processing_fee": 0.025,  # 2.5%
                "processing_time": 0.8
            },
            "bank_transfer": {
                "name": "Bank Transfer",
                "icon": "🏦",
                "description": "Direct bank account transfer",
                "processing_fee": 0.001,  # 0.1%
                "processing_time": 3.0
            },
            "cash_on_delivery": {
                "name": "Cash on Delivery",
                "icon": "💵",
                "description": "Pay when you receive your order",
                "processing_fee": 0.0,  # No fee
                "processing_time": 0.5
            },
            "walmart_card": {
                "name": "Walmart Credit Card",
                "icon": "🏪",
                "description": "Walmart branded credit card",
                "processing_fee": 0.0,  # No fee for Walmart card
                "processing_time": 1.0
            },
            "gift_card": {
                "name": "Gift Card",
                "icon": "🎁",
                "description": "Walmart gift card",
                "processing_fee": 0.0,  # No fee
                "processing_time": 0.5
            },
            "cryptocurrency": {
                "name": "Cryptocurrency",
                "icon": "₿",
                "description": "Bitcoin, Ethereum, etc.",
                "processing_fee": 0.01,  # 1%
                "processing_time": 5.0
            }
        }
    
    def get_payment_methods(self) -> Dict:
        """Get all available payment methods"""
        return self.supported_methods
    
    def calculate_processing_fee(self, amount: float, method: str) -> float:
        """Calculate processing fee for a payment method"""
        if method in self.supported_methods:
            fee_rate = self.supported_methods[method]["processing_fee"]
            return amount * fee_rate
        return 0.0
    
    def process_payment(self, amount: float, method: str, payment_details: Dict) -> Tuple[bool, str, Dict]:
        """
        Process payment with given method and details
        Returns: (success, message, transaction_details)
        """
        if method not in self.supported_methods:
            return False, "Unsupported payment method", {}
        
        method_info = self.supported_methods[method]
        processing_fee = self.calculate_processing_fee(amount, method)
        total_amount = amount + processing_fee
        
        # Simulate payment processing
        processing_time = method_info["processing_time"]
        
        # Generate transaction ID
        transaction_id = f"TXN{random.randint(100000, 999999)}"
        
        # Simulate processing delay
        time.sleep(processing_time)
        
        # Simulate success/failure (95% success rate)
        success = random.random() < 0.95
        
        if success:
            transaction_details = {
                "transaction_id": transaction_id,
                "method": method,
                "amount": amount,
                "processing_fee": processing_fee,
                "total_amount": total_amount,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed",
                "payment_details": payment_details
            }
            
            return True, f"Payment successful! Transaction ID: {transaction_id}", transaction_details
        else:
            return False, "Payment failed. Please try again or use a different payment method.", {}

def display_payment_form(cart_total: float, payment_processor: PaymentProcessor, form_id: str = "default") -> Tuple[Optional[str], Optional[Dict]]:
    """
    Display payment form and handle payment selection
    Returns: (selected_method, payment_details)
    """
    # Customer Information Section
    st.subheader("� Customer Information")
    
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Full Name *", placeholder="John Doe", key=f"payment_customer_name_{form_id}")
        customer_email = st.text_input("Email Address *", placeholder="john@example.com", key=f"payment_customer_email_{form_id}")
        customer_phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567", key=f"payment_customer_phone_{form_id}")
    
    with col2:
        billing_address = st.text_area("Billing Address *", placeholder="123 Main St\nDallas, TX 75201", key=f"payment_billing_address_{form_id}")
        delivery_same = st.checkbox("Delivery address same as billing", value=True, key=f"payment_delivery_same_{form_id}")
        
        if not delivery_same:
            delivery_address = st.text_area("Delivery Address", placeholder="456 Oak Ave\nDallas, TX 75202", key=f"payment_delivery_address_{form_id}")
        else:
            delivery_address = billing_address
    
    st.subheader("�💳 Payment Information")
    
    # Payment method selection
    payment_methods = payment_processor.get_payment_methods()
    method_options = []
    method_keys = []
    
    for key, info in payment_methods.items():
        fee = payment_processor.calculate_processing_fee(cart_total, key)
        fee_text = f" (+${fee:.2f} fee)" if fee > 0 else " (No fee)"
        method_options.append(f"{info['icon']} {info['name']} - {info['description']}{fee_text}")
        method_keys.append(key)
    
    selected_index = st.selectbox(
        "Select Payment Method:",
        range(len(method_options)),
        format_func=lambda x: method_options[x],
        help="Choose your preferred payment method",
        key=f"payment_method_select_{form_id}"
    )
    
    selected_method = method_keys[selected_index]
    method_info = payment_methods[selected_method]
    
    # Show payment method details
    processing_fee = payment_processor.calculate_processing_fee(cart_total, selected_method)
    total_with_fee = cart_total + processing_fee
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    ">
        <h4 style="margin: 0; color: #1976d2;">{method_info['icon']} {method_info['name']}</h4>
        <p style="margin: 5px 0; color: #555;">{method_info['description']}</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
            <div><strong>Subtotal:</strong> ${cart_total:.2f}</div>
            <div><strong>Processing Fee:</strong> ${processing_fee:.2f}</div>
        </div>
        <div style="text-align: center; margin-top: 10px; background: #1976d2; color: white; padding: 8px; border-radius: 6px;">
            <strong>Total Amount: ${total_with_fee:.2f}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment details form based on selected method
    payment_details = {
        "customer_name": customer_name,
        "email": customer_email,
        "phone": customer_phone,
        "billing_address": billing_address,
        "delivery_address": delivery_address
    }
    
    if selected_method == "credit_card" or selected_method == "debit_card":
        st.markdown("#### 💳 Card Details")
        
        # Card number field - full width
        card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456", max_chars=19, key=f"payment_card_number_{form_id}")
        
        # Cardholder name field - full width  
        cardholder_name = st.text_input("Cardholder Name", placeholder="John Doe", key=f"payment_cardholder_name_{form_id}")
        
        # Expiry and CVV in columns with proper spacing
        col1, col2 = st.columns([1, 1])
        with col1:
            expiry_date = st.text_input("Expiry Date", placeholder="MM/YY", max_chars=5, key=f"payment_expiry_date_{form_id}")
        with col2:
            cvv = st.text_input("CVV", placeholder="123", max_chars=4, type="password", key=f"payment_cvv_{form_id}")
        
        payment_details.update({
            "card_number": card_number[-4:] if card_number else "",  # Store only last 4 digits
            "cardholder_name": cardholder_name,
            "expiry_date": expiry_date
        })
    
    elif selected_method == "paypal":
        paypal_email = st.text_input("PayPal Email", placeholder="your@email.com", key=f"payment_paypal_email_{form_id}")
        payment_details.update({"paypal_email": paypal_email})
    
    elif selected_method == "bank_transfer":
        col1, col2 = st.columns(2)
        with col1:
            account_number = st.text_input("Account Number", placeholder="123456789", key=f"payment_account_number_{form_id}")
            routing_number = st.text_input("Routing Number", placeholder="021000021", key=f"payment_routing_number_{form_id}")
        with col2:
            account_holder = st.text_input("Account Holder", placeholder="John Doe", key=f"payment_account_holder_{form_id}")
            bank_name = st.text_input("Bank Name", placeholder="Bank of America", key=f"payment_bank_name_{form_id}")
        
        payment_details.update({
            "account_number": account_number[-4:] if account_number else "",
            "account_holder": account_holder,
            "bank_name": bank_name
        })
    
    elif selected_method == "cash_on_delivery":
        st.info("💵 You will pay in cash when your order is delivered.")
        payment_details.update({"delivery_payment": True})
    
    elif selected_method == "walmart_card":
        walmart_card_number = st.text_input("Walmart Card Number", placeholder="1234 5678 9012 3456", key=f"payment_walmart_card_{form_id}")
        payment_details.update({"walmart_card": walmart_card_number[-4:] if walmart_card_number else ""})
    
    elif selected_method == "gift_card":
        gift_card_number = st.text_input("Gift Card Number", placeholder="1234 5678 9012 3456", key=f"payment_gift_card_{form_id}")
        gift_card_pin = st.text_input("Gift Card PIN", placeholder="1234", type="password", key=f"payment_gift_card_pin_{form_id}")
        payment_details.update({"gift_card": gift_card_number[-4:] if gift_card_number else ""})
    
    elif selected_method in ["apple_pay", "google_pay"]:
        st.info(f"📱 You will be redirected to {method_info['name']} to complete your payment.")
        payment_details.update({"digital_wallet": selected_method})
    
    elif selected_method == "cryptocurrency":
        crypto_type = st.selectbox("Cryptocurrency Type", ["Bitcoin", "Ethereum", "Litecoin", "Dogecoin"], key=f"payment_crypto_type_{form_id}")
        wallet_address = st.text_input("Your Wallet Address", placeholder="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", key=f"payment_wallet_address_{form_id}")
        payment_details.update({"crypto_type": crypto_type, "wallet_address": wallet_address})
    
    # Validate required fields
    if not customer_name or not customer_email or not billing_address:
        st.warning("⚠️ Please fill in all required fields marked with *")
        return None, None
    
    return selected_method, payment_details

def display_payment_confirmation(transaction_details: Dict):
    """Display payment confirmation with transaction details"""
    st.balloons()
    
    confirmation_html = f"""
    <div style="
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #4CAF50;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        text-align: center;
    ">
        <h2 style="color: #2e7d32; margin: 0 0 20px 0;">🎉 PAYMENT SUCCESSFUL! 🎉</h2>
        
        <div style="background: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h3 style="margin: 0 0 15px 0; color: #2c3e50;">💳 Transaction Details</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left;">
                <div><strong>Transaction ID:</strong> {transaction_details['transaction_id']}</div>
                <div><strong>Payment Method:</strong> {transaction_details['method'].replace('_', ' ').title()}</div>
                <div><strong>Amount:</strong> ${transaction_details['amount']:.2f}</div>
                <div><strong>Processing Fee:</strong> ${transaction_details['processing_fee']:.2f}</div>
                <div><strong>Total Paid:</strong> ${transaction_details['total_amount']:.2f}</div>
                <div><strong>Status:</strong> ✅ {transaction_details['status'].title()}</div>
            </div>
            <div style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 8px;">
                <strong>Timestamp:</strong> {datetime.datetime.fromisoformat(transaction_details['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        
        <div style="background: #2e7d32; color: white; padding: 15px; border-radius: 8px;">
            <h3 style="margin: 0;">✅ Order Placed Successfully!</h3>
            <p style="margin: 5px 0;">Your order has been confirmed and is being processed.</p>
        </div>
    </div>
    """
    
    st.markdown(confirmation_html, unsafe_allow_html=True)

def get_payment_summary(cart_items: List[Dict], payment_method: str) -> Dict:
    """Generate payment summary for order"""
    processor = PaymentProcessor()
    
    subtotal = sum(item['quantity'] * item['price'] for item in cart_items)
    tax = subtotal * 0.085  # 8.5% tax
    processing_fee = processor.calculate_processing_fee(subtotal, payment_method)
    total = subtotal + tax + processing_fee
    
    return {
        "subtotal": subtotal,
        "tax": tax,
        "processing_fee": processing_fee,
        "total": total,
        "item_count": len(cart_items),
        "total_quantity": sum(item['quantity'] for item in cart_items)
    }

import streamlit as st
import datetime
import json
from typing import Dict, List, Optional
import base64
from io import BytesIO
import uuid

class ReceiptGenerator:
    """
    Comprehensive receipt generation system for Walmart WMS
    Handles both order bills and warehouse receipts
    """
    
    def __init__(self):
        self.company_info = {
            "name": "Walmart Supercenter",
            "address": "1234 Commerce Way, Bentonville, AR 72712",
            "phone": "(479) 273-4000",
            "email": "customerservice@walmart.com",
            "website": "www.walmart.com"
        }
    
    def generate_order_bill(self, order_data: Dict, cart_items: List[Dict] = None) -> Dict:
        """Generate a detailed bill/receipt when an order is placed"""
        try:
            # Generate unique receipt ID
            receipt_id = f"BILL-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:6].upper()}"
            
            # Calculate totals
            if cart_items:
                subtotal = sum(item['quantity'] * item['price'] for item in cart_items)
                total_items = sum(item['quantity'] for item in cart_items)
            else:
                subtotal = order_data.get('quantity', 1) * order_data.get('price', 0)
                total_items = order_data.get('quantity', 1)
            
            tax_rate = 0.085  # 8.5% tax
            tax_amount = subtotal * tax_rate
            total_amount = subtotal + tax_amount
            
            # Create receipt data
            receipt_data = {
                "receipt_id": receipt_id,
                "receipt_type": "ORDER_BILL",
                "timestamp": datetime.datetime.now().isoformat(),
                "order_id": order_data.get('order_id', f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"),
                "customer_info": {
                    "name": order_data.get('customer_name', 'Walk-in Customer'),
                    "email": order_data.get('customer_email', ''),
                    "address": order_data.get('delivery_address', '')
                },
                "items": cart_items if cart_items else [{
                    "name": order_data.get('product_name', 'Unknown Product'),
                    "quantity": order_data.get('quantity', 1),
                    "price": order_data.get('price', 0),
                    "total": order_data.get('quantity', 1) * order_data.get('price', 0)
                }],
                "financial_summary": {
                    "subtotal": subtotal,
                    "tax_rate": tax_rate,
                    "tax_amount": tax_amount,
                    "total_amount": total_amount,
                    "total_items": total_items
                },
                "payment_method": order_data.get('payment_method', 'Not specified'),
                "special_instructions": order_data.get('special_instructions', ''),
                "status": "PAID"
            }
            
            return {
                "success": True,
                "receipt_data": receipt_data,
                "receipt_html": self._generate_receipt_html(receipt_data)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate order bill: {str(e)}"
            }
    
    def generate_warehouse_receipt(self, fulfillment_data: Dict) -> Dict:
        """Generate a warehouse receipt when items are taken out for fulfillment"""
        try:
            # Generate unique receipt ID
            receipt_id = f"WH-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:6].upper()}"
            
            # Create warehouse receipt data
            receipt_data = {
                "receipt_id": receipt_id,
                "receipt_type": "WAREHOUSE_FULFILLMENT",
                "timestamp": datetime.datetime.now().isoformat(),
                "order_id": fulfillment_data.get('order_id', ''),
                "picking_id": fulfillment_data.get('picking_id', ''),
                "warehouse_info": {
                    "location": fulfillment_data.get('warehouse_location', 'Main Warehouse'),
                    "zone": fulfillment_data.get('zone', 'A1'),
                    "assigned_worker": fulfillment_data.get('assigned_worker', 'System Auto')
                },
                "customer_info": {
                    "name": fulfillment_data.get('customer_name', ''),
                    "delivery_address": fulfillment_data.get('delivery_address', '')
                },
                "items": fulfillment_data.get('items', []),
                "fulfillment_summary": {
                    "total_items": sum(item.get('quantity', 0) for item in fulfillment_data.get('items', [])),
                    "total_weight": fulfillment_data.get('total_weight', 0),
                    "packaging_type": fulfillment_data.get('packaging_type', 'Standard Box')
                },
                "delivery_info": {
                    "delivery_id": fulfillment_data.get('delivery_id', ''),
                    "agent_assigned": fulfillment_data.get('agent_assigned', ''),
                    "eta": fulfillment_data.get('eta', '')
                },
                "status": "READY_FOR_SHIPPING"
            }
            
            return {
                "success": True,
                "receipt_data": receipt_data,
                "receipt_html": self._generate_warehouse_receipt_html(receipt_data)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate warehouse receipt: {str(e)}"
            }
    
    def _generate_receipt_html(self, receipt_data: Dict) -> str:
        """Generate HTML for order bill receipt"""
        items_html = ""
        for item in receipt_data['items']:
            items_html += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{item.get('name', 'Unknown')}</td>
                <td style="padding: 8px; text-align: center; border-bottom: 1px solid #ddd;">{item.get('quantity', 1)}</td>
                <td style="padding: 8px; text-align: right; border-bottom: 1px solid #ddd;">${item.get('price', 0):.2f}</td>
                <td style="padding: 8px; text-align: right; border-bottom: 1px solid #ddd; font-weight: bold;">${item.get('quantity', 1) * item.get('price', 0):.2f}</td>
            </tr>
            """
        
        html = f"""
        <div style="
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Arial', sans-serif;
            background: white;
            border: 2px solid #0071ce;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #0071ce;">
                <h1 style="color: #0071ce; margin: 0; font-size: 28px; font-weight: bold;">🛒 WALMART</h1>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">{self.company_info['address']}</p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">{self.company_info['phone']} | {self.company_info['email']}</p>
            </div>
            
            <!-- Receipt Info -->
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h2 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 20px;">📋 ORDER RECEIPT</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
                    <div><strong>Receipt ID:</strong> {receipt_data['receipt_id']}</div>
                    <div><strong>Order ID:</strong> {receipt_data['order_id']}</div>
                    <div><strong>Date:</strong> {datetime.datetime.fromisoformat(receipt_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</div>
                    <div><strong>Payment:</strong> {receipt_data['payment_method']}</div>
                </div>
            </div>
            
            <!-- Customer Info -->
            <div style="background: #e8f4f8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;">👤 Customer Information</h3>
                <div style="font-size: 14px;">
                    <div><strong>Name:</strong> {receipt_data['customer_info']['name']}</div>
                    <div><strong>Email:</strong> {receipt_data['customer_info']['email']}</div>
                    <div><strong>Delivery Address:</strong> {receipt_data['customer_info']['address']}</div>
                </div>
            </div>
            
            <!-- Items -->
            <div style="margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 16px;">🛍️ Items Purchased</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <thead>
                        <tr style="background: #f8f9fa;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #0071ce;">Item</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #0071ce;">Qty</th>
                            <th style="padding: 10px; text-align: right; border-bottom: 2px solid #0071ce;">Price</th>
                            <th style="padding: 10px; text-align: right; border-bottom: 2px solid #0071ce;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>
            </div>
            
            <!-- Financial Summary -->
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 16px;">💰 Payment Summary</h3>
                <div style="font-size: 14px;">
                    <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                        <span>Subtotal ({receipt_data['financial_summary']['total_items']} items):</span>
                        <span>${receipt_data['financial_summary']['subtotal']:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                        <span>Tax ({receipt_data['financial_summary']['tax_rate'] * 100:.1f}%):</span>
                        <span>${receipt_data['financial_summary']['tax_amount']:.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 15px 0 5px 0; padding-top: 10px; border-top: 1px solid #ddd; font-size: 16px; font-weight: bold; color: #0071ce;">
                        <span>TOTAL PAID:</span>
                        <span>${receipt_data['financial_summary']['total_amount']:.2f}</span>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                <p style="margin: 5px 0;">Thank you for shopping with Walmart!</p>
                <p style="margin: 5px 0;">Visit us at {self.company_info['website']}</p>
                <p style="margin: 5px 0;">Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        """
        
        return html
    
    def _generate_warehouse_receipt_html(self, receipt_data: Dict) -> str:
        """Generate HTML for warehouse fulfillment receipt"""
        items_html = ""
        for item in receipt_data['items']:
            items_html += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{item.get('name', 'Unknown')}</td>
                <td style="padding: 8px; text-align: center; border-bottom: 1px solid #ddd;">{item.get('quantity', 1)}</td>
                <td style="padding: 8px; text-align: center; border-bottom: 1px solid #ddd;">{item.get('location', 'N/A')}</td>
                <td style="padding: 8px; text-align: center; border-bottom: 1px solid #ddd;">{item.get('status', 'PICKED')}</td>
            </tr>
            """
        
        html = f"""
        <div style="
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Arial', sans-serif;
            background: white;
            border: 2px solid #ff6b35;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <!-- Header -->
            <div style="text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #ff6b35;">
                <h1 style="color: #ff6b35; margin: 0; font-size: 28px; font-weight: bold;">🏪 WALMART WAREHOUSE</h1>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Fulfillment Center</p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">{self.company_info['address']}</p>
            </div>
            
            <!-- Receipt Info -->
            <div style="background: #fff2e6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h2 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 20px;">📦 WAREHOUSE FULFILLMENT RECEIPT</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
                    <div><strong>Receipt ID:</strong> {receipt_data['receipt_id']}</div>
                    <div><strong>Order ID:</strong> {receipt_data['order_id']}</div>
                    <div><strong>Picking ID:</strong> {receipt_data['picking_id']}</div>
                    <div><strong>Date:</strong> {datetime.datetime.fromisoformat(receipt_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
            </div>
            
            <!-- Warehouse Info -->
            <div style="background: #e8f4f8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;">🏪 Warehouse Information</h3>
                <div style="font-size: 14px;">
                    <div><strong>Location:</strong> {receipt_data['warehouse_info']['location']}</div>
                    <div><strong>Zone:</strong> {receipt_data['warehouse_info']['zone']}</div>
                    <div><strong>Assigned Worker:</strong> {receipt_data['warehouse_info']['assigned_worker']}</div>
                </div>
            </div>
            
            <!-- Customer Info -->
            <div style="background: #f0f9ff; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 16px;">🚚 Delivery Information</h3>
                <div style="font-size: 14px;">
                    <div><strong>Customer:</strong> {receipt_data['customer_info']['name']}</div>
                    <div><strong>Delivery Address:</strong> {receipt_data['customer_info']['delivery_address']}</div>
                    <div><strong>Delivery ID:</strong> {receipt_data['delivery_info']['delivery_id']}</div>
                    <div><strong>Agent:</strong> {receipt_data['delivery_info']['agent_assigned']}</div>
                    <div><strong>ETA:</strong> {receipt_data['delivery_info']['eta']}</div>
                </div>
            </div>
            
            <!-- Items -->
            <div style="margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 16px;">📋 Items Fulfilled</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <thead>
                        <tr style="background: #fff2e6;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ff6b35;">Item</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ff6b35;">Qty</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ff6b35;">Location</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ff6b35;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                </table>
            </div>
            
            <!-- Summary -->
            <div style="background: #fff2e6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 16px;">📊 Fulfillment Summary</h3>
                <div style="font-size: 14px;">
                    <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                        <span>Total Items:</span>
                        <span>{receipt_data['fulfillment_summary']['total_items']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                        <span>Total Weight:</span>
                        <span>{receipt_data['fulfillment_summary']['total_weight']} lbs</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                        <span>Packaging:</span>
                        <span>{receipt_data['fulfillment_summary']['packaging_type']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 15px 0 5px 0; padding-top: 10px; border-top: 1px solid #ddd; font-size: 16px; font-weight: bold; color: #ff6b35;">
                        <span>STATUS:</span>
                        <span>{receipt_data['status']}</span>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                <p style="margin: 5px 0;">Items picked and ready for shipping</p>
                <p style="margin: 5px 0;">Walmart Fulfillment Center</p>
                <p style="margin: 5px 0;">Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        """
        
        return html
    
    def display_receipt(self, receipt_html: str, receipt_data: Dict):
        """Display the receipt in Streamlit with download options"""
        st.markdown(receipt_html, unsafe_allow_html=True)
        
        # Add download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as HTML
            st.download_button(
                label="📄 Download Receipt (HTML)",
                data=receipt_html,
                file_name=f"{receipt_data['receipt_id']}.html",
                mime="text/html",
                key=f"download_html_{receipt_data['receipt_id']}"
            )
        
        with col2:
            # Download as JSON
            receipt_json = json.dumps(receipt_data, indent=2)
            st.download_button(
                label="📋 Download Receipt (JSON)",
                data=receipt_json,
                file_name=f"{receipt_data['receipt_id']}.json",
                mime="application/json",
                key=f"download_json_{receipt_data['receipt_id']}"
            )

# Global instance
receipt_generator = ReceiptGenerator()

def auto_generate_order_receipt(order_data: Dict, cart_items: List[Dict] = None) -> Dict:
    """Auto-generate receipt when order is placed"""
    return receipt_generator.generate_order_bill(order_data, cart_items)

def auto_generate_warehouse_receipt(fulfillment_data: Dict) -> Dict:
    """Auto-generate receipt when items are taken from warehouse"""
    return receipt_generator.generate_warehouse_receipt(fulfillment_data)

def display_auto_receipt(receipt_result: Dict):
    """Display automatically generated receipt"""
    if receipt_result.get('success'):
        st.success("✅ **Receipt Generated Successfully!**")
        receipt_generator.display_receipt(
            receipt_result['receipt_html'], 
            receipt_result['receipt_data']
        )
    else:
        st.error(f"❌ **Receipt Generation Failed:** {receipt_result.get('error', 'Unknown error')}")

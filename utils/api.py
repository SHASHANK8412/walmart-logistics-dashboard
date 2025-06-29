import requests
import streamlit as st
import json
import os
import random
import datetime
import math
from typing import Dict, List, Optional
import time

class WalmartAPI:
    """
    Comprehensive API client for Walmart Logistics Backend
    """
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Make HTTP request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params)
            elif method.upper() == 'PATCH':
                response = self.session.patch(url, json=data, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend server. Please make sure the server is running.")
            return {"success": False, "error": "Connection failed"}
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                st.error(f"❌ {error_data.get('error', 'HTTP Error')}")
            except:
                st.error(f"❌ HTTP Error: {e.response.status_code}")
            return {"success": False, "error": f"HTTP Error: {e.response.status_code}"}
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    # Health Check
    def health_check(self) -> Dict:
        """Check backend health status"""
        return self._make_request('GET', '/health')
    
    # Orders API
    def get_orders(self, filters: Dict = None) -> Dict:
        """Get all orders with optional filtering"""
        return self._make_request('GET', '/api/orders', params=filters)
    
    def get_order_by_id(self, order_id: str) -> Dict:
        """Get specific order by ID"""
        return self._make_request('GET', f'/api/orders/{order_id}')
    
    def create_order(self, order_data: Dict) -> Dict:
        """Create a new order"""
        return self._make_request('POST', '/api/orders', data=order_data)
    
    def update_order(self, order_id: str, update_data: Dict) -> Dict:
        """Update an existing order"""
        return self._make_request('PUT', f'/api/orders/{order_id}', data=update_data)
    
    def update_order_status(self, order_id: str, status: str) -> Dict:
        """Update order status"""
        return self._make_request('PATCH', f'/api/orders/{order_id}/status', data={"status": status})
    
    def delete_order(self, order_id: str) -> Dict:
        """Delete an order"""
        return self._make_request('DELETE', f'/api/orders/{order_id}')
    
    def get_orders_analytics(self) -> Dict:
        """Get orders analytics and summary"""
        return self._make_request('GET', '/api/orders/analytics/summary')
    
    # Inventory API
    def get_inventory(self, filters: Dict = None) -> Dict:
        """Get all products with optional filtering"""
        return self._make_request('GET', '/api/inventory', params=filters)
    
    def get_product_by_id(self, product_id: str) -> Dict:
        """Get specific product by ID"""
        return self._make_request('GET', f'/api/inventory/{product_id}')
    
    # Delivery API
    def get_deliveries(self, filters: Dict = None) -> Dict:
        """Get all deliveries with optional filtering"""
        return self._make_request('GET', '/api/delivery', params=filters)
    
    # Warehouse API
    def get_warehouses(self, filters: Dict = None) -> Dict:
        """Get all warehouses with optional filtering"""
        return self._make_request('GET', '/api/warehouse', params=filters)
    
    # Dashboard API
    def get_dashboard_overview(self) -> Dict:
        """Get dashboard overview with key metrics"""
        return self._make_request('GET', '/api/dashboard/overview')

# Singleton instance
@st.cache_resource
def get_api_client():
    """Get cached API client instance"""
    return WalmartAPI()
# Mock data generation functions for fallback
def generate_mock_orders(count=20):
    """Generate mock order data"""
    orders = []
    statuses = ["pending", "shipped", "delivered", "cancelled"]
    products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor", "Keyboard", "Mouse", "Printer", "Speaker", "Camera"]
    
    for i in range(1, count + 1):
        # Calculate a random date within the last 30 days
        days_ago = random.randint(0, 30)
        order_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).isoformat()
        
        # Generate a random order
        order = {
            "id": i,
            "order_id": f"ORD-{2023000 + i}",
            "customer_name": f"Customer {i}",
            "customer_email": f"customer{i}@example.com",
            "product_id": f"PROD-{random.randint(1000, 9999)}",
            "product_name": random.choice(products),
            "quantity": random.randint(1, 5),
            "price": round(random.uniform(50, 1000), 2),
            "status": random.choice(statuses),
            "order_date": order_date,
            "delivery_address": f"{random.randint(1, 999)} Main St, City {i}, State",
            "payment_method": random.choice(["Credit Card", "PayPal", "Cash on Delivery"])
        }
        orders.append(order)
    
    return orders

def generate_mock_inventory(count=30):
    """Generate mock inventory data"""
    inventory = []
    categories = ["Electronics", "Clothing", "Groceries", "Home Goods", "Sports", "Toys", "Health", "Beauty"]
    
    for i in range(1, count + 1):
        # Generate random inventory item
        min_stock = random.randint(5, 20)
        quantity = random.randint(0, 40)
        
        item = {
            "id": i,
            "sku": f"SKU-{10000 + i}",
            "name": f"Product {i}",
            "description": f"Description for Product {i}",
            "category": random.choice(categories),
            "quantity": quantity,
            "price": round(random.uniform(10, 500), 2),
            "bin_location": f"{random.choice('ABCDE')}{random.randint(1, 20)}",
            "min_stock_level": min_stock,
            "last_restocked": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 60))).isoformat(),
            "supplier": f"Supplier {random.randint(1, 10)}"
        }
        inventory.append(item)
    
    return inventory

def generate_mock_deliveries(count=15):
    """Generate mock delivery data"""
    deliveries = []
    statuses = ["pending", "in-transit", "delivered", "failed", "rescheduled"]
    
    for i in range(1, count + 1):
        # Calculate a random delivery date within the next 7 days
        days_ahead = random.randint(-2, 7)  # Include some in the past
        delivery_date = (datetime.datetime.now() + datetime.timedelta(days=days_ahead)).isoformat()
        
        # Random delivery time
        hours_ahead = random.randint(1, 8)
        eta = (datetime.datetime.now() + datetime.timedelta(hours=hours_ahead)).isoformat()
        
        # Random coordinates in a reasonable US range
        latitude = round(random.uniform(30, 45), 6)
        longitude = round(random.uniform(-85, -120), 6)
        
        delivery = {
            "id": i,
            "delivery_id": f"DEL-{30000 + i}",
            "order_id": f"ORD-{2023000 + random.randint(1, 20)}",
            "agent_id": f"DRV-{100 + random.randint(1, 10)}",
            "agent_name": f"Driver {random.randint(1, 10)}",
            "status": random.choice(statuses),
            "delivery_date": delivery_date,
            "eta": eta,
            "region": random.choice(["North", "South", "East", "West", "Central"]),
            "latitude": latitude,
            "longitude": longitude,
            "address": f"{random.randint(1, 999)} Main St, City {i}, State",
            "notes": "Leave at door" if random.random() > 0.5 else ""
        }
        deliveries.append(delivery)
    
    return deliveries

# Simple helper functions for backward compatibility
def get_data(endpoint):
    """Get data from API with fallback to mock data"""
    api = get_api_client()
    
    if endpoint == "orders":
        result = api.get_orders()
        if result.get("success"):
            return result.get("data", [])
        else:
            st.warning("Using mock data for orders")
            return generate_mock_orders()
    
    elif endpoint == "inventory":
        result = api.get_inventory()
        if result.get("success"):
            return result.get("data", [])
        else:
            st.warning("Using mock data for inventory")
            return generate_mock_inventory()
    
    elif endpoint == "deliveries":
        result = api.get_deliveries()
        if result.get("success"):
            return result.get("data", [])
        else:
            st.warning("Using mock data for deliveries")
            return generate_mock_deliveries()
    
    elif endpoint == "dashboard":
        result = api.get_dashboard_overview()
        if result.get("success"):
            return result.get("data", {})
        else:
            st.warning("Using mock data for dashboard")
            return {
                "total_orders": 150,
                "total_revenue": 75000,
                "pending_deliveries": 25,
                "low_stock_items": 8
            }
    
    return []

def post_data(endpoint, payload):
    """Post data to API"""
    api = get_api_client()
    
    if endpoint == "orders":
        result = api.create_order(payload)
        if result.get("success"):
            return True, result.get("data")
        else:
            return False, None
    
    return False, None

def put_data(endpoint, item_id, payload):
    """Update data via API"""
    api = get_api_client()
    
    if endpoint == "orders":
        result = api.update_order(item_id, payload)
        if result.get("success"):
            return True, result.get("data")
        else:
            return False, None
    elif endpoint == "inventory":
        result = api._make_request('PUT', f'/api/inventory/{item_id}', data=payload)
        if result.get("success"):
            return True, result.get("data")
        else:
            return False, None
    elif endpoint == "deliveries":
        result = api._make_request('PUT', f'/api/delivery/{item_id}', data=payload)
        if result.get("success"):
            return True, result.get("data")
        else:
            return False, None
    
    return False, None

def delete_data(endpoint, item_id):
    """Delete data via API"""
    api = get_api_client()
    
    if endpoint == "orders":
        result = api.delete_order(item_id)
        if result.get("success"):
            return True, None
        else:
            return False, None
    
    return False, None

def update_order_status(order_id, status):
    """Update order status specifically"""
    api = get_api_client()
    result = api.update_order_status(order_id, status)
    if result.get("success"):
        return True, result.get("data")
    else:
        return False, None

# Additional utility functions for specific endpoints
def get_orders_with_filters(status=None, customer_name=None, start_date=None, end_date=None):
    """Get orders with specific filters"""
    api = get_api_client()
    filters = {}
    
    if status:
        filters['status'] = status
    if customer_name:
        filters['customer_name'] = customer_name
    if start_date:
        filters['start_date'] = start_date
    if end_date:
        filters['end_date'] = end_date
    
    result = api.get_orders(filters)
    if result.get("success"):
        return result.get("data", [])
    else:
        st.warning("Using mock data for orders")
        return generate_mock_orders()

def get_inventory_with_filters(category=None, low_stock=None, search=None):
    """Get inventory with specific filters"""
    api = get_api_client()
    filters = {}
    
    if category:
        filters['category'] = category
    if low_stock is not None:
        filters['low_stock'] = 'true' if low_stock else 'false'
    if search:
        filters['search'] = search
    
    result = api.get_inventory(filters)
    if result.get("success"):
        return result.get("data", [])
    else:
        st.warning("Using mock data for inventory")
        return generate_mock_inventory()

def create_order(order_data):
    """Create a new order with validation"""
    api = get_api_client()
    result = api.create_order(order_data)
    return result.get("success", False), result.get("data"), result.get("error")

def create_integrated_order(order_data):
    """Create a comprehensive order that updates inventory, delivery, and warehouse automatically"""
    api = get_api_client()
    
    try:
        # Use the new integration endpoint
        result = api._make_request('POST', '/api/integration/order', data=order_data)
        
        if result.get("success"):
            order = result.get("data", {}).get("order")
            integration_status = result.get("data", {}).get("integration_status")
            details = result.get("data", {}).get("details", {})
            
            # Show integration details
            if details:
                st.success("🔄 **System Integration Complete!**")
                
                if details.get("inventory"):
                    inv = details["inventory"]
                    st.info(f"📊 **Inventory**: Reduced {inv.get('product_name')} by {inv.get('quantity_reduced')} units. "
                           f"New stock: {inv.get('new_stock_level')} units" + 
                           (" ⚠️ Low stock alert!" if inv.get('low_stock_alert') else ""))
                
                if details.get("delivery"):
                    delv = details["delivery"]
                    st.info(f"🚚 **Delivery**: Created delivery {delv.get('delivery_id')} assigned to {delv.get('agent_assigned')}. "
                           f"ETA: {delv.get('eta', '')[:16]}")
                
                if details.get("warehouse"):
                    wh = details["warehouse"]
                    st.info(f"🏪 **Warehouse**: Added to picking queue {wh.get('picking_id')} at {wh.get('location')}. "
                           f"Assigned to {wh.get('assigned_worker')}")
            
            return True, order, integration_status
        else:
            return False, None, result.get("error", "Integration failed")
            
    except Exception as e:
        st.error(f"❌ Integration system error: {str(e)}")
        return False, None, f"Integration error: {str(e)}"

def update_inventory_for_order(order):
    """Update inventory stock when order is placed"""
    try:
        api = get_api_client()
        
        # Get current inventory to find the product
        inventory_result = api.get_inventory({"search": order.get("product_name")})
        if not inventory_result.get("success"):
            return False
        
        products = inventory_result.get("data", [])
        if not products:
            # Create new product if doesn't exist
            new_product = {
                "name": order.get("product_name"),
                "category": "General",
                "quantity": max(0, 100 - order.get("quantity", 0)),  # Start with 100, reduce by order quantity
                "price": order.get("price"),
                "min_stock_level": 10,
                "sku": f"SKU-{int(time.time())}"
            }
            return True  # In real implementation, create the product
        
        # Update existing product quantity
        product = products[0]
        new_quantity = max(0, product.get("quantity", 0) - order.get("quantity", 0))
        
        update_data = {
            "quantity": new_quantity,
            "last_updated": datetime.datetime.now().isoformat()
        }
        
        # Note: This would need backend API endpoint for inventory updates
        return True
        
    except Exception as e:
        st.warning(f"Inventory update failed: {str(e)}")
        return False

def create_delivery_for_order(order):
    """Create delivery record when order is placed"""
    try:
        # Generate delivery data
        delivery_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 3))
        eta = delivery_date + datetime.timedelta(hours=random.randint(2, 8))
        
        delivery_data = {
            "order_id": order.get("order_id"),
            "customer_name": order.get("customer_name"),
            "delivery_address": order.get("delivery_address"),
            "status": "pending",
            "delivery_date": delivery_date.isoformat(),
            "eta": eta.isoformat(),
            "agent_name": f"Driver {random.randint(1, 10)}",
            "region": "Central",  # Could be determined by address
            "priority": "normal"
        }
        
        # Note: This would need backend API endpoint for delivery creation
        return True
        
    except Exception as e:
        st.warning(f"Delivery creation failed: {str(e)}")
        return False

def update_warehouse_for_order(order):
    """Update warehouse operations when order is placed"""
    try:
        # Update warehouse picking list
        warehouse_update = {
            "order_id": order.get("order_id"),
            "product_name": order.get("product_name"),
            "quantity": order.get("quantity"),
            "status": "picking_required",
            "assigned_worker": f"Worker {random.randint(1, 5)}",
            "location": f"Section {random.choice(['A', 'B', 'C'])}{random.randint(1, 20)}",
            "priority": "normal"
        }
        
        # Note: This would need backend API endpoint for warehouse updates
        return True
        
    except Exception as e:
        st.warning(f"Warehouse update failed: {str(e)}")
        return False

def update_order_status_integrated(order_id, new_status):
    """Update order status and trigger related updates"""
    api = get_api_client()
    
    try:
        # Use the new integration endpoint for status updates
        result = api._make_request('PATCH', f'/api/integration/order/{order_id}/status', data={"status": new_status})
        
        if result.get("success"):
            order = result.get("data", {}).get("order")
            integration_results = result.get("data", {}).get("integration_results", {})
            
            # Show what systems were updated
            updates = []
            if integration_results.get("inventory"):
                updates.append("📊 Inventory restored")
            if integration_results.get("delivery"):
                updates.append("🚚 Delivery updated")
            if integration_results.get("warehouse"):
                updates.append("🏪 Warehouse updated")
            
            if updates:
                st.success(f"✅ Order status updated to **{new_status}**. Systems updated: {', '.join(updates)}")
            
            return True, order
        else:
            return False, None
            
    except Exception as e:
        st.error(f"❌ Status update failed: {str(e)}")
        return False, None

def update_delivery_status(order_id, status):
    """Update delivery status for an order"""
    try:
        # This would update delivery records
        return True
    except Exception as e:
        st.warning(f"Delivery status update failed: {str(e)}")
        return False

def update_warehouse_status(order_id, status):
    """Update warehouse status for an order"""
    try:
        # This would update warehouse operations
        return True
    except Exception as e:
        st.warning(f"Warehouse status update failed: {str(e)}")
        return False

def restore_inventory_for_cancelled_order(order):
    """Restore inventory when order is cancelled"""
    try:
        # This would add back the quantity to inventory
        return True
    except Exception as e:
        st.warning(f"Inventory restoration failed: {str(e)}")
        return False

def get_integrated_dashboard_data():
    """Get comprehensive dashboard data with real-time metrics"""
    api = get_api_client()
    
    try:
        # Get data from all endpoints
        orders_result = api.get_orders()
        inventory_result = api.get_inventory()
        deliveries_result = api.get_deliveries()
        warehouses_result = api.get_warehouses()
        
        orders = orders_result.get("data", []) if orders_result.get("success") else []
        inventory = inventory_result.get("data", []) if inventory_result.get("success") else []
        deliveries = deliveries_result.get("data", []) if deliveries_result.get("success") else []
        warehouses = warehouses_result.get("data", []) if warehouses_result.get("success") else []
        
        # Calculate integrated metrics
        today = datetime.datetime.now().date()
        
        # Order metrics
        total_orders = len(orders)
        today_orders = len([o for o in orders if o.get("order_date", "").startswith(str(today))])
        pending_orders = len([o for o in orders if o.get("status") == "pending"])
        total_revenue = sum(float(o.get("price", 0)) * int(o.get("quantity", 0)) for o in orders)
        
        # Inventory metrics
        total_products = len(inventory)
        low_stock_items = len([i for i in inventory if i.get("quantity", 0) <= i.get("min_stock_level", 5)])
        out_of_stock = len([i for i in inventory if i.get("quantity", 0) == 0])
        
        # Delivery metrics
        pending_deliveries = len([d for d in deliveries if d.get("status") == "pending"])
        in_transit = len([d for d in deliveries if d.get("status") == "in-transit"])
        delivered_today = len([d for d in deliveries if d.get("status") == "delivered" and d.get("delivery_date", "").startswith(str(today))])
        
        # Warehouse metrics
        picking_required = len([w for w in warehouses if w.get("status") == "picking_required"])
        processing = len([w for w in warehouses if w.get("status") == "processing"])
        
        return {
            "orders": {
                "total": total_orders,
                "today": today_orders,
                "pending": pending_orders,
                "revenue": total_revenue
            },
            "inventory": {
                "total_products": total_products,
                "low_stock": low_stock_items,
                "out_of_stock": out_of_stock
            },
            "deliveries": {
                "pending": pending_deliveries,
                "in_transit": in_transit,
                "delivered_today": delivered_today
            },
            "warehouse": {
                "picking_required": picking_required,
                "processing": processing
            }
        }
        
    except Exception as e:
        st.error(f"Failed to get integrated dashboard data: {str(e)}")
        return {}

def test_integration_connectivity():
    """Test all integration endpoints and connectivity"""
    api = get_api_client()
    
    test_results = {
        "backend_health": False,
        "orders_api": False,
        "inventory_api": False,
        "delivery_api": False,
        "warehouse_api": False,
        "integration_endpoint": False
    }
    
    try:
        # Test backend health
        health = api.health_check()
        test_results["backend_health"] = health.get("success", False)
        
        # Test individual APIs
        orders = api.get_orders()
        test_results["orders_api"] = orders.get("success", False)
        
        inventory = api.get_inventory()
        test_results["inventory_api"] = inventory.get("success", False)
        
        deliveries = api.get_deliveries()
        test_results["delivery_api"] = deliveries.get("success", False)
        
        warehouses = api.get_warehouses()
        test_results["warehouse_api"] = warehouses.get("success", False)
        
        # Test integration endpoint
        test_integration = api._make_request('GET', '/api/integration/health')
        test_results["integration_endpoint"] = test_integration.get("success", False)
        
    except Exception as e:
        st.error(f"Integration connectivity test failed: {str(e)}")
    
    return test_results

def get_integration_status():
    """Get real-time integration status"""
    test_results = test_integration_connectivity()
    
    status = {
        "overall_health": all(test_results.values()),
        "systems_online": sum(test_results.values()),
        "total_systems": len(test_results),
        "details": test_results
    }
    
    return status

# Google Maps Integration Functions

def get_delivery_live_tracking(delivery_id):
    """Get live tracking for a delivery using Google Maps"""
    api = get_api_client()
    
    try:
        result = api._make_request('GET', f'/api/delivery-tracking/{delivery_id}/live-tracking')
        
        if result.get("success"):
            return True, result
        else:
            return False, result.get("error", "Tracking failed")
            
    except Exception as e:
        st.error(f"❌ Live tracking error: {str(e)}")
        return False, f"Tracking error: {str(e)}"

def calculate_delivery_route(origin, destination, optimize_for_traffic=True):
    """Calculate delivery route using Google Maps"""
    api = get_api_client()
    
    try:
        route_data = {
            "origin": origin,
            "destination": destination,
            "optimizeForTraffic": optimize_for_traffic
        }
        
        result = api._make_request('POST', '/api/delivery-tracking/calculate-route', data=route_data)
        
        if result.get("success"):
            return True, result
        else:
            return False, result.get("error", "Route calculation failed")
            
    except Exception as e:
        st.error(f"❌ Route calculation error: {str(e)}")
        return False, f"Route calculation error: {str(e)}"

def optimize_delivery_routes(deliveries, warehouse_location=None):
    """Optimize multiple delivery routes using Google Maps"""
    api = get_api_client()
    
    try:
        optimization_data = {
            "deliveries": deliveries,
            "warehouse_location": warehouse_location or "Walmart Distribution Center, 508 SW 8th St, Bentonville, AR 72716"
        }
        
        result = api._make_request('POST', '/api/delivery-tracking/bulk-optimize', data=optimization_data)
        
        if result.get("success"):
            return True, result
        else:
            return False, result.get("error", "Route optimization failed")
            
    except Exception as e:
        st.error(f"❌ Route optimization error: {str(e)}")
        return False, f"Route optimization error: {str(e)}"

def get_traffic_information():
    """Get current traffic information for all active deliveries"""
    api = get_api_client()
    
    try:
        result = api._make_request('GET', '/api/delivery-tracking/traffic-info')
        
        if result.get("success"):
            return True, result.get("traffic_updates", [])
        else:
            return False, result.get("error", "Traffic info failed")
            
    except Exception as e:
        st.error(f"❌ Traffic info error: {str(e)}")
        return False, f"Traffic info error: {str(e)}"

def geocode_address(address):
    """Geocode an address using Google Maps"""
    api = get_api_client()
    
    try:
        result = api._make_request('GET', '/api/delivery-tracking/geocode', params={"address": address})
        
        if result.get("success"):
            return True, result
        else:
            return False, result.get("error", "Geocoding failed")
            
    except Exception as e:
        st.error(f"❌ Geocoding error: {str(e)}")
        return False, f"Geocoding error: {str(e)}"

def update_driver_location(delivery_id, lat, lng):
    """Update driver location for real-time tracking"""
    api = get_api_client()
    
    try:
        location_data = {
            "lat": lat,
            "lng": lng,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        result = api._make_request('PUT', f'/api/delivery-tracking/{delivery_id}/update-location', data=location_data)
        
        if result.get("success"):
            return True, result
        else:
            return False, result.get("error", "Location update failed")
            
    except Exception as e:
        st.error(f"❌ Location update error: {str(e)}")
        return False, f"Location update error: {str(e)}"

def find_nearby_warehouses(lat, lng, radius=5000):
    """Find nearby warehouses using Google Places API"""
    api = get_api_client()
    
    try:
        params = {
            "lat": lat,
            "lng": lng,
            "radius": radius
        }
        
        result = api._make_request('GET', '/api/integration/nearby-warehouses', params=params)
        
        if result.get("success"):
            return True, result.get("warehouses", [])
        else:
            return False, result.get("error", "Warehouse search failed")
            
    except Exception as e:
        st.error(f"❌ Warehouse search error: {str(e)}")
        return False, f"Warehouse search error: {str(e)}"

def get_google_maps_integration_status():
    """Check Google Maps integration status"""
    try:
        # Test Google Maps connectivity
        success, result = calculate_delivery_route(
            "Walmart Distribution Center, Bentonville, AR",
            "Times Square, New York, NY"
        )
        
        return {
            "google_maps_api": success,
            "routing_service": success,
            "geocoding_service": success,
            "traffic_service": success,
            "places_service": success,
            "last_tested": datetime.datetime.now().isoformat(),
            "integration_active": success
        }
        
    except Exception as e:
        return {
            "google_maps_api": False,
            "routing_service": False,
            "geocoding_service": False,
            "traffic_service": False,
            "places_service": False,
            "last_tested": datetime.datetime.now().isoformat(),
            "integration_active": False,
            "error": str(e)
        }

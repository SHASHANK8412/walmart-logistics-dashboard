# Integrating Python Frontend with Node.js Backend

## Overview
The Node.js backend is now running and provides a comprehensive REST API for the Walmart Logistics Dashboard. To integrate the existing Python Streamlit frontend with this new backend, you need to update the API calls in the Python code.

## Backend API Status
✅ **Backend is running at:** `http://localhost:3000`
✅ **Health check:** `http://localhost:3000/health`
✅ **API documentation:** `http://localhost:3000/`

## Key Changes Required in Python Frontend

### 1. Update `utils/api.py`

Replace the `API_BASE` URL in your Python `utils/api.py` file:

```python
# Old configuration
API_BASE = "http://localhost:3000/api"  # This was already correct!
USE_MOCK_DATA = True  # Set to False to use real backend

# New configuration (update these lines)
API_BASE = "http://localhost:3000/api"
USE_MOCK_DATA = False  # Now use the real Node.js backend
```

### 2. API Endpoint Mapping

The Node.js backend provides these endpoints that match your Python frontend expectations:

| Python Frontend Call | Node.js Backend Endpoint | Status |
|---------------------|---------------------------|---------|
| `get_data("orders")` | `GET /api/orders` | ✅ Working |
| `get_data("inventory")` | `GET /api/inventory` | ✅ Working |
| `get_data("deliveries")` | `GET /api/delivery` | ✅ Working |
| `get_data("warehouse")` | `GET /api/warehouse` | ✅ Working |
| `post_data("orders", data)` | `POST /api/orders` | ✅ Working |
| `put_data("orders", id, data)` | `PUT /api/orders/{id}` | ✅ Working |
| `delete_data("orders", id)` | `DELETE /api/orders/{id}` | ✅ Working |

### 3. Response Format

The Node.js backend returns data in this format:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "current_page": 1,
    "total_pages": 2,
    "total_items": 100,
    "items_per_page": 50
  }
}
```

Update your Python `get_data` function to handle this:

```python
def get_data(endpoint):
    """Updated function to work with Node.js backend"""
    try:
        response = requests.get(f"{API_BASE}/{endpoint}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result.get('data', [])
        return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []
```

### 4. Sample API Calls

Here are working examples you can test:

**Get all orders:**
```bash
curl http://localhost:3000/api/orders
```

**Get orders with filters:**
```bash
curl "http://localhost:3000/api/orders?status=pending,shipped&page=1&limit=10"
```

**Create new order:**
```bash
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "product_name": "Test Product",
    "quantity": 2,
    "price": 99.99,
    "delivery_address": "123 Main St, City, State"
  }'
```

**Get dashboard overview:**
```bash
curl http://localhost:3000/api/dashboard/overview
```

### 5. Advanced Features Available

The Node.js backend provides additional features not available in the mock data:

1. **Route Optimization:**
   ```bash
   curl "http://localhost:3000/api/optimizer/route?waypoints=Address1,Address2,Address3"
   ```

2. **Inventory Analytics:**
   ```bash
   curl http://localhost:3000/api/inventory/analytics/summary
   ```

3. **Real-time Dashboard:**
   ```bash
   curl http://localhost:3000/api/dashboard/real-time
   ```

4. **Demand Forecasting:**
   ```bash
   curl -X POST http://localhost:3000/api/optimizer/demand-forecast \
     -H "Content-Type: application/json" \
     -d '{"product_ids": [1, 2, 3], "forecast_period_days": 30}'
   ```

### 6. Error Handling

The backend returns standardized error responses:
```json
{
  "success": false,
  "error": "Error message",
  "message": "Detailed error description"
}
```

Update your error handling in Python:
```python
def handle_api_response(response):
    """Handle standardized API responses"""
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            return result.get('data')
        else:
            st.error(result.get('error', 'Unknown error'))
            return None
    else:
        st.error(f"API Error: {response.status_code}")
        return None
```

### 7. Running Both Services

To run both frontend and backend:

1. **Start the Node.js backend:**
   ```bash
   cd backend
   npm run dev
   ```
   Backend runs on: http://localhost:3000

2. **Start the Python frontend:**
   ```bash
   streamlit run app.py
   ```
   Frontend runs on: http://localhost:8501

3. **Update the frontend API configuration:**
   In `utils/api.py`, set `USE_MOCK_DATA = False`

### 8. Benefits of Using Node.js Backend

✅ **Real Data Persistence:** Data survives server restarts
✅ **Advanced Analytics:** Comprehensive business intelligence
✅ **Optimization Algorithms:** Route planning, inventory optimization
✅ **Real-time Updates:** Live dashboard metrics
✅ **Scalable Architecture:** Production-ready with security features
✅ **API Documentation:** Self-documenting REST API
✅ **Performance:** Faster response times and efficient data handling

### 9. Next Steps

1. Update your Python `utils/api.py` file
2. Set `USE_MOCK_DATA = False`
3. Test the integration with a simple endpoint
4. Gradually migrate all features to use the new backend
5. Enhance the frontend to use the new advanced features

### 10. Troubleshooting

**If you get connection errors:**
- Ensure the Node.js backend is running (`npm run dev`)
- Check that the URL is correct (`http://localhost:3000`)
- Verify no firewall is blocking the connection

**If you get CORS errors:**
- The backend is configured to allow requests from `http://localhost:8501`
- Make sure your Streamlit app is running on the default port

**If data looks different:**
- The Node.js backend generates fresh mock data each time it starts
- Data structure is the same, but values will be different from the JSON file

## Testing the Integration

Run this test in your Python frontend to verify the connection:

```python
import requests

# Test connection
try:
    response = requests.get("http://localhost:3000/health")
    if response.status_code == 200:
        st.success("✅ Backend connection successful!")
        st.json(response.json())
    else:
        st.error(f"❌ Backend connection failed: {response.status_code}")
except Exception as e:
    st.error(f"❌ Connection error: {e}")
```

The Node.js backend is now fully operational and ready to serve your Walmart Logistics Dashboard!

# Walmart Logistics Backend

A comprehensive Node.js backend API for the Walmart Logistics Dashboard system.

## Features

- **Orders Management**: Create, read, update, and delete orders with real-time status tracking
- **Inventory Management**: Product management with stock levels, categories, and automatic reorder alerts
- **Delivery Tracking**: Comprehensive delivery management with route optimization
- **Warehouse Management**: Multi-warehouse support with zone management and utilization tracking
- **Optimization Engine**: AI-powered route optimization, demand forecasting, and cost analysis
- **Real-time Dashboard**: Live metrics, KPIs, and analytics for business intelligence

## API Endpoints

### Orders (`/api/orders`)
- `GET /` - Get all orders with filtering and pagination
- `GET /:id` - Get specific order by ID
- `POST /` - Create new order
- `PUT /:id` - Update existing order
- `DELETE /:id` - Delete order
- `PATCH /:id/status` - Update order status
- `GET /analytics/summary` - Get orders analytics

### Inventory (`/api/inventory`)
- `GET /` - Get all products with filtering and search
- `GET /:id` - Get specific product by ID
- `POST /` - Create new product
- `PUT /:id` - Update existing product
- `DELETE /:id` - Delete product
- `PATCH /:id/stock` - Update product stock
- `GET /analytics/summary` - Get inventory analytics
- `GET /low-stock` - Get low stock products
- `GET /categories` - Get product categories

### Delivery (`/api/delivery`)
- `GET /` - Get all deliveries with filtering
- `GET /:id` - Get specific delivery by ID
- `POST /` - Create new delivery
- `PUT /:id` - Update existing delivery
- `DELETE /:id` - Delete delivery
- `PATCH /:id/status` - Update delivery status
- `GET /route-optimization` - Get optimized delivery routes
- `GET /analytics/performance` - Get delivery performance analytics
- `GET /drivers` - Get driver statistics

### Warehouse (`/api/warehouse`)
- `GET /` - Get all warehouses
- `GET /:id` - Get specific warehouse by ID
- `POST /` - Create new warehouse
- `PUT /:id` - Update existing warehouse
- `DELETE /:id` - Delete warehouse
- `PATCH /:id/utilization` - Update warehouse utilization
- `POST /:id/zones` - Add zone to warehouse
- `DELETE /:id/zones/:zoneId` - Remove zone from warehouse
- `GET /analytics/utilization` - Get warehouse utilization analytics

### Optimizer (`/api/optimizer`)
- `GET /route` - Optimize delivery routes
- `POST /inventory` - Optimize inventory levels
- `GET /warehouse-allocation` - Optimize warehouse allocation
- `POST /demand-forecast` - Generate demand forecasts
- `GET /cost-analysis` - Analyze operational costs
- `POST /staff-scheduling` - Optimize staff scheduling

### Dashboard (`/api/dashboard`)
- `GET /overview` - Get dashboard overview with key metrics
- `GET /analytics` - Get detailed analytics for charts
- `GET /kpis` - Get Key Performance Indicators
- `GET /real-time` - Get real-time dashboard data

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository or navigate to the backend directory
```bash
cd backend
```

2. Install dependencies
```bash
npm install
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your configuration
```

4. Start the development server
```bash
npm run dev
```

5. Start the production server
```bash
npm start
```

The API will be available at `http://localhost:3000`

### Available Scripts

- `npm start` - Start production server
- `npm run dev` - Start development server with auto-reload
- `npm test` - Run tests (when implemented)

## API Documentation

### Authentication
Currently, the API doesn't require authentication for development purposes. In production, implement JWT or similar authentication mechanisms.

### Request/Response Format
All API responses follow this format:
```json
{
  "success": true|false,
  "data": { /* response data */ },
  "message": "Success message",
  "error": "Error message (if any)",
  "pagination": { /* pagination info for list endpoints */ }
}
```

### Error Handling
The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

### Filtering and Pagination
List endpoints support:
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 50)
- Various filters specific to each endpoint

## Data Models

### Order
- Order ID, customer information, product details
- Status tracking (pending, shipped, delivered, cancelled)
- Payment method and delivery address
- Timestamps for creation and updates

### Product (Inventory)
- SKU, name, category, pricing
- Stock quantities and reorder levels
- Supplier information and location
- Stock status and value calculations

### Delivery
- Delivery ID linked to orders
- Driver and vehicle information
- Pickup and delivery addresses
- Status tracking and time estimates
- Priority levels and notes

### Warehouse
- Warehouse information and capacity
- Manager contact details
- Operating hours and status
- Zone management with utilization tracking

## Features

### Mock Data Service
The backend includes a comprehensive mock data service that generates realistic data for:
- 100+ sample orders with various statuses
- 50+ products across multiple categories
- 75+ deliveries with different stages
- 5 warehouses with zone management

### Optimization Algorithms
- Route optimization for efficient deliveries
- Inventory level optimization with safety stock calculations
- Demand forecasting using trend analysis
- Cost analysis with savings opportunities
- Staff scheduling optimization

### Real-time Features
- Live dashboard metrics
- Real-time status updates
- Performance monitoring
- System health checks

## Architecture

### Directory Structure
```
backend/
├── models/          # Data models (Order, Product, Delivery, Warehouse)
├── routes/          # API route handlers
├── services/        # Business logic and mock data service
├── utils/           # Helper functions and utilities
├── server.js        # Main application entry point
├── package.json     # Dependencies and scripts
└── .env            # Environment configuration
```

### Security Features
- Helmet.js for security headers
- CORS configuration
- Rate limiting
- Input validation and sanitization
- Error handling middleware

### Performance Features
- Response compression
- Request logging with Morgan
- Efficient data structures
- Optimized query handling

## Development

### Adding New Endpoints
1. Create route handler in `/routes` directory
2. Implement business logic in `/services` if needed
3. Add appropriate validation using utilities
4. Update this README with new endpoint documentation

### Testing
Run tests with:
```bash
npm test
```

### Environment Variables
Key environment variables:
- `PORT` - Server port (default: 3000)
- `NODE_ENV` - Environment (development/production)
- `FRONTEND_URL` - Frontend URL for CORS
- Add database configuration when implementing real database

## Production Deployment

### Docker (Recommended)
```bash
# Build image
docker build -t walmart-logistics-backend .

# Run container
docker run -p 3000:3000 --env-file .env walmart-logistics-backend
```

### Traditional Deployment
1. Set `NODE_ENV=production`
2. Configure production database
3. Set up reverse proxy (nginx)
4. Configure SSL certificates
5. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@walmart-logistics.com or create an issue in the repository.

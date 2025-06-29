const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

// Database connection
const { connectDB } = require('./config/database');

// Import routes
const ordersRoutes = require('./routes/orders');
const inventoryRoutes = require('./routes/inventory');
const deliveryRoutes = require('./routes/delivery');
const warehouseRoutes = require('./routes/warehouse');
const optimizerRoutes = require('./routes/optimizer');
const dashboardRoutes = require('./routes/dashboard');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

// Middleware
app.use(compression());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:8501', // Streamlit default port
  credentials: true
}));
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: process.env.npm_package_version || '1.0.0'
  });
});

// API routes
app.use('/api/orders', ordersRoutes);
app.use('/api/inventory', inventoryRoutes);
app.use('/api/delivery', deliveryRoutes);
app.use('/api/warehouse', warehouseRoutes);
app.use('/api/optimizer', optimizerRoutes);
app.use('/api/dashboard', dashboardRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Walmart Logistics Backend API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      orders: '/api/orders',
      inventory: '/api/inventory',
      delivery: '/api/delivery',
      warehouse: '/api/warehouse',
      optimizer: '/api/optimizer',
      dashboard: '/api/dashboard'
    }
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.originalUrl,
    method: req.method
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});

// Start server and connect to database
const startServer = async () => {
  try {
    // Connect to database (MongoDB or fallback to mock data)
    await connectDB();
    
    // Start server
    app.listen(PORT, () => {
      console.log(`🚀 Walmart Logistics Backend running on port ${PORT}`);
      console.log(`📊 Health check: http://localhost:${PORT}/health`);
      console.log(`📋 API docs: http://localhost:${PORT}/`);
      console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
};

startServer();

module.exports = app;

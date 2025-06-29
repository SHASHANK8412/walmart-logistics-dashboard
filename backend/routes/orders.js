const express = require('express');
const router = express.Router();
const databaseService = require('../services/databaseService');
const Order = require('../models/Order');
const { Validator } = require('../utils/helpers');

/**
 * GET /api/orders
 * Get all orders with optional filtering
 */
router.get('/', async (req, res) => {
  try {
    const { status, start_date, end_date, customer_name, page = 1, limit = 50 } = req.query;
    
    const filters = {};
    
    if (status) {
      const statusArray = Array.isArray(status) ? status : status.split(',');
      filters.status = statusArray;
    }
    
    if (start_date && end_date) {
      filters.startDate = start_date;
      filters.endDate = end_date;
    }
    
    if (customer_name) {
      filters.customer_name = customer_name;
    }
    
    const orders = await databaseService.getOrders(filters);
    
    // Pagination
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    const paginatedOrders = orders.slice(startIndex, endIndex);
    
    res.json({
      success: true,
      data: paginatedOrders,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(orders.length / limit),
        total_items: orders.length,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch orders',
      message: error.message
    });
  }
});

/**
 * GET /api/orders/:id
 * Get a specific order by ID
 */
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const order = await databaseService.getOrderById(id);
    
    if (!order) {
      return res.status(404).json({
        success: false,
        error: 'Order not found'
      });
    }
    
    res.json({
      success: true,
      data: order
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch order',
      message: error.message
    });
  }
});

/**
 * POST /api/orders
 * Create a new order
 */
router.post('/', async (req, res) => {
  try {
    const orderData = req.body;
    
    // Validate required fields
    const requiredFields = ['customer_name', 'customer_email', 'product_name', 'quantity', 'price', 'delivery_address'];
    const missingFields = Validator.validateRequired(orderData, requiredFields);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        missing_fields: missingFields
      });
    }
    
    // Validate email format
    if (!Validator.isValidEmail(orderData.customer_email)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email format'
      });
    }
    
    // Validate quantity and price
    if (!Validator.isPositiveNumber(orderData.quantity) || !Validator.isPositiveNumber(orderData.price)) {
      return res.status(400).json({
        success: false,
        error: 'Quantity and price must be positive numbers'
      });
    }
    
    // Create new order
    const orderData_clean = {
      customer_name: Validator.sanitizeString(orderData.customer_name),
      customer_email: orderData.customer_email.toLowerCase(),
      product_name: Validator.sanitizeString(orderData.product_name),
      quantity: parseInt(orderData.quantity),
      price: parseFloat(orderData.price),
      delivery_address: Validator.sanitizeString(orderData.delivery_address),
      payment_method: orderData.payment_method || 'Credit Card'
    };
    
    const newOrder = await databaseService.createOrder(orderData_clean);
    
    res.status(201).json({
      success: true,
      message: 'Order created successfully',
      data: newOrder
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to create order',
      message: error.message
    });
  }
});

/**
 * PUT /api/orders/:id/**
 * PUT /api/orders/:id
 * Update an existing order
 */
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updateData = req.body;
    
    // Validate allowed fields and prepare update data
    const allowedUpdates = {};
    
    if (updateData.status && Order.getValidStatuses().includes(updateData.status)) {
      allowedUpdates.status = updateData.status;
    }
    
    if (updateData.delivery_address) {
      allowedUpdates.delivery_address = Validator.sanitizeString(updateData.delivery_address);
    }
    
    if (updateData.quantity && Validator.isPositiveNumber(updateData.quantity)) {
      allowedUpdates.quantity = parseInt(updateData.quantity);
    }
    
    if (Object.keys(allowedUpdates).length === 0) {
      return res.status(400).json({
        success: false,
        error: 'No valid fields to update'
      });
    }
    
    const updatedOrder = await databaseService.updateOrder(id, allowedUpdates);
    
    if (!updatedOrder) {
      return res.status(404).json({
        success: false,
        error: 'Order not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Order updated successfully',
      data: updatedOrder
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update order',
      message: error.message
    });
  }
});

/**
 * DELETE /api/orders/:id
 * Delete an order
 */
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const deleted = await databaseService.deleteOrder(id);
    
    if (!deleted) {
      return res.status(404).json({
        success: false,
        error: 'Order not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Order deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to delete order',
      message: error.message
    });
  }
});

/**
 * GET /api/orders/analytics/summary
 * Get orders analytics and summary
 */
router.get('/analytics/summary', async (req, res) => {
  try {
    const analytics = await databaseService.getOrdersAnalytics();
    
    res.json({
      success: true,
      data: analytics
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch analytics',
      message: error.message
    });
  }
});

/**
 * PATCH /api/orders/:id/status
 * Update order status
 */
router.patch('/:id/status', async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;
    
    if (!status) {
      return res.status(400).json({
        success: false,
        error: 'Status is required'
      });
    }
    
    if (!Order.getValidStatuses().includes(status)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid status',
        valid_statuses: Order.getValidStatuses()
      });
    }
    
    const updatedOrder = await databaseService.updateOrder(id, { status });
    
    if (!updatedOrder) {
      return res.status(404).json({
        success: false,
        error: 'Order not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Order status updated successfully',
      data: updatedOrder
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update order status',
      message: error.message
    });
  }
});

module.exports = router;

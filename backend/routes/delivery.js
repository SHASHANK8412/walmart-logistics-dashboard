const express = require('express');
const router = express.Router();
const databaseService = require('../services/databaseService');
const Delivery = require('../models/Delivery');
const { Validator, Calculator } = require('../utils/helpers');

/**
 * GET /api/delivery
 * Get all deliveries with optional filtering
 */
router.get('/', async (req, res) => {
  try {
    const { status, driver_name, priority, page = 1, limit = 50 } = req.query;
    
    const filters = {};
    
    if (status) {
      const statusArray = Array.isArray(status) ? status : status.split(',');
      filters.status = statusArray;
    }
    
    if (driver_name) {
      filters.driver_name = driver_name;
    }
    
    if (priority) {
      filters.priority = priority;
    }

    console.log('Getting deliveries with filters:', filters);
    let deliveries = await databaseService.getDeliveries(filters);
    
    // Pagination
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    const paginatedDeliveries = deliveries.slice(startIndex, endIndex);
    
    res.json({
      success: true,
      data: paginatedDeliveries,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(deliveries.length / limit),
        total_items: deliveries.length,
        items_per_page: parseInt(limit)
      }
    });
  } catch (error) {
    console.error('Delivery route error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch deliveries',
      message: error.message
    });
  }
});

/**
 * GET /api/delivery/:id
 * Get a specific delivery by ID
 */
router.get('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const delivery = mockDataService.getDeliveryById(id);
    
    if (!delivery) {
      return res.status(404).json({
        success: false,
        error: 'Delivery not found'
      });
    }
    
    res.json({
      success: true,
      data: delivery
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch delivery',
      message: error.message
    });
  }
});

/**
 * POST /api/delivery
 * Create a new delivery
 */
router.post('/', (req, res) => {
  try {
    const deliveryData = req.body;
    
    // Validate required fields
    const requiredFields = ['order_id', 'driver_name', 'vehicle_id', 'pickup_address', 'delivery_address'];
    const missingFields = Validator.validateRequired(deliveryData, requiredFields);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        missing_fields: missingFields
      });
    }
    
    // Validate priority if provided
    if (deliveryData.priority && !Delivery.getPriorityLevels().includes(deliveryData.priority)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid priority level',
        valid_priorities: Delivery.getPriorityLevels()
      });
    }
    
    // Create new delivery
    const delivery = new Delivery({
      order_id: Validator.sanitizeString(deliveryData.order_id),
      driver_name: Validator.sanitizeString(deliveryData.driver_name),
      vehicle_id: Validator.sanitizeString(deliveryData.vehicle_id),
      pickup_address: Validator.sanitizeString(deliveryData.pickup_address),
      delivery_address: Validator.sanitizeString(deliveryData.delivery_address),
      estimated_delivery_time: deliveryData.estimated_delivery_time ? new Date(deliveryData.estimated_delivery_time) : null,
      priority: deliveryData.priority || 'normal',
      notes: Validator.sanitizeString(deliveryData.notes) || ''
    });
    
    // Add to mock data
    mockDataService.deliveries.push(delivery);
    
    res.status(201).json({
      success: true,
      message: 'Delivery created successfully',
      data: delivery.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to create delivery',
      message: error.message
    });
  }
});

/**
 * PUT /api/delivery/:id
 * Update an existing delivery
 */
router.put('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const updateData = req.body;
    
    const deliveryIndex = mockDataService.deliveries.findIndex(d => d.id == id);
    
    if (deliveryIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Delivery not found'
      });
    }
    
    const delivery = mockDataService.deliveries[deliveryIndex];
    
    // Update allowed fields
    if (updateData.driver_name) {
      delivery.driver_name = Validator.sanitizeString(updateData.driver_name);
      delivery.updated_at = new Date();
    }
    
    if (updateData.vehicle_id) {
      delivery.vehicle_id = Validator.sanitizeString(updateData.vehicle_id);
      delivery.updated_at = new Date();
    }
    
    if (updateData.estimated_delivery_time) {
      delivery.estimated_delivery_time = new Date(updateData.estimated_delivery_time);
      delivery.updated_at = new Date();
    }
    
    if (updateData.priority && Delivery.getPriorityLevels().includes(updateData.priority)) {
      delivery.priority = updateData.priority;
      delivery.updated_at = new Date();
    }
    
    if (updateData.notes !== undefined) {
      delivery.notes = Validator.sanitizeString(updateData.notes);
      delivery.updated_at = new Date();
    }
    
    res.json({
      success: true,
      message: 'Delivery updated successfully',
      data: delivery.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update delivery',
      message: error.message
    });
  }
});

/**
 * PATCH /api/delivery/:id/status
 * Update delivery status
 */
router.patch('/:id/status', (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;
    
    if (!status) {
      return res.status(400).json({
        success: false,
        error: 'Status is required'
      });
    }
    
    const deliveryIndex = mockDataService.deliveries.findIndex(d => d.id == id);
    
    if (deliveryIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Delivery not found'
      });
    }
    
    const delivery = mockDataService.deliveries[deliveryIndex];
    const updated = delivery.updateStatus(status);
    
    if (!updated) {
      return res.status(400).json({
        success: false,
        error: 'Invalid status',
        valid_statuses: Delivery.getValidStatuses()
      });
    }
    
    res.json({
      success: true,
      message: 'Delivery status updated successfully',
      data: delivery.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update delivery status',
      message: error.message
    });
  }
});

/**
 * DELETE /api/delivery/:id
 * Delete a delivery
 */
router.delete('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const deliveryIndex = mockDataService.deliveries.findIndex(d => d.id == id);
    
    if (deliveryIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Delivery not found'
      });
    }
    
    mockDataService.deliveries.splice(deliveryIndex, 1);
    
    res.json({
      success: true,
      message: 'Delivery deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to delete delivery',
      message: error.message
    });
  }
});

/**
 * GET /api/delivery/route-optimization
 * Get optimized delivery route
 */
router.get('/route-optimization', (req, res) => {
  try {
    const { deliveries: deliveryIds, start_location } = req.query;
    
    if (!deliveryIds) {
      return res.status(400).json({
        success: false,
        error: 'Delivery IDs are required'
      });
    }
    
    const ids = Array.isArray(deliveryIds) ? deliveryIds : deliveryIds.split(',');
    const deliveries = ids.map(id => mockDataService.getDeliveryById(id)).filter(Boolean);
    
    if (deliveries.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'No valid deliveries found'
      });
    }
    
    // Simple route optimization (in a real system, you'd use Google Maps API or similar)
    const optimizedRoute = {
      total_distance: Math.random() * 100 + 20, // km
      estimated_time: Math.random() * 180 + 60, // minutes
      fuel_cost: Math.random() * 50 + 20,
      waypoints: deliveries.map((delivery, index) => ({
        order: index + 1,
        delivery_id: delivery.delivery_id,
        address: delivery.delivery_address,
        estimated_arrival: new Date(Date.now() + (index + 1) * 30 * 60000), // 30 min intervals
        priority: delivery.priority
      })),
      start_location: start_location || 'Walmart Distribution Center',
      recommendations: [
        'Deliver high priority items first',
        'Consider traffic conditions during route execution',
        'Verify delivery addresses before departure'
      ]
    };
    
    res.json({
      success: true,
      data: optimizedRoute
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to optimize route',
      message: error.message
    });
  }
});

/**
 * GET /api/delivery/analytics/performance
 * Get delivery performance analytics
 */
router.get('/analytics/performance', (req, res) => {
  try {
    const deliveries = mockDataService.getDeliveries();
    
    const totalDeliveries = deliveries.length;
    const completedDeliveries = deliveries.filter(d => d.status === 'delivered');
    const pendingDeliveries = deliveries.filter(d => d.status === 'pending');
    const inTransitDeliveries = deliveries.filter(d => d.status === 'in_transit');
    const failedDeliveries = deliveries.filter(d => d.status === 'failed');
    
    // Calculate average delivery time for completed deliveries
    const deliveryTimes = completedDeliveries
      .map(d => d.delivery_time_minutes)
      .filter(time => time !== null);
    
    const avgDeliveryTime = deliveryTimes.length > 0 
      ? deliveryTimes.reduce((sum, time) => sum + time, 0) / deliveryTimes.length
      : 0;
    
    // On-time delivery rate (mock calculation)
    const onTimeDeliveries = Math.floor(completedDeliveries.length * 0.85); // 85% on-time rate
    const onTimeRate = completedDeliveries.length > 0 
      ? (onTimeDeliveries / completedDeliveries.length * 100).toFixed(2)
      : 0;
    
    const analytics = {
      total_deliveries: totalDeliveries,
      completed_deliveries: completedDeliveries.length,
      pending_deliveries: pendingDeliveries.length,
      in_transit_deliveries: inTransitDeliveries.length,
      failed_deliveries: failedDeliveries.length,
      success_rate: totalDeliveries > 0 ? ((completedDeliveries.length / totalDeliveries) * 100).toFixed(2) : 0,
      average_delivery_time_minutes: avgDeliveryTime.toFixed(0),
      on_time_delivery_rate: onTimeRate,
      performance_metrics: {
        efficiency_score: Math.floor(Math.random() * 20 + 80), // 80-100%
        customer_satisfaction: Math.floor(Math.random() * 10 + 90) / 10, // 9.0-10.0
        cost_per_delivery: (Math.random() * 10 + 15).toFixed(2) // $15-25
      }
    };
    
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
 * GET /api/delivery/drivers
 * Get list of available drivers
 */
router.get('/drivers', (req, res) => {
  try {
    const deliveries = mockDataService.getDeliveries();
    const drivers = [...new Set(deliveries.map(d => d.driver_name))];
    
    const driverStats = drivers.map(driver => {
      const driverDeliveries = deliveries.filter(d => d.driver_name === driver);
      const completed = driverDeliveries.filter(d => d.status === 'delivered').length;
      
      return {
        name: driver,
        total_deliveries: driverDeliveries.length,
        completed_deliveries: completed,
        current_status: driverDeliveries.some(d => d.status === 'in_transit') ? 'on_route' : 'available',
        success_rate: driverDeliveries.length > 0 ? ((completed / driverDeliveries.length) * 100).toFixed(2) : 0
      };
    });
    
    res.json({
      success: true,
      data: driverStats
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch drivers',
      message: error.message
    });
  }
});

module.exports = router;

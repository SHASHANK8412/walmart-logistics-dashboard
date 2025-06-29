const express = require('express');
const router = express.Router();
const databaseService = require('../services/databaseService');
const Warehouse = require('../models/Warehouse');
const { Validator } = require('../utils/helpers');

/**
 * GET /api/warehouse
 * Get all warehouses
 */
router.get('/', async (req, res) => {
  try {
    const warehouses = await databaseService.getWarehouses();
    
    res.json({
      success: true,
      data: warehouses,
      count: warehouses.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch warehouses',
      message: error.message
    });
  }
});

/**
 * GET /api/warehouse/:id
 * Get a specific warehouse by ID
 */
router.get('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const warehouse = mockDataService.getWarehouseById(id);
    
    if (!warehouse) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    res.json({
      success: true,
      data: warehouse
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch warehouse',
      message: error.message
    });
  }
});

/**
 * POST /api/warehouse
 * Create a new warehouse
 */
router.post('/', (req, res) => {
  try {
    const warehouseData = req.body;
    
    // Validate required fields
    const requiredFields = ['name', 'location', 'capacity', 'manager_name'];
    const missingFields = Validator.validateRequired(warehouseData, requiredFields);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        missing_fields: missingFields
      });
    }
    
    // Validate numeric fields
    if (!Validator.isPositiveNumber(warehouseData.capacity)) {
      return res.status(400).json({
        success: false,
        error: 'Capacity must be a positive number'
      });
    }
    
    // Validate email if provided
    if (warehouseData.email && !Validator.isValidEmail(warehouseData.email)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email format'
      });
    }
    
    // Validate phone if provided
    if (warehouseData.phone && !Validator.isValidPhone(warehouseData.phone)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid phone format'
      });
    }
    
    // Create new warehouse
    const warehouse = new Warehouse({
      name: Validator.sanitizeString(warehouseData.name),
      location: Validator.sanitizeString(warehouseData.location),
      capacity: parseInt(warehouseData.capacity),
      current_utilization: parseInt(warehouseData.current_utilization) || 0,
      manager_name: Validator.sanitizeString(warehouseData.manager_name),
      phone: warehouseData.phone || '',
      email: warehouseData.email || '',
      operating_hours: warehouseData.operating_hours || { start: '08:00', end: '18:00' }
    });
    
    // Add to mock data
    mockDataService.warehouses.push(warehouse);
    
    res.status(201).json({
      success: true,
      message: 'Warehouse created successfully',
      data: warehouse.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to create warehouse',
      message: error.message
    });
  }
});

/**
 * PUT /api/warehouse/:id
 * Update an existing warehouse
 */
router.put('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const updateData = req.body;
    
    const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
    
    if (warehouseIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    const warehouse = mockDataService.warehouses[warehouseIndex];
    
    // Update allowed fields
    if (updateData.name) {
      warehouse.name = Validator.sanitizeString(updateData.name);
      warehouse.updated_at = new Date();
    }
    
    if (updateData.location) {
      warehouse.location = Validator.sanitizeString(updateData.location);
      warehouse.updated_at = new Date();
    }
    
    if (updateData.capacity && Validator.isPositiveNumber(updateData.capacity)) {
      warehouse.capacity = parseInt(updateData.capacity);
      warehouse.updated_at = new Date();
    }
    
    if (updateData.manager_name) {
      warehouse.manager_name = Validator.sanitizeString(updateData.manager_name);
      warehouse.updated_at = new Date();
    }
    
    if (updateData.phone !== undefined) {
      if (updateData.phone && !Validator.isValidPhone(updateData.phone)) {
        return res.status(400).json({
          success: false,
          error: 'Invalid phone format'
        });
      }
      warehouse.phone = updateData.phone;
      warehouse.updated_at = new Date();
    }
    
    if (updateData.email !== undefined) {
      if (updateData.email && !Validator.isValidEmail(updateData.email)) {
        return res.status(400).json({
          success: false,
          error: 'Invalid email format'
        });
      }
      warehouse.email = updateData.email;
      warehouse.updated_at = new Date();
    }
    
    if (updateData.operating_hours) {
      warehouse.operating_hours = updateData.operating_hours;
      warehouse.updated_at = new Date();
    }
    
    if (updateData.status && Warehouse.getValidStatuses().includes(updateData.status)) {
      warehouse.status = updateData.status;
      warehouse.updated_at = new Date();
    }
    
    res.json({
      success: true,
      message: 'Warehouse updated successfully',
      data: warehouse.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update warehouse',
      message: error.message
    });
  }
});

/**
 * PATCH /api/warehouse/:id/utilization
 * Update warehouse utilization
 */
router.patch('/:id/utilization', (req, res) => {
  try {
    const { id } = req.params;
    const { utilization } = req.body;
    
    if (utilization === undefined || !Validator.isNonNegativeNumber(utilization)) {
      return res.status(400).json({
        success: false,
        error: 'Valid utilization value is required'
      });
    }
    
    const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
    
    if (warehouseIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    const warehouse = mockDataService.warehouses[warehouseIndex];
    const updated = warehouse.updateUtilization(parseInt(utilization));
    
    if (!updated) {
      return res.status(400).json({
        success: false,
        error: 'Utilization cannot exceed warehouse capacity',
        capacity: warehouse.capacity
      });
    }
    
    res.json({
      success: true,
      message: 'Warehouse utilization updated successfully',
      data: {
        warehouse_id: warehouse.warehouse_id,
        name: warehouse.name,
        capacity: warehouse.capacity,
        current_utilization: warehouse.current_utilization,
        utilization_percentage: warehouse.getUtilizationPercentage(),
        available_capacity: warehouse.getAvailableCapacity()
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update utilization',
      message: error.message
    });
  }
});

/**
 * POST /api/warehouse/:id/zones
 * Add a zone to a warehouse
 */
router.post('/:id/zones', (req, res) => {
  try {
    const { id } = req.params;
    const zoneData = req.body;
    
    // Validate required fields
    const requiredFields = ['name', 'capacity'];
    const missingFields = Validator.validateRequired(zoneData, requiredFields);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        missing_fields: missingFields
      });
    }
    
    if (!Validator.isPositiveNumber(zoneData.capacity)) {
      return res.status(400).json({
        success: false,
        error: 'Zone capacity must be a positive number'
      });
    }
    
    const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
    
    if (warehouseIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    const warehouse = mockDataService.warehouses[warehouseIndex];
    
    // Validate zone type if provided
    if (zoneData.type && !Warehouse.getZoneTypes().includes(zoneData.type)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid zone type',
        valid_types: Warehouse.getZoneTypes()
      });
    }
    
    warehouse.addZone({
      name: Validator.sanitizeString(zoneData.name),
      type: zoneData.type || 'general',
      capacity: parseInt(zoneData.capacity),
      current_stock: parseInt(zoneData.current_stock) || 0,
      temperature_controlled: Boolean(zoneData.temperature_controlled)
    });
    
    res.status(201).json({
      success: true,
      message: 'Zone added successfully',
      data: warehouse.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to add zone',
      message: error.message
    });
  }
});

/**
 * DELETE /api/warehouse/:id/zones/:zoneId
 * Remove a zone from a warehouse
 */
router.delete('/:id/zones/:zoneId', (req, res) => {
  try {
    const { id, zoneId } = req.params;
    
    const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
    
    if (warehouseIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    const warehouse = mockDataService.warehouses[warehouseIndex];
    const zoneExists = warehouse.zones.some(zone => zone.id == zoneId);
    
    if (!zoneExists) {
      return res.status(404).json({
        success: false,
        error: 'Zone not found'
      });
    }
    
    warehouse.removeZone(parseInt(zoneId));
    
    res.json({
      success: true,
      message: 'Zone removed successfully',
      data: warehouse.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to remove zone',
      message: error.message
    });
  }
});

/**
 * GET /api/warehouse/analytics/utilization
 * Get warehouse utilization analytics
 */
router.get('/analytics/utilization', (req, res) => {
  try {
    const warehouses = mockDataService.getWarehouses();
    
    const totalCapacity = warehouses.reduce((sum, w) => sum + w.capacity, 0);
    const totalUtilization = warehouses.reduce((sum, w) => sum + w.current_utilization, 0);
    const overallUtilization = totalCapacity > 0 ? ((totalUtilization / totalCapacity) * 100).toFixed(2) : 0;
    
    const warehouseUtilization = warehouses.map(w => ({
      warehouse_id: w.warehouse_id,
      name: w.name,
      location: w.location,
      utilization_percentage: w.utilization_percentage,
      is_near_capacity: w.is_near_capacity,
      available_capacity: w.available_capacity,
      status: w.status
    }));
    
    const nearCapacityCount = warehouses.filter(w => w.is_near_capacity).length;
    
    const analytics = {
      total_warehouses: warehouses.length,
      total_capacity: totalCapacity,
      total_utilization: totalUtilization,
      overall_utilization_percentage: overallUtilization,
      warehouses_near_capacity: nearCapacityCount,
      warehouse_utilization: warehouseUtilization,
      recommendations: [
        nearCapacityCount > 0 ? 'Consider redistributing inventory from near-capacity warehouses' : null,
        overallUtilization > 85 ? 'Overall utilization is high - consider expanding capacity' : null,
        'Monitor seasonal demand patterns for optimal capacity planning'
      ].filter(Boolean)
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
 * DELETE /api/warehouse/:id
 * Delete a warehouse
 */
router.delete('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
    
    if (warehouseIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    mockDataService.warehouses.splice(warehouseIndex, 1);
    
    res.json({
      success: true,
      message: 'Warehouse deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to delete warehouse',
      message: error.message
    });
  }
});

module.exports = router;

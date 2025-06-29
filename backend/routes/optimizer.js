const express = require('express');
const router = express.Router();
const mockDataService = require('../services/mockDataService');
const { Calculator } = require('../utils/helpers');

// Initialize mock data
mockDataService.initialize();

/**
 * GET /api/optimizer/route
 * Optimize delivery route for multiple destinations
 */
router.get('/route', (req, res) => {
  try {
    const { waypoints, start_location, vehicle_type = 'van', optimization_type = 'time' } = req.query;
    
    if (!waypoints) {
      return res.status(400).json({
        success: false,
        error: 'Waypoints are required for route optimization'
      });
    }
    
    const waypointList = Array.isArray(waypoints) ? waypoints : waypoints.split(',');
    
    if (waypointList.length < 2) {
      return res.status(400).json({
        success: false,
        error: 'At least 2 waypoints are required'
      });
    }
    
    // Mock route optimization algorithm
    const optimizedRoute = generateOptimizedRoute(waypointList, start_location, vehicle_type, optimization_type);
    
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
 * POST /api/optimizer/inventory
 * Optimize inventory levels and suggest reorder points
 */
router.post('/inventory', (req, res) => {
  try {
    const { demand_history, lead_time_days = 7, service_level = 95 } = req.body;
    
    if (!demand_history || !Array.isArray(demand_history)) {
      return res.status(400).json({
        success: false,
        error: 'Demand history array is required'
      });
    }
    
    const products = mockDataService.getProducts();
    const inventoryOptimization = generateInventoryOptimization(products, demand_history, lead_time_days, service_level);
    
    res.json({
      success: true,
      data: inventoryOptimization
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to optimize inventory',
      message: error.message
    });
  }
});

/**
 * GET /api/optimizer/warehouse-allocation
 * Optimize product allocation across warehouses
 */
router.get('/warehouse-allocation', (req, res) => {
  try {
    const { product_id, demand_by_region } = req.query;
    
    if (!product_id) {
      return res.status(400).json({
        success: false,
        error: 'Product ID is required'
      });
    }
    
    const warehouses = mockDataService.getWarehouses();
    const product = mockDataService.getProductById(product_id);
    
    if (!product) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }
    
    const allocationOptimization = generateWarehouseAllocation(product, warehouses, demand_by_region);
    
    res.json({
      success: true,
      data: allocationOptimization
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to optimize warehouse allocation',
      message: error.message
    });
  }
});

/**
 * POST /api/optimizer/demand-forecast
 * Generate demand forecast for products
 */
router.post('/demand-forecast', (req, res) => {
  try {
    const { product_ids, forecast_period_days = 30, seasonality_factor = 1.0 } = req.body;
    
    if (!product_ids || !Array.isArray(product_ids)) {
      return res.status(400).json({
        success: false,
        error: 'Product IDs array is required'
      });
    }
    
    const demandForecast = generateDemandForecast(product_ids, forecast_period_days, seasonality_factor);
    
    res.json({
      success: true,
      data: demandForecast
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to generate demand forecast',
      message: error.message
    });
  }
});

/**
 * GET /api/optimizer/cost-analysis
 * Analyze and optimize operational costs
 */
router.get('/cost-analysis', (req, res) => {
  try {
    const { analysis_type = 'all', time_period = 30 } = req.query;
    
    const costAnalysis = generateCostAnalysis(analysis_type, time_period);
    
    res.json({
      success: true,
      data: costAnalysis
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to analyze costs',
      message: error.message
    });
  }
});

/**
 * POST /api/optimizer/staff-scheduling
 * Optimize staff scheduling for warehouses
 */
router.post('/staff-scheduling', (req, res) => {
  try {
    const { warehouse_id, shift_requirements, staff_availability } = req.body;
    
    if (!warehouse_id) {
      return res.status(400).json({
        success: false,
        error: 'Warehouse ID is required'
      });
    }
    
    const warehouse = mockDataService.getWarehouseById(warehouse_id);
    
    if (!warehouse) {
      return res.status(404).json({
        success: false,
        error: 'Warehouse not found'
      });
    }
    
    const staffSchedule = generateStaffSchedule(warehouse, shift_requirements, staff_availability);
    
    res.json({
      success: true,
      data: staffSchedule
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to optimize staff scheduling',
      message: error.message
    });
  }
});

// Helper functions for optimization algorithms

function generateOptimizedRoute(waypoints, startLocation, vehicleType, optimizationType) {
  // Mock optimization - in real scenario, would use Google Maps API or OR-Tools
  const baseDistance = waypoints.length * (10 + Math.random() * 20); // km
  const baseTime = waypoints.length * (15 + Math.random() * 30); // minutes
  
  const vehicleMultipliers = {
    'van': { speed: 1.0, fuel: 1.0, capacity: 1000 },
    'truck': { speed: 0.8, fuel: 1.5, capacity: 5000 },
    'bike': { speed: 0.4, fuel: 0.1, capacity: 50 }
  };
  
  const vehicle = vehicleMultipliers[vehicleType] || vehicleMultipliers.van;
  
  const optimizedWaypoints = waypoints.map((waypoint, index) => ({
    order: index + 1,
    address: waypoint,
    estimated_arrival_time: new Date(Date.now() + (index + 1) * baseTime * 60000 / waypoints.length),
    distance_from_previous: index === 0 ? 0 : (baseDistance / waypoints.length).toFixed(2),
    estimated_duration_minutes: Math.round(baseTime / waypoints.length)
  }));
  
  return {
    optimization_type: optimizationType,
    vehicle_type: vehicleType,
    start_location: startLocation || 'Walmart Distribution Center',
    total_distance_km: baseDistance.toFixed(2),
    total_time_minutes: Math.round(baseTime / vehicle.speed),
    estimated_fuel_cost: (baseDistance * vehicle.fuel * 0.15).toFixed(2), // $0.15 per km base
    vehicle_capacity_kg: vehicle.capacity,
    waypoints: optimizedWaypoints,
    optimization_savings: {
      distance_saved_km: (Math.random() * 5 + 2).toFixed(2),
      time_saved_minutes: Math.round(Math.random() * 30 + 10),
      fuel_cost_saved: (Math.random() * 10 + 5).toFixed(2)
    },
    recommendations: [
      'Start early to avoid traffic congestion',
      'Carry GPS device for real-time navigation',
      'Verify delivery addresses before departure',
      optimizationType === 'fuel' ? 'Maintain steady speed for fuel efficiency' : 'Take highway routes for faster delivery'
    ]
  };
}

function generateInventoryOptimization(products, demandHistory, leadTimeDays, serviceLevel) {
  const optimizedProducts = products.slice(0, 20).map(product => {
    // Mock demand calculation
    const avgDailyDemand = Math.random() * 10 + 5;
    const demandVariability = Math.random() * 0.3 + 0.1;
    
    const safetyStock = Math.ceil(avgDailyDemand * Math.sqrt(leadTimeDays) * (serviceLevel / 100));
    const reorderPoint = Calculator.calculateReorderPoint(avgDailyDemand, leadTimeDays, safetyStock);
    const economicOrderQuantity = Math.ceil(Math.sqrt((2 * avgDailyDemand * 365 * 50) / (product.cost * 0.2))); // EOQ formula
    
    const currentStatus = product.stock_quantity <= reorderPoint ? 'reorder_needed' : 
                         product.stock_quantity <= product.reorder_level ? 'low_stock' : 'optimal';
    
    return {
      product_id: product.id,
      sku: product.sku,
      name: product.name,
      current_stock: product.stock_quantity,
      current_reorder_level: product.reorder_level,
      optimized_reorder_point: reorderPoint,
      recommended_order_quantity: economicOrderQuantity,
      safety_stock: safetyStock,
      average_daily_demand: avgDailyDemand.toFixed(2),
      lead_time_days: leadTimeDays,
      status: currentStatus,
      cost_impact: {
        holding_cost_annual: (product.stock_quantity * product.cost * 0.2).toFixed(2),
        stockout_risk_percentage: currentStatus === 'reorder_needed' ? (Math.random() * 20 + 10).toFixed(1) : '0.0'
      }
    };
  });
  
  const totalHoldingCost = optimizedProducts.reduce((sum, p) => sum + parseFloat(p.cost_impact.holding_cost_annual), 0);
  const reorderNeeded = optimizedProducts.filter(p => p.status === 'reorder_needed').length;
  
  return {
    summary: {
      total_products_analyzed: optimizedProducts.length,
      products_needing_reorder: reorderNeeded,
      total_annual_holding_cost: totalHoldingCost.toFixed(2),
      service_level_target: `${serviceLevel}%`,
      average_lead_time_days: leadTimeDays
    },
    optimized_products: optimizedProducts,
    recommendations: [
      reorderNeeded > 0 ? `${reorderNeeded} products need immediate reordering` : 'All products have adequate stock levels',
      'Review demand patterns monthly for accuracy',
      'Consider vendor-managed inventory for high-volume items',
      'Implement automated reorder alerts'
    ]
  };
}

function generateWarehouseAllocation(product, warehouses, demandByRegion) {
  const allocations = warehouses.map(warehouse => {
    const regionDemand = Math.random() * 1000 + 100; // Mock regional demand
    const allocationPercentage = (regionDemand / (warehouses.length * 500)) * 100;
    const recommendedStock = Math.ceil(regionDemand * 0.3); // 30% buffer
    
    return {
      warehouse_id: warehouse.warehouse_id,
      warehouse_name: warehouse.name,
      location: warehouse.location,
      current_capacity: warehouse.capacity,
      available_capacity: warehouse.available_capacity,
      regional_demand: regionDemand.toFixed(0),
      recommended_allocation: recommendedStock,
      allocation_percentage: Math.min(allocationPercentage, 100).toFixed(2),
      distance_to_demand_center: (Math.random() * 500 + 50).toFixed(0), // km
      transportation_cost_per_unit: (Math.random() * 5 + 2).toFixed(2)
    };
  });
  
  const totalDemand = allocations.reduce((sum, a) => sum + parseFloat(a.regional_demand), 0);
  const totalRecommendedStock = allocations.reduce((sum, a) => sum + a.recommended_allocation, 0);
  
  return {
    product: {
      id: product.id,
      sku: product.sku,
      name: product.name,
      current_total_stock: product.stock_quantity
    },
    allocation_analysis: {
      total_demand: totalDemand.toFixed(0),
      total_recommended_stock: totalRecommendedStock,
      current_vs_recommended: product.stock_quantity >= totalRecommendedStock ? 'adequate' : 'insufficient',
      shortage_amount: Math.max(0, totalRecommendedStock - product.stock_quantity)
    },
    warehouse_allocations: allocations,
    optimization_benefits: {
      reduced_transportation_cost: (Math.random() * 1000 + 500).toFixed(2),
      improved_delivery_time: (Math.random() * 24 + 12).toFixed(0) + ' hours',
      inventory_turnover_improvement: (Math.random() * 20 + 10).toFixed(1) + '%'
    },
    recommendations: [
      'Prioritize allocation to warehouses closest to demand centers',
      'Consider seasonal demand variations',
      'Monitor transportation costs vs. inventory holding costs',
      'Implement cross-docking for high-velocity items'
    ]
  };
}

function generateDemandForecast(productIds, forecastPeriodDays, seasonalityFactor) {
  const forecasts = productIds.slice(0, 10).map(productId => {
    const product = mockDataService.getProductById(productId);
    if (!product) return null;
    
    const baseDemand = Math.random() * 50 + 20;
    const trend = (Math.random() - 0.5) * 0.1; // -5% to +5% trend
    
    const dailyForecast = Array.from({ length: forecastPeriodDays }, (_, day) => {
      const seasonalMultiplier = 1 + Math.sin((day / forecastPeriodDays) * 2 * Math.PI) * 0.2 * seasonalityFactor;
      const trendMultiplier = 1 + (trend * day / forecastPeriodDays);
      const randomVariation = 0.8 + Math.random() * 0.4; // ±20% random variation
      
      const forecastedDemand = baseDemand * seasonalMultiplier * trendMultiplier * randomVariation;
      
      return {
        date: new Date(Date.now() + day * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        forecasted_demand: Math.round(forecastedDemand),
        confidence_interval: {
          lower: Math.round(forecastedDemand * 0.8),
          upper: Math.round(forecastedDemand * 1.2)
        }
      };
    });
    
    const totalForecastedDemand = dailyForecast.reduce((sum, day) => sum + day.forecasted_demand, 0);
    const averageDailyDemand = totalForecastedDemand / forecastPeriodDays;
    
    return {
      product_id: productId,
      product_name: product.name,
      sku: product.sku,
      forecast_period_days: forecastPeriodDays,
      total_forecasted_demand: totalForecastedDemand,
      average_daily_demand: averageDailyDemand.toFixed(2),
      trend_direction: trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable',
      trend_percentage: (trend * 100).toFixed(2),
      seasonality_factor: seasonalityFactor,
      current_stock: product.stock_quantity,
      stock_coverage_days: product.stock_quantity > 0 ? (product.stock_quantity / averageDailyDemand).toFixed(1) : '0',
      daily_forecast: dailyForecast
    };
  }).filter(Boolean);
  
  return {
    forecast_summary: {
      products_analyzed: forecasts.length,
      forecast_period_days: forecastPeriodDays,
      total_forecasted_demand: forecasts.reduce((sum, f) => sum + f.total_forecasted_demand, 0),
      accuracy_confidence: (85 + Math.random() * 10).toFixed(1) + '%'
    },
    product_forecasts: forecasts,
    methodology: {
      model_type: 'Seasonal Trend Decomposition',
      factors_considered: ['Historical demand', 'Seasonal patterns', 'Trend analysis', 'Random variations'],
      last_updated: new Date().toISOString()
    },
    recommendations: [
      'Review forecast accuracy weekly and adjust parameters',
      'Consider external factors (promotions, holidays) in planning',
      'Use forecast for procurement and inventory planning',
      'Monitor actual vs. forecasted demand for model improvement'
    ]
  };
}

function generateCostAnalysis(analysisType, timePeriod) {
  const costCategories = {
    inventory_holding: Math.random() * 50000 + 20000,
    transportation: Math.random() * 30000 + 15000,
    warehousing: Math.random() * 40000 + 25000,
    labor: Math.random() * 60000 + 40000,
    technology: Math.random() * 20000 + 10000,
    utilities: Math.random() * 15000 + 8000
  };
  
  const totalCosts = Object.values(costCategories).reduce((sum, cost) => sum + cost, 0);
  
  const optimizationOpportunities = [
    {
      category: 'inventory_holding',
      current_cost: costCategories.inventory_holding.toFixed(2),
      potential_savings: (costCategories.inventory_holding * 0.15).toFixed(2),
      savings_percentage: '15%',
      recommendations: ['Implement just-in-time inventory', 'Reduce slow-moving stock', 'Optimize reorder points']
    },
    {
      category: 'transportation',
      current_cost: costCategories.transportation.toFixed(2),
      potential_savings: (costCategories.transportation * 0.12).toFixed(2),
      savings_percentage: '12%',
      recommendations: ['Optimize delivery routes', 'Consolidate shipments', 'Negotiate better carrier rates']
    },
    {
      category: 'warehousing',
      current_cost: costCategories.warehousing.toFixed(2),
      potential_savings: (costCategories.warehousing * 0.08).toFixed(2),
      savings_percentage: '8%',
      recommendations: ['Improve space utilization', 'Automate storage systems', 'Optimize layout design']
    }
  ];
  
  const totalPotentialSavings = optimizationOpportunities.reduce((sum, opp) => 
    sum + parseFloat(opp.potential_savings), 0);
  
  return {
    analysis_period: `${timePeriod} days`,
    analysis_type: analysisType,
    cost_breakdown: costCategories,
    total_costs: totalCosts.toFixed(2),
    cost_per_order: (totalCosts / (Math.random() * 1000 + 500)).toFixed(2),
    optimization_opportunities: optimizationOpportunities,
    total_potential_savings: totalPotentialSavings.toFixed(2),
    potential_savings_percentage: ((totalPotentialSavings / totalCosts) * 100).toFixed(1),
    roi_analysis: {
      implementation_cost: (totalPotentialSavings * 0.3).toFixed(2),
      payback_period_months: Math.ceil((totalPotentialSavings * 0.3) / (totalPotentialSavings / 12)),
      annual_roi_percentage: (((totalPotentialSavings - (totalPotentialSavings * 0.3)) / (totalPotentialSavings * 0.3)) * 100).toFixed(1)
    },
    recommendations: [
      'Focus on high-impact, low-cost optimizations first',
      'Implement phased approach to cost reduction',
      'Monitor cost metrics continuously',
      'Invest in automation for long-term savings'
    ]
  };
}

function generateStaffSchedule(warehouse, shiftRequirements, staffAvailability) {
  const shifts = ['morning', 'afternoon', 'night'];
  const roles = ['picker', 'packer', 'loader', 'supervisor', 'maintenance'];
  
  const schedule = shifts.map(shift => {
    const staffNeeded = roles.map(role => ({
      role: role,
      required_count: Math.floor(Math.random() * 5) + 2,
      assigned_count: Math.floor(Math.random() * 4) + 2,
      skill_level_required: ['basic', 'intermediate', 'advanced'][Math.floor(Math.random() * 3)]
    }));
    
    const totalRequired = staffNeeded.reduce((sum, s) => sum + s.required_count, 0);
    const totalAssigned = staffNeeded.reduce((sum, s) => sum + s.assigned_count, 0);
    
    return {
      shift: shift,
      time_range: shift === 'morning' ? '06:00-14:00' : 
                 shift === 'afternoon' ? '14:00-22:00' : '22:00-06:00',
      staffing_requirements: staffNeeded,
      total_required: totalRequired,
      total_assigned: totalAssigned,
      staffing_percentage: ((totalAssigned / totalRequired) * 100).toFixed(1),
      overtime_needed: Math.max(0, totalRequired - totalAssigned)
    };
  });
  
  const totalStaffRequired = schedule.reduce((sum, s) => sum + s.total_required, 0);
  const totalStaffAssigned = schedule.reduce((sum, s) => sum + s.total_assigned, 0);
  
  return {
    warehouse: {
      warehouse_id: warehouse.warehouse_id,
      name: warehouse.name,
      location: warehouse.location
    },
    schedule_period: 'Weekly',
    shifts: schedule,
    summary: {
      total_staff_required: totalStaffRequired,
      total_staff_assigned: totalStaffAssigned,
      overall_staffing_percentage: ((totalStaffAssigned / totalStaffRequired) * 100).toFixed(1),
      total_overtime_hours: schedule.reduce((sum, s) => sum + s.overtime_needed, 0) * 8
    },
    optimization_suggestions: [
      'Cross-train staff for multiple roles to increase flexibility',
      'Consider part-time staff for peak periods',
      'Implement staggered shifts to reduce overtime costs',
      'Use temporary staff during high-demand seasons'
    ],
    cost_analysis: {
      regular_labor_cost: (totalStaffAssigned * 8 * 15 * 7).toFixed(2), // $15/hour base
      overtime_cost: (schedule.reduce((sum, s) => sum + s.overtime_needed, 0) * 8 * 22.5 * 7).toFixed(2), // $22.5/hour overtime
      total_weekly_cost: ((totalStaffAssigned * 8 * 15 * 7) + (schedule.reduce((sum, s) => sum + s.overtime_needed, 0) * 8 * 22.5 * 7)).toFixed(2)
    }
  };
}

module.exports = router;

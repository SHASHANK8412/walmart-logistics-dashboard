const express = require('express');
const router = express.Router();
const GoogleMapsService = require('../services/googleMapsService');
const databaseService = require('../services/databaseService');

// Initialize Google Maps service
const googleMaps = new GoogleMapsService();

/**
 * GET /api/delivery/:id/live-tracking
 * Get live tracking information for a delivery
 */
router.get('/:id/live-tracking', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Get delivery from database
    const delivery = await databaseService.getDelivery(id);
    
    if (!delivery) {
      return res.status(404).json({
        success: false,
        error: 'Delivery not found'
      });
    }
    
    // Simulate real-time driver location (in production, this would come from GPS)
    const driverLocation = {
      lat: delivery.delivery_coordinates?.lat || (40.7128 + Math.random() * 0.01),
      lng: delivery.delivery_coordinates?.lng || (-74.0060 + Math.random() * 0.01)
    };
    
    // Get real-time route information
    const trackingInfo = await googleMaps.getDeliveryTracking(
      id,
      driverLocation,
      delivery.delivery_address
    );
    
    res.json({
      success: true,
      delivery_id: id,
      driver: {
        name: delivery.driver_name,
        vehicle: delivery.vehicle_id,
        current_location: driverLocation
      },
      tracking: trackingInfo.success ? trackingInfo.tracking : null,
      google_maps_link: trackingInfo.success ? trackingInfo.tracking.google_maps_link : null,
      last_updated: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Live tracking error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get live tracking',
      message: error.message
    });
  }
});

/**
 * POST /api/delivery/calculate-route
 * Calculate delivery route using Google Maps
 */
router.post('/calculate-route', async (req, res) => {
  try {
    const { origin, destination, optimizeForTraffic = true } = req.body;
    
    if (!origin || !destination) {
      return res.status(400).json({
        success: false,
        error: 'Origin and destination are required'
      });
    }
    
    const routeInfo = await googleMaps.calculateRoute(origin, destination, optimizeForTraffic);
    
    if (routeInfo.success) {
      res.json({
        success: true,
        route: routeInfo.route,
        google_maps_link: googleMaps.generateMapsLink(origin, destination),
        calculated_at: new Date().toISOString()
      });
    } else {
      res.status(500).json({
        success: false,
        error: 'Route calculation failed',
        message: routeInfo.error
      });
    }
    
  } catch (error) {
    console.error('Route calculation error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to calculate route',
      message: error.message
    });
  }
});

/**
 * POST /api/delivery/bulk-optimize
 * Optimize routes for multiple deliveries
 */
router.post('/bulk-optimize', async (req, res) => {
  try {
    const { deliveries, warehouse_location } = req.body;
    
    if (!deliveries || !Array.isArray(deliveries) || deliveries.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Valid deliveries array is required'
      });
    }
    
    const origin = warehouse_location || "Walmart Distribution Center, 508 SW 8th St, Bentonville, AR 72716";
    const destinations = deliveries.map(delivery => delivery.delivery_address);
    
    const optimizedRoute = await googleMaps.optimizeDeliveryRoute(origin, destinations);
    
    if (optimizedRoute.success) {
      // Map the optimized order back to original deliveries
      const optimizedDeliveries = optimizedRoute.optimized_route.waypoint_order.map(index => 
        deliveries[index]
      );
      
      res.json({
        success: true,
        optimized_deliveries: optimizedDeliveries,
        route_details: optimizedRoute.optimized_route,
        savings: {
          total_distance: optimizedRoute.optimized_route.total_distance,
          total_time: optimizedRoute.optimized_route.total_duration,
          estimated_completion: optimizedRoute.optimized_route.estimated_completion
        },
        google_maps_optimized: true
      });
    } else {
      res.status(500).json({
        success: false,
        error: 'Route optimization failed',
        message: optimizedRoute.error
      });
    }
    
  } catch (error) {
    console.error('Bulk optimization error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to optimize delivery routes',
      message: error.message
    });
  }
});

/**
 * PUT /api/delivery/:id/update-location
 * Update driver location for real-time tracking
 */
router.put('/:id/update-location', async (req, res) => {
  try {
    const { id } = req.params;
    const { lat, lng, timestamp } = req.body;
    
    if (!lat || !lng) {
      return res.status(400).json({
        success: false,
        error: 'Latitude and longitude are required'
      });
    }
    
    // Update delivery location in database
    const updateData = {
      current_location: { lat: parseFloat(lat), lng: parseFloat(lng) },
      last_location_update: timestamp || new Date().toISOString()
    };
    
    const updatedDelivery = await databaseService.updateDelivery(id, updateData);
    
    if (updatedDelivery) {
      // Recalculate ETA based on new location
      const delivery = await databaseService.getDelivery(id);
      const trackingInfo = await googleMaps.getDeliveryTracking(
        id,
        { lat: parseFloat(lat), lng: parseFloat(lng) },
        delivery.delivery_address
      );
      
      res.json({
        success: true,
        message: 'Location updated successfully',
        delivery_id: id,
        new_location: { lat: parseFloat(lat), lng: parseFloat(lng) },
        updated_eta: trackingInfo.success ? trackingInfo.tracking.estimated_arrival : null,
        tracking_info: trackingInfo.success ? trackingInfo.tracking : null
      });
    } else {
      res.status(404).json({
        success: false,
        error: 'Delivery not found'
      });
    }
    
  } catch (error) {
    console.error('Location update error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update location',
      message: error.message
    });
  }
});

/**
 * GET /api/delivery/geocode
 * Geocode an address using Google Maps
 */
router.get('/geocode', async (req, res) => {
  try {
    const { address } = req.query;
    
    if (!address) {
      return res.status(400).json({
        success: false,
        error: 'Address parameter is required'
      });
    }
    
    const geocodeResult = await googleMaps.geocodeAddress(address);
    
    if (geocodeResult.success) {
      res.json({
        success: true,
        geocoded_address: geocodeResult.formatted_address,
        coordinates: geocodeResult.coordinates,
        place_id: geocodeResult.place_id
      });
    } else {
      res.status(404).json({
        success: false,
        error: 'Address not found',
        message: geocodeResult.error
      });
    }
    
  } catch (error) {
    console.error('Geocoding error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to geocode address',
      message: error.message
    });
  }
});

/**
 * GET /api/delivery/traffic-info
 * Get current traffic information for active deliveries
 */
router.get('/traffic-info', async (req, res) => {
  try {
    // Get all active deliveries
    const activeDeliveries = await databaseService.getActiveDeliveries();
    
    const trafficInfo = [];
    
    for (const delivery of activeDeliveries) {
      if (delivery.current_location && delivery.delivery_address) {
        const routeInfo = await googleMaps.calculateRoute(
          delivery.current_location,
          delivery.delivery_address
        );
        
        if (routeInfo.success) {
          trafficInfo.push({
            delivery_id: delivery.delivery_id,
            driver_name: delivery.driver_name,
            current_traffic: routeInfo.route.traffic_conditions,
            estimated_arrival: routeInfo.route.estimated_arrival,
            remaining_time: routeInfo.route.duration,
            remaining_distance: routeInfo.route.distance
          });
        }
      }
    }
    
    res.json({
      success: true,
      traffic_updates: trafficInfo,
      last_updated: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Traffic info error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to get traffic information',
      message: error.message
    });
  }
});

module.exports = router;

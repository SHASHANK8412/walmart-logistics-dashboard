const axios = require('axios');
require('dotenv').config();

class GoogleMapsService {
  constructor() {
    this.apiKey = process.env.GOOGLE_MAPS_API_KEY || 'your-google-maps-api-key-here';
    this.routesApiKey = process.env.GOOGLE_ROUTES_API_KEY || this.apiKey;
    this.placesApiKey = process.env.GOOGLE_PLACES_API_KEY || this.apiKey;
    this.baseUrl = 'https://maps.googleapis.com/maps/api';
    this.routesBaseUrl = 'https://routes.googleapis.com/directions/v2:computeRoutes';
  }

  /**
   * Geocode an address to get coordinates
   */
  async geocodeAddress(address) {
    try {
      const response = await axios.get(`${this.baseUrl}/geocode/json`, {
        params: {
          address: address,
          key: this.apiKey
        }
      });

      if (response.data.status === 'OK' && response.data.results.length > 0) {
        const result = response.data.results[0];
        return {
          success: true,
          coordinates: {
            lat: result.geometry.location.lat,
            lng: result.geometry.location.lng
          },
          formatted_address: result.formatted_address,
          place_id: result.place_id
        };
      } else {
        return {
          success: false,
          error: 'Address not found',
          status: response.data.status
        };
      }
    } catch (error) {
      console.error('Geocoding error:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Calculate route between two points using Google Routes API
   */
  async calculateRoute(origin, destination, optimizeWaypoints = true) {
    try {
      // First geocode addresses if they're strings
      let originCoords = origin;
      let destCoords = destination;

      if (typeof origin === 'string') {
        const geocoded = await this.geocodeAddress(origin);
        if (!geocoded.success) {
          throw new Error(`Failed to geocode origin: ${origin}`);
        }
        originCoords = geocoded.coordinates;
      }

      if (typeof destination === 'string') {
        const geocoded = await this.geocodeAddress(destination);
        if (!geocoded.success) {
          throw new Error(`Failed to geocode destination: ${destination}`);
        }
        destCoords = geocoded.coordinates;
      }

      // Use Google Routes API for advanced routing
      const routeRequest = {
        origin: {
          location: {
            latLng: {
              latitude: originCoords.lat,
              longitude: originCoords.lng
            }
          }
        },
        destination: {
          location: {
            latLng: {
              latitude: destCoords.lat,
              longitude: destCoords.lng
            }
          }
        },
        travelMode: 'DRIVE',
        routingPreference: 'TRAFFIC_AWARE',
        computeAlternativeRoutes: false,
        routeModifiers: {
          avoidTolls: false,
          avoidHighways: false,
          avoidFerries: false
        },
        languageCode: 'en-US',
        units: 'IMPERIAL'
      };

      const response = await axios.post(this.routesBaseUrl, routeRequest, {
        headers: {
          'Content-Type': 'application/json',
          'X-Goog-Api-Key': this.routesApiKey,
          'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.legs.steps'
        }
      });

      if (response.data.routes && response.data.routes.length > 0) {
        const route = response.data.routes[0];
        
        return {
          success: true,
          route: {
            distance: {
              meters: route.distanceMeters,
              miles: (route.distanceMeters * 0.000621371).toFixed(2)
            },
            duration: {
              seconds: parseInt(route.duration.replace('s', '')),
              text: this.formatDuration(parseInt(route.duration.replace('s', '')))
            },
            polyline: route.polyline?.encodedPolyline,
            estimated_arrival: new Date(Date.now() + (parseInt(route.duration.replace('s', '')) * 1000)),
            traffic_conditions: 'TRAFFIC_AWARE_CALCULATED',
            route_optimized: true
          }
        };
      } else {
        throw new Error('No routes found');
      }
    } catch (error) {
      console.error('Route calculation error:', error.message);
      
      // Fallback to Distance Matrix API if Routes API fails
      return await this.calculateRouteDistanceMatrix(originCoords, destCoords);
    }
  }

  /**
   * Fallback route calculation using Distance Matrix API
   */
  async calculateRouteDistanceMatrix(origin, destination) {
    try {
      const response = await axios.get(`${this.baseUrl}/distancematrix/json`, {
        params: {
          origins: `${origin.lat},${origin.lng}`,
          destinations: `${destination.lat},${destination.lng}`,
          mode: 'driving',
          units: 'imperial',
          departure_time: 'now',
          traffic_model: 'best_guess',
          key: this.apiKey
        }
      });

      if (response.data.status === 'OK' && response.data.rows[0].elements[0].status === 'OK') {
        const element = response.data.rows[0].elements[0];
        
        return {
          success: true,
          route: {
            distance: {
              text: element.distance.text,
              meters: element.distance.value,
              miles: (element.distance.value * 0.000621371).toFixed(2)
            },
            duration: {
              text: element.duration.text,
              seconds: element.duration.value
            },
            duration_in_traffic: element.duration_in_traffic ? {
              text: element.duration_in_traffic.text,
              seconds: element.duration_in_traffic.value
            } : null,
            estimated_arrival: new Date(Date.now() + (element.duration.value * 1000)),
            traffic_conditions: element.duration_in_traffic ? 'TRAFFIC_AWARE' : 'NORMAL',
            route_optimized: true
          }
        };
      } else {
        throw new Error('Distance calculation failed');
      }
    } catch (error) {
      console.error('Distance Matrix error:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get real-time tracking information
   */
  async getDeliveryTracking(deliveryId, currentLocation, destination) {
    try {
      // Calculate current route from driver location to destination
      const routeInfo = await this.calculateRoute(currentLocation, destination);
      
      if (routeInfo.success) {
        return {
          success: true,
          tracking: {
            delivery_id: deliveryId,
            current_location: currentLocation,
            destination: destination,
            estimated_arrival: routeInfo.route.estimated_arrival,
            remaining_distance: routeInfo.route.distance,
            remaining_time: routeInfo.route.duration,
            traffic_conditions: routeInfo.route.traffic_conditions,
            last_updated: new Date().toISOString(),
            status: 'IN_TRANSIT',
            google_maps_link: this.generateMapsLink(currentLocation, destination)
          }
        };
      } else {
        throw new Error('Failed to calculate tracking route');
      }
    } catch (error) {
      console.error('Tracking error:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Optimize delivery route for multiple stops
   */
  async optimizeDeliveryRoute(origin, destinations, returnToOrigin = true) {
    try {
      if (destinations.length === 0) {
        throw new Error('No destinations provided');
      }

      // For single destination, use regular route calculation
      if (destinations.length === 1) {
        return await this.calculateRoute(origin, destinations[0]);
      }

      // For multiple destinations, use Directions API with waypoint optimization
      const waypoints = destinations.slice(0, -1).map(dest => 
        typeof dest === 'string' ? dest : `${dest.lat},${dest.lng}`
      ).join('|');
      
      const finalDestination = destinations[destinations.length - 1];
      
      const response = await axios.get(`${this.baseUrl}/directions/json`, {
        params: {
          origin: typeof origin === 'string' ? origin : `${origin.lat},${origin.lng}`,
          destination: typeof finalDestination === 'string' ? finalDestination : `${finalDestination.lat},${finalDestination.lng}`,
          waypoints: `optimize:true|${waypoints}`,
          mode: 'driving',
          departure_time: 'now',
          traffic_model: 'best_guess',
          key: this.apiKey
        }
      });

      if (response.data.status === 'OK' && response.data.routes.length > 0) {
        const route = response.data.routes[0];
        
        return {
          success: true,
          optimized_route: {
            total_distance: route.legs.reduce((total, leg) => total + leg.distance.value, 0),
            total_duration: route.legs.reduce((total, leg) => total + leg.duration.value, 0),
            waypoint_order: route.waypoint_order,
            legs: route.legs.map((leg, index) => ({
              step: index + 1,
              start_address: leg.start_address,
              end_address: leg.end_address,
              distance: leg.distance.text,
              duration: leg.duration.text,
              traffic_duration: leg.duration_in_traffic?.text
            })),
            polyline: route.overview_polyline.points,
            optimized: true,
            estimated_completion: new Date(Date.now() + (route.legs.reduce((total, leg) => total + leg.duration.value, 0) * 1000))
          }
        };
      } else {
        throw new Error('Route optimization failed');
      }
    } catch (error) {
      console.error('Route optimization error:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Generate Google Maps link for tracking
   */
  generateMapsLink(origin, destination) {
    const originStr = typeof origin === 'string' ? origin : `${origin.lat},${origin.lng}`;
    const destStr = typeof destination === 'string' ? destination : `${destination.lat},${destination.lng}`;
    
    return `https://www.google.com/maps/dir/${encodeURIComponent(originStr)}/${encodeURIComponent(destStr)}`;
  }

  /**
   * Format duration in seconds to human readable format
   */
  formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else {
      return `${minutes}m`;
    }
  }

  /**
   * Get place details from Place ID
   */
  async getPlaceDetails(placeId) {
    try {
      const response = await axios.get(`${this.baseUrl}/place/details/json`, {
        params: {
          place_id: placeId,
          fields: 'name,formatted_address,geometry,formatted_phone_number,opening_hours',
          key: this.placesApiKey
        }
      });

      if (response.data.status === 'OK') {
        return {
          success: true,
          place: response.data.result
        };
      } else {
        return {
          success: false,
          error: response.data.status
        };
      }
    } catch (error) {
      console.error('Place details error:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Search for nearby places (warehouses, distribution centers)
   */
  async findNearbyWarehouses(location, radius = 5000) {
    try {
      const response = await axios.get(`${this.baseUrl}/place/nearbysearch/json`, {
        params: {
          location: typeof location === 'string' ? location : `${location.lat},${location.lng}`,
          radius: radius,
          keyword: 'warehouse distribution center',
          type: 'storage',
          key: this.placesApiKey
        }
      });

      if (response.data.status === 'OK') {
        return {
          success: true,
          warehouses: response.data.results.map(place => ({
            place_id: place.place_id,
            name: place.name,
            address: place.vicinity,
            location: place.geometry.location,
            rating: place.rating,
            distance: null // Would need to calculate
          }))
        };
      } else {
        return {
          success: false,
          error: response.data.status
        };
      }
    } catch (error) {
      console.error('Nearby search error:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = GoogleMapsService;

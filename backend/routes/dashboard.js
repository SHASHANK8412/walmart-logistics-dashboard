const express = require('express');
const router = express.Router();
const databaseService = require('../services/databaseService');

/**
 * GET /api/dashboard/overview
 * Get dashboard overview with key metrics
 */
router.get('/overview', (req, res) => {
  try {
    const ordersAnalytics = mockDataService.getOrdersAnalytics();
    const inventoryAnalytics = mockDataService.getInventoryAnalytics();
    const deliveries = mockDataService.getDeliveries();
    const warehouses = mockDataService.getWarehouses();
    
    // Delivery analytics
    const totalDeliveries = deliveries.length;
    const pendingDeliveries = deliveries.filter(d => d.status === 'pending').length;
    const inTransitDeliveries = deliveries.filter(d => d.status === 'in_transit').length;
    const completedDeliveries = deliveries.filter(d => d.status === 'delivered').length;
    
    // Warehouse analytics
    const totalCapacity = warehouses.reduce((sum, w) => sum + w.capacity, 0);
    const totalUtilization = warehouses.reduce((sum, w) => sum + w.current_utilization, 0);
    const overallUtilization = totalCapacity > 0 ? ((totalUtilization / totalCapacity) * 100).toFixed(2) : 0;
    
    // Performance metrics
    const performanceMetrics = {
      order_fulfillment_rate: ((completedDeliveries / totalDeliveries) * 100).toFixed(2),
      inventory_turnover: (parseFloat(ordersAnalytics.total_revenue) / parseFloat(inventoryAnalytics.total_inventory_value) * 12).toFixed(2),
      warehouse_efficiency: overallUtilization,
      delivery_success_rate: ((completedDeliveries / totalDeliveries) * 100).toFixed(2)
    };
    
    // Recent activity
    const recentOrders = mockDataService.getOrders().slice(0, 5);
    const recentDeliveries = deliveries.slice(0, 5);
    
    // Alerts and notifications
    const alerts = [];
    
    if (parseInt(inventoryAnalytics.low_stock_items) > 0) {
      alerts.push({
        type: 'warning',
        message: `${inventoryAnalytics.low_stock_items} products are running low on stock`,
        priority: 'medium',
        timestamp: new Date().toISOString()
      });
    }
    
    if (parseInt(inventoryAnalytics.out_of_stock_items) > 0) {
      alerts.push({
        type: 'error',
        message: `${inventoryAnalytics.out_of_stock_items} products are out of stock`,
        priority: 'high',
        timestamp: new Date().toISOString()
      });
    }
    
    if (pendingDeliveries > 10) {
      alerts.push({
        type: 'info',
        message: `${pendingDeliveries} deliveries are pending dispatch`,
        priority: 'low',
        timestamp: new Date().toISOString()
      });
    }
    
    const overview = {
      summary: {
        total_orders: ordersAnalytics.total_orders,
        pending_orders: ordersAnalytics.pending_orders,
        total_revenue: ordersAnalytics.total_revenue,
        total_products: inventoryAnalytics.total_products,
        low_stock_items: inventoryAnalytics.low_stock_items,
        total_deliveries: totalDeliveries,
        pending_deliveries: pendingDeliveries,
        total_warehouses: warehouses.length,
        warehouse_utilization: overallUtilization
      },
      performance_metrics: performanceMetrics,
      recent_activity: {
        recent_orders: recentOrders,
        recent_deliveries: recentDeliveries
      },
      alerts: alerts,
      quick_stats: {
        revenue_growth: (Math.random() * 10 + 5).toFixed(1) + '%',
        order_growth: (Math.random() * 15 + 8).toFixed(1) + '%',
        customer_satisfaction: (Math.random() * 0.5 + 4.5).toFixed(1) + '/5.0',
        on_time_delivery: (Math.random() * 10 + 85).toFixed(1) + '%'
      }
    };
    
    res.json({
      success: true,
      data: overview,
      last_updated: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch dashboard overview',
      message: error.message
    });
  }
});

/**
 * GET /api/dashboard/analytics
 * Get detailed analytics data for charts
 */
router.get('/analytics', (req, res) => {
  try {
    const { period = '30d', metric = 'all' } = req.query;
    
    // Generate time series data for charts
    const days = period === '7d' ? 7 : period === '30d' ? 30 : 90;
    const chartData = generateChartData(days);
    
    const analytics = {
      time_period: period,
      chart_data: chartData,
      summary_stats: {
        period_total_orders: chartData.orders.reduce((sum, day) => sum + day.value, 0),
        period_total_revenue: chartData.revenue.reduce((sum, day) => sum + day.value, 0).toFixed(2),
        period_avg_daily_orders: (chartData.orders.reduce((sum, day) => sum + day.value, 0) / days).toFixed(1),
        period_avg_daily_revenue: (chartData.revenue.reduce((sum, day) => sum + day.value, 0) / days).toFixed(2)
      },
      comparisons: {
        orders_vs_previous_period: (Math.random() * 20 - 10).toFixed(1) + '%',
        revenue_vs_previous_period: (Math.random() * 15 - 5).toFixed(1) + '%',
        delivery_time_vs_previous_period: (Math.random() * 10 - 15).toFixed(1) + '%'
      },
      trends: {
        orders_trend: Math.random() > 0.5 ? 'increasing' : 'decreasing',
        revenue_trend: Math.random() > 0.6 ? 'increasing' : 'stable',
        efficiency_trend: Math.random() > 0.7 ? 'improving' : 'stable'
      }
    };
    
    res.json({
      success: true,
      data: analytics
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch analytics data',
      message: error.message
    });
  }
});

/**
 * GET /api/dashboard/kpis
 * Get Key Performance Indicators
 */
router.get('/kpis', (req, res) => {
  try {
    const kpis = {
      operational: {
        order_accuracy: {
          value: (Math.random() * 5 + 95).toFixed(2),
          unit: '%',
          trend: Math.random() > 0.5 ? 'up' : 'down',
          target: '98.0',
          status: 'good'
        },
        inventory_accuracy: {
          value: (Math.random() * 4 + 96).toFixed(2),
          unit: '%',
          trend: 'up',
          target: '99.0',
          status: 'good'
        },
        order_cycle_time: {
          value: (Math.random() * 2 + 2).toFixed(1),
          unit: 'hours',
          trend: 'down',
          target: '2.0',
          status: 'excellent'
        },
        warehouse_productivity: {
          value: (Math.random() * 20 + 80).toFixed(0),
          unit: 'orders/hour',
          trend: 'up',
          target: '85',
          status: 'good'
        }
      },
      financial: {
        cost_per_order: {
          value: (Math.random() * 5 + 15).toFixed(2),
          unit: '$',
          trend: 'down',
          target: '18.00',
          status: 'excellent'
        },
        inventory_carrying_cost: {
          value: (Math.random() * 2 + 18).toFixed(1),
          unit: '%',
          trend: 'stable',
          target: '20.0',
          status: 'good'
        },
        transportation_cost_ratio: {
          value: (Math.random() * 2 + 8).toFixed(1),
          unit: '%',
          trend: 'down',
          target: '10.0',
          status: 'good'
        },
        labor_productivity: {
          value: (Math.random() * 10 + 85).toFixed(0),
          unit: '%',
          trend: 'up',
          target: '90',
          status: 'good'
        }
      },
      customer: {
        order_fulfillment_rate: {
          value: (Math.random() * 3 + 97).toFixed(1),
          unit: '%',
          trend: 'up',
          target: '98.0',
          status: 'good'
        },
        on_time_delivery: {
          value: (Math.random() * 5 + 90).toFixed(1),
          unit: '%',
          trend: 'stable',
          target: '95.0',
          status: 'good'
        },
        customer_satisfaction: {
          value: (Math.random() * 0.3 + 4.7).toFixed(1),
          unit: '/5.0',
          trend: 'up',
          target: '4.5',
          status: 'excellent'
        },
        return_rate: {
          value: (Math.random() * 1 + 2).toFixed(1),
          unit: '%',
          trend: 'down',
          target: '3.0',
          status: 'good'
        }
      }
    };
    
    res.json({
      success: true,
      data: kpis,
      last_updated: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch KPIs',
      message: error.message
    });
  }
});

/**
 * GET /api/dashboard/real-time
 * Get real-time dashboard data
 */
router.get('/real-time', (req, res) => {
  try {
    const realTimeData = {
      current_time: new Date().toISOString(),
      active_users: Math.floor(Math.random() * 50) + 20,
      orders_today: Math.floor(Math.random() * 200) + 100,
      orders_this_hour: Math.floor(Math.random() * 25) + 5,
      revenue_today: (Math.random() * 50000 + 25000).toFixed(2),
      active_deliveries: Math.floor(Math.random() * 30) + 10,
      warehouse_alerts: Math.floor(Math.random() * 5),
      system_status: {
        api_status: 'operational',
        database_status: 'operational',
        payment_gateway: 'operational',
        inventory_system: Math.random() > 0.95 ? 'warning' : 'operational',
        delivery_tracking: 'operational'
      },
      live_metrics: {
        orders_per_minute: (Math.random() * 2 + 1).toFixed(1),
        average_order_value: (Math.random() * 50 + 75).toFixed(2),
        conversion_rate: (Math.random() * 2 + 3).toFixed(2) + '%',
        page_load_time: (Math.random() * 1 + 1.5).toFixed(2) + 's'
      },
      geographical_activity: [
        { region: 'North America', orders: Math.floor(Math.random() * 50) + 20, revenue: (Math.random() * 15000 + 10000).toFixed(2) },
        { region: 'Europe', orders: Math.floor(Math.random() * 30) + 15, revenue: (Math.random() * 10000 + 7000).toFixed(2) },
        { region: 'Asia Pacific', orders: Math.floor(Math.random() * 40) + 25, revenue: (Math.random() * 12000 + 8000).toFixed(2) },
        { region: 'South America', orders: Math.floor(Math.random() * 20) + 10, revenue: (Math.random() * 8000 + 5000).toFixed(2) }
      ]
    };
    
    res.json({
      success: true,
      data: realTimeData
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch real-time data',
      message: error.message
    });
  }
});

// Helper function to generate chart data
function generateChartData(days) {
  const chartData = {
    orders: [],
    revenue: [],
    deliveries: [],
    inventory_levels: []
  };
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(Date.now() - i * 24 * 60 * 60 * 1000);
    const dateStr = date.toISOString().split('T')[0];
    
    // Generate realistic data with some trends and seasonality
    const weekday = date.getDay();
    const isWeekend = weekday === 0 || weekday === 6;
    const weekdayMultiplier = isWeekend ? 0.7 : 1.0;
    
    const baseOrders = 50 + Math.random() * 30;
    const orders = Math.floor(baseOrders * weekdayMultiplier);
    
    const baseRevenue = orders * (75 + Math.random() * 50);
    const revenue = baseRevenue * (0.8 + Math.random() * 0.4);
    
    chartData.orders.push({
      date: dateStr,
      value: orders,
      label: date.toLocaleDateString('en-US', { weekday: 'short' })
    });
    
    chartData.revenue.push({
      date: dateStr,
      value: parseFloat(revenue.toFixed(2)),
      label: date.toLocaleDateString('en-US', { weekday: 'short' })
    });
    
    chartData.deliveries.push({
      date: dateStr,
      value: Math.floor(orders * 0.9), // 90% of orders become deliveries
      label: date.toLocaleDateString('en-US', { weekday: 'short' })
    });
    
    chartData.inventory_levels.push({
      date: dateStr,
      value: Math.floor(Math.random() * 1000 + 8000),
      label: date.toLocaleDateString('en-US', { weekday: 'short' })
    });
  }
  
  return chartData;
}

module.exports = router;

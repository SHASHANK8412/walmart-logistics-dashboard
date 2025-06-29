const Order = require('../models/Order');
const Product = require('../models/Product');
const Delivery = require('../models/Delivery');
const Warehouse = require('../models/Warehouse');
const { DataGenerator } = require('../utils/helpers');

/**
 * Mock data generator for development and testing
 */
class MockDataService {
  constructor() {
    this.orders = [];
    this.products = [];
    this.deliveries = [];
    this.warehouses = [];
    this.initialized = false;
  }

  initialize() {
    if (this.initialized) return;
    
    this.generateProducts();
    this.generateWarehouses();
    this.generateOrders();
    this.generateDeliveries();
    
    this.initialized = true;
  }

  generateProducts(count = 50) {
    const categories = Product.getCategories();
    const suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Global Supply Co.', 'Best Wholesaler'];
    const productNames = {
      'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Speaker', 'Headphones'],
      'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 'Hat', 'Socks', 'Sweater'],
      'Home & Garden': ['Chair', 'Table', 'Lamp', 'Vase', 'Plant Pot', 'Cushion', 'Mirror', 'Clock'],
      'Sports & Outdoors': ['Football', 'Basketball', 'Tennis Racket', 'Running Shoes', 'Bike', 'Helmet'],
      'Health & Beauty': ['Shampoo', 'Soap', 'Toothbrush', 'Moisturizer', 'Perfume', 'Vitamins']
    };

    for (let i = 0; i < count; i++) {
      const category = categories[Math.floor(Math.random() * categories.length)];
      const nameOptions = productNames[category] || ['Generic Product'];
      const name = nameOptions[Math.floor(Math.random() * nameOptions.length)];
      
      const cost = DataGenerator.generateRandomPrice(5, 200);
      const price = cost * (1.3 + Math.random() * 0.7); // 30-100% markup
      
      const product = new Product({
        name: name,
        category: category,
        price: parseFloat(price.toFixed(2)),
        cost: cost,
        stock_quantity: Math.floor(Math.random() * 1000) + 10,
        reorder_level: Math.floor(Math.random() * 50) + 5,
        supplier: suppliers[Math.floor(Math.random() * suppliers.length)],
        description: `High quality ${name.toLowerCase()} from ${category.toLowerCase()} category`,
        location: `Aisle ${Math.floor(Math.random() * 20) + 1}-${Math.floor(Math.random() * 50) + 1}`
      });
      
      this.products.push(product);
    }
  }

  generateOrders(count = 100) {
    const statuses = Order.getValidStatuses();
    const paymentMethods = Order.getPaymentMethods();
    
    for (let i = 0; i < count; i++) {
      const customerName = DataGenerator.generateRandomName();
      const product = this.products[Math.floor(Math.random() * this.products.length)];
      
      const order = new Order({
        customer_name: customerName,
        customer_email: DataGenerator.generateRandomEmail(customerName),
        product_id: product.sku,
        product_name: product.name,
        quantity: Math.floor(Math.random() * 5) + 1,
        price: product.price,
        status: statuses[Math.floor(Math.random() * statuses.length)],
        order_date: DataGenerator.generateRandomDate(30),
        delivery_address: DataGenerator.generateRandomAddress(),
        payment_method: paymentMethods[Math.floor(Math.random() * paymentMethods.length)]
      });
      
      this.orders.push(order);
    }
  }

  generateDeliveries(count = 75) {
    const statuses = Delivery.getValidStatuses();
    const priorities = Delivery.getPriorityLevels();
    const drivers = ['John Smith', 'Mike Johnson', 'Sarah Davis', 'David Wilson', 'Lisa Brown'];
    const vehicles = ['VAN-001', 'TRUCK-002', 'VAN-003', 'TRUCK-004', 'VAN-005'];
    
    for (let i = 0; i < count; i++) {
      const order = this.orders[Math.floor(Math.random() * this.orders.length)];
      const pickupTime = Math.random() > 0.5 ? DataGenerator.generateRandomDate(10) : null;
      const estimatedDelivery = new Date(Date.now() + Math.random() * 7 * 24 * 60 * 60 * 1000);
      
      const delivery = new Delivery({
        order_id: order.order_id,
        driver_name: drivers[Math.floor(Math.random() * drivers.length)],
        vehicle_id: vehicles[Math.floor(Math.random() * vehicles.length)],
        pickup_address: 'Walmart Distribution Center, Main St, City',
        delivery_address: order.delivery_address,
        pickup_time: pickupTime,
        estimated_delivery_time: estimatedDelivery,
        status: statuses[Math.floor(Math.random() * statuses.length)],
        priority: priorities[Math.floor(Math.random() * priorities.length)],
        notes: Math.random() > 0.7 ? 'Fragile items - handle with care' : ''
      });
      
      this.deliveries.push(delivery);
    }
  }

  generateWarehouses(count = 5) {
    const locations = [
      'Los Angeles, CA',
      'Dallas, TX', 
      'Chicago, IL',
      'Atlanta, GA',
      'New York, NY'
    ];
    
    const managers = [
      'Robert Johnson',
      'Maria Garcia', 
      'James Williams',
      'Jennifer Davis',
      'Michael Brown'
    ];

    for (let i = 0; i < count; i++) {
      const capacity = Math.floor(Math.random() * 50000) + 10000;
      const utilization = Math.floor(Math.random() * capacity * 0.8);
      
      const warehouse = new Warehouse({
        name: `Walmart Distribution Center ${i + 1}`,
        location: locations[i],
        capacity: capacity,
        current_utilization: utilization,
        manager_name: managers[i],
        phone: `+1-555-${Math.floor(Math.random() * 9000) + 1000}`,
        email: `${managers[i].toLowerCase().replace(' ', '.')}@walmart.com`,
        operating_hours: { start: '06:00', end: '22:00' }
      });
      
      // Add some zones
      const zoneTypes = Warehouse.getZoneTypes();
      const numZones = Math.floor(Math.random() * 4) + 2;
      
      for (let j = 0; j < numZones; j++) {
        warehouse.addZone({
          name: `Zone ${String.fromCharCode(65 + j)}`,
          type: zoneTypes[Math.floor(Math.random() * zoneTypes.length)],
          capacity: Math.floor(capacity / numZones),
          current_stock: Math.floor(Math.random() * (capacity / numZones) * 0.7)
        });
      }
      
      this.warehouses.push(warehouse);
    }
  }

  // Data access methods
  getOrders(filters = {}) {
    let filtered = [...this.orders];
    
    if (filters.status) {
      filtered = filtered.filter(order => filters.status.includes(order.status));
    }
    
    if (filters.startDate && filters.endDate) {
      filtered = filtered.filter(order => {
        const orderDate = new Date(order.order_date);
        return orderDate >= new Date(filters.startDate) && orderDate <= new Date(filters.endDate);
      });
    }
    
    if (filters.customer_name) {
      filtered = filtered.filter(order => 
        order.customer_name.toLowerCase().includes(filters.customer_name.toLowerCase())
      );
    }
    
    return filtered.map(order => order.toJSON());
  }

  getProducts(filters = {}) {
    let filtered = [...this.products];
    
    if (filters.category) {
      filtered = filtered.filter(product => product.category === filters.category);
    }
    
    if (filters.low_stock) {
      filtered = filtered.filter(product => product.isLowStock());
    }
    
    if (filters.status) {
      filtered = filtered.filter(product => product.status === filters.status);
    }
    
    return filtered.map(product => product.toJSON());
  }

  getDeliveries(filters = {}) {
    let filtered = [...this.deliveries];
    
    if (filters.status) {
      filtered = filtered.filter(delivery => filters.status.includes(delivery.status));
    }
    
    if (filters.driver_name) {
      filtered = filtered.filter(delivery => 
        delivery.driver_name.toLowerCase().includes(filters.driver_name.toLowerCase())
      );
    }
    
    return filtered.map(delivery => delivery.toJSON());
  }

  getWarehouses() {
    return this.warehouses.map(warehouse => warehouse.toJSON());
  }

  // Individual item access
  getOrderById(id) {
    const order = this.orders.find(o => o.id == id);
    return order ? order.toJSON() : null;
  }

  getProductById(id) {
    const product = this.products.find(p => p.id == id);
    return product ? product.toJSON() : null;
  }

  getDeliveryById(id) {
    const delivery = this.deliveries.find(d => d.id == id);
    return delivery ? delivery.toJSON() : null;
  }

  getWarehouseById(id) {
    const warehouse = this.warehouses.find(w => w.id == id);
    return warehouse ? warehouse.toJSON() : null;
  }

  // Analytics methods
  getOrdersAnalytics() {
    const total = this.orders.length;
    const pending = this.orders.filter(o => o.status === 'pending').length;
    const shipped = this.orders.filter(o => o.status === 'shipped').length;
    const delivered = this.orders.filter(o => o.status === 'delivered').length;
    const cancelled = this.orders.filter(o => o.status === 'cancelled').length;
    
    const totalRevenue = this.orders
      .filter(o => o.status === 'delivered')
      .reduce((sum, order) => sum + (order.quantity * order.price), 0);
    
    return {
      total_orders: total,
      pending_orders: pending,
      shipped_orders: shipped,
      delivered_orders: delivered,
      cancelled_orders: cancelled,
      total_revenue: totalRevenue.toFixed(2)
    };
  }

  getInventoryAnalytics() {
    const total = this.products.length;
    const lowStock = this.products.filter(p => p.isLowStock()).length;
    const outOfStock = this.products.filter(p => p.stock_quantity === 0).length;
    
    const totalValue = this.products
      .reduce((sum, product) => sum + (product.stock_quantity * product.cost), 0);
    
    return {
      total_products: total,
      low_stock_items: lowStock,
      out_of_stock_items: outOfStock,
      total_inventory_value: totalValue.toFixed(2)
    };
  }
}

// Create singleton instance
const mockDataService = new MockDataService();

module.exports = mockDataService;

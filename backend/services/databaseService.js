const mongoose = require('mongoose');

// MongoDB Models
const MongoOrder = require('../models/MongoOrder');
const MongoProduct = require('../models/MongoProduct');
const MongoDelivery = require('../models/MongoDelivery');
const MongoWarehouse = require('../models/MongoWarehouse');

// Mock Data Service (fallback)
const mockDataService = require('./mockDataService');

class DatabaseService {
  constructor() {
    this.isMongoConnected = false;
    this.checkConnection();
  }

  checkConnection() {
    this.isMongoConnected = mongoose.connection.readyState === 1;
    
    // Listen for connection changes
    mongoose.connection.on('connected', () => {
      this.isMongoConnected = true;
      console.log('📊 Database service switched to MongoDB');
    });
    
    mongoose.connection.on('disconnected', () => {
      this.isMongoConnected = false;
      console.log('📊 Database service switched to Mock Data');
    });
  }

  // Generic method to choose between MongoDB and Mock data
  async useDatabase() {
    return this.isMongoConnected;
  }

  // ORDER METHODS
  async getOrders(filters = {}) {
    if (await this.useDatabase()) {
      try {
        let query = {};
        
        // Build MongoDB query from filters
        if (filters.status && filters.status.length > 0) {
          query.status = { $in: filters.status };
        }
        
        if (filters.startDate && filters.endDate) {
          query.order_date = {
            $gte: new Date(filters.startDate),
            $lte: new Date(filters.endDate)
          };
        }
        
        if (filters.customer_name) {
          query.customer_name = { $regex: filters.customer_name, $options: 'i' };
        }

        const orders = await MongoOrder.find(query).sort({ order_date: -1 });
        return orders.map(order => order.toJSON());
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getOrders(filters);
      }
    } else {
      return mockDataService.getOrders(filters);
    }
  }

  async getOrderById(id) {
    if (await this.useDatabase()) {
      try {
        const order = await MongoOrder.findById(id);
        return order ? order.toJSON() : null;
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getOrderById(id);
      }
    } else {
      return mockDataService.getOrderById(id);
    }
  }
  async createOrder(orderData) {
    if (await this.useDatabase()) {
      try {
        // Generate required fields for MongoDB
        const mongoOrderData = {
          ...orderData,
          order_id: orderData.order_id || `ORDER-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
          product_id: orderData.product_id || `PROD-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
          status: orderData.status || 'pending'
        };
        
        const order = new MongoOrder(mongoOrderData);
        await order.save();
        return order.toJSON();
      } catch (error) {
        console.error('MongoDB save error:', error);
        throw error;
      }
    } else {
      // For mock data, simulate creation
      const Order = require('../models/Order');
      const order = new Order(orderData);
      mockDataService.orders.push(order);
      return order.toJSON();
    }
  }

  async updateOrder(id, updateData) {
    if (await this.useDatabase()) {
      try {
        const order = await MongoOrder.findByIdAndUpdate(id, updateData, { 
          new: true, 
          runValidators: true 
        });
        return order ? order.toJSON() : null;
      } catch (error) {
        console.error('MongoDB update error:', error);
        throw error;
      }
    } else {
      // Mock data update
      const orderIndex = mockDataService.orders.findIndex(o => o.id == id);
      if (orderIndex !== -1) {
        Object.assign(mockDataService.orders[orderIndex], updateData);
        mockDataService.orders[orderIndex].updated_at = new Date();
        return mockDataService.orders[orderIndex].toJSON();
      }
      return null;
    }
  }

  async deleteOrder(id) {
    if (await this.useDatabase()) {
      try {
        const result = await MongoOrder.findByIdAndDelete(id);
        return !!result;
      } catch (error) {
        console.error('MongoDB delete error:', error);
        throw error;
      }
    } else {
      const orderIndex = mockDataService.orders.findIndex(o => o.id == id);
      if (orderIndex !== -1) {
        mockDataService.orders.splice(orderIndex, 1);
        return true;
      }
      return false;
    }
  }

  async getOrdersAnalytics() {
    if (await this.useDatabase()) {
      try {
        return await MongoOrder.getOrdersAnalytics();
      } catch (error) {
        console.error('MongoDB analytics error:', error);
        return mockDataService.getOrdersAnalytics();
      }
    } else {
      return mockDataService.getOrdersAnalytics();
    }
  }

  // PRODUCT METHODS
  async getProducts(filters = {}) {
    if (await this.useDatabase()) {
      try {
        let query = {};
        
        if (filters.category) {
          query.category = filters.category;
        }
        
        if (filters.low_stock) {
          query.$expr = { $lte: ['$stock_quantity', '$reorder_level'] };
        }
        
        if (filters.status) {
          query.status = filters.status;
        }

        const products = await MongoProduct.find(query).sort({ name: 1 });
        return products.map(product => product.toJSON());
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getProducts(filters);
      }
    } else {
      return mockDataService.getProducts(filters);
    }
  }

  async getProductById(id) {
    if (await this.useDatabase()) {
      try {
        const product = await MongoProduct.findById(id);
        return product ? product.toJSON() : null;
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getProductById(id);
      }
    } else {
      return mockDataService.getProductById(id);
    }
  }

  async createProduct(productData) {
    if (await this.useDatabase()) {
      try {
        const product = new MongoProduct(productData);
        await product.save();
        return product.toJSON();
      } catch (error) {
        console.error('MongoDB save error:', error);
        throw error;
      }
    } else {
      const Product = require('../models/Product');
      const product = new Product(productData);
      mockDataService.products.push(product);
      return product.toJSON();
    }
  }

  async updateProduct(id, updateData) {
    if (await this.useDatabase()) {
      try {
        const product = await MongoProduct.findByIdAndUpdate(id, updateData, { 
          new: true, 
          runValidators: true 
        });
        return product ? product.toJSON() : null;
      } catch (error) {
        console.error('MongoDB update error:', error);
        throw error;
      }
    } else {
      const productIndex = mockDataService.products.findIndex(p => p.id == id);
      if (productIndex !== -1) {
        Object.assign(mockDataService.products[productIndex], updateData);
        mockDataService.products[productIndex].updated_at = new Date();
        return mockDataService.products[productIndex].toJSON();
      }
      return null;
    }
  }

  async deleteProduct(id) {
    if (await this.useDatabase()) {
      try {
        const result = await MongoProduct.findByIdAndDelete(id);
        return !!result;
      } catch (error) {
        console.error('MongoDB delete error:', error);
        throw error;
      }
    } else {
      const productIndex = mockDataService.products.findIndex(p => p.id == id);
      if (productIndex !== -1) {
        mockDataService.products.splice(productIndex, 1);
        return true;
      }
      return false;
    }
  }

  async getInventoryAnalytics() {
    if (await this.useDatabase()) {
      try {
        return await MongoProduct.getInventoryAnalytics();
      } catch (error) {
        console.error('MongoDB analytics error:', error);
        return mockDataService.getInventoryAnalytics();
      }
    } else {
      return mockDataService.getInventoryAnalytics();
    }
  }

  // DELIVERY METHODS
  async getDeliveries(filters = {}) {
    if (await this.useDatabase()) {
      try {
        let query = {};
        
        if (filters.status && filters.status.length > 0) {
          query.status = { $in: filters.status };
        }
        
        if (filters.driver_name) {
          query.driver_name = { $regex: filters.driver_name, $options: 'i' };
        }

        const deliveries = await MongoDelivery.find(query).sort({ createdAt: -1 });
        return deliveries.map(delivery => delivery.toJSON());
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getDeliveries(filters);
      }
    } else {
      return mockDataService.getDeliveries(filters);
    }
  }

  async getDeliveryById(id) {
    if (await this.useDatabase()) {
      try {
        const delivery = await MongoDelivery.findById(id);
        return delivery ? delivery.toJSON() : null;
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getDeliveryById(id);
      }
    } else {
      return mockDataService.getDeliveryById(id);
    }
  }

  async createDelivery(deliveryData) {
    if (await this.useDatabase()) {
      try {
        const delivery = new MongoDelivery(deliveryData);
        await delivery.save();
        return delivery.toJSON();
      } catch (error) {
        console.error('MongoDB save error:', error);
        throw error;
      }
    } else {
      const Delivery = require('../models/Delivery');
      const delivery = new Delivery(deliveryData);
      mockDataService.deliveries.push(delivery);
      return delivery.toJSON();
    }
  }

  async updateDelivery(id, updateData) {
    if (await this.useDatabase()) {
      try {
        const delivery = await MongoDelivery.findByIdAndUpdate(id, updateData, { 
          new: true, 
          runValidators: true 
        });
        return delivery ? delivery.toJSON() : null;
      } catch (error) {
        console.error('MongoDB update error:', error);
        throw error;
      }
    } else {
      const deliveryIndex = mockDataService.deliveries.findIndex(d => d.id == id);
      if (deliveryIndex !== -1) {
        Object.assign(mockDataService.deliveries[deliveryIndex], updateData);
        mockDataService.deliveries[deliveryIndex].updated_at = new Date();
        return mockDataService.deliveries[deliveryIndex].toJSON();
      }
      return null;
    }
  }

  async deleteDelivery(id) {
    if (await this.useDatabase()) {
      try {
        const result = await MongoDelivery.findByIdAndDelete(id);
        return !!result;
      } catch (error) {
        console.error('MongoDB delete error:', error);
        throw error;
      }
    } else {
      const deliveryIndex = mockDataService.deliveries.findIndex(d => d.id == id);
      if (deliveryIndex !== -1) {
        mockDataService.deliveries.splice(deliveryIndex, 1);
        return true;
      }
      return false;
    }
  }

  // WAREHOUSE METHODS
  async getWarehouses() {
    if (await this.useDatabase()) {
      try {
        const warehouses = await MongoWarehouse.find().sort({ name: 1 });
        return warehouses.map(warehouse => warehouse.toJSON());
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getWarehouses();
      }
    } else {
      return mockDataService.getWarehouses();
    }
  }

  async getWarehouseById(id) {
    if (await this.useDatabase()) {
      try {
        const warehouse = await MongoWarehouse.findById(id);
        return warehouse ? warehouse.toJSON() : null;
      } catch (error) {
        console.error('MongoDB query error:', error);
        return mockDataService.getWarehouseById(id);
      }
    } else {
      return mockDataService.getWarehouseById(id);
    }
  }

  async createWarehouse(warehouseData) {
    if (await this.useDatabase()) {
      try {
        const warehouse = new MongoWarehouse(warehouseData);
        await warehouse.save();
        return warehouse.toJSON();
      } catch (error) {
        console.error('MongoDB save error:', error);
        throw error;
      }
    } else {
      const Warehouse = require('../models/Warehouse');
      const warehouse = new Warehouse(warehouseData);
      mockDataService.warehouses.push(warehouse);
      return warehouse.toJSON();
    }
  }

  async updateWarehouse(id, updateData) {
    if (await this.useDatabase()) {
      try {
        const warehouse = await MongoWarehouse.findByIdAndUpdate(id, updateData, { 
          new: true, 
          runValidators: true 
        });
        return warehouse ? warehouse.toJSON() : null;
      } catch (error) {
        console.error('MongoDB update error:', error);
        throw error;
      }
    } else {
      const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
      if (warehouseIndex !== -1) {
        Object.assign(mockDataService.warehouses[warehouseIndex], updateData);
        mockDataService.warehouses[warehouseIndex].updated_at = new Date();
        return mockDataService.warehouses[warehouseIndex].toJSON();
      }
      return null;
    }
  }

  async deleteWarehouse(id) {
    if (await this.useDatabase()) {
      try {
        const result = await MongoWarehouse.findByIdAndDelete(id);
        return !!result;
      } catch (error) {
        console.error('MongoDB delete error:', error);
        throw error;
      }
    } else {
      const warehouseIndex = mockDataService.warehouses.findIndex(w => w.id == id);
      if (warehouseIndex !== -1) {
        mockDataService.warehouses.splice(warehouseIndex, 1);
        return true;
      }
      return false;
    }
  }

  // INITIALIZATION METHOD
  async initializeSampleData() {
    if (await this.useDatabase()) {
      try {
        // Check if data already exists
        const orderCount = await MongoOrder.countDocuments();
        const productCount = await MongoProduct.countDocuments();
        
        if (orderCount === 0 && productCount === 0) {
          console.log('🌱 Initializing MongoDB with sample data...');
          
          // Initialize mock data service to generate sample data
          mockDataService.initialize();
          
          // Transfer mock data to MongoDB
          await this.transferMockDataToMongo();
          
          console.log('✅ Sample data initialized in MongoDB');
        } else {
          console.log(`📊 MongoDB already contains data: ${orderCount} orders, ${productCount} products`);
        }
      } catch (error) {
        console.error('❌ Error initializing sample data:', error);
      }
    } else {
      // Initialize mock data service
      mockDataService.initialize();
      console.log('📊 Mock data service initialized');
    }
  }

  async transferMockDataToMongo() {
    try {
      // Transfer products
      const products = mockDataService.products.map(p => ({
        sku: p.sku,
        name: p.name,
        category: p.category,
        price: p.price,
        cost: p.cost,
        stock_quantity: p.stock_quantity,
        reorder_level: p.reorder_level,
        supplier: p.supplier,
        description: p.description,
        location: p.location,
        status: p.status
      }));
      
      if (products.length > 0) {
        await MongoProduct.insertMany(products);
        console.log(`✅ Transferred ${products.length} products to MongoDB`);
      }

      // Transfer orders
      const orders = mockDataService.orders.map(o => ({
        order_id: o.order_id,
        customer_name: o.customer_name,
        customer_email: o.customer_email,
        product_id: o.product_id,
        product_name: o.product_name,
        quantity: o.quantity,
        price: o.price,
        status: o.status,
        order_date: o.order_date,
        delivery_address: o.delivery_address,
        payment_method: o.payment_method
      }));
      
      if (orders.length > 0) {
        await MongoOrder.insertMany(orders);
        console.log(`✅ Transferred ${orders.length} orders to MongoDB`);
      }

      // Transfer deliveries
      const deliveries = mockDataService.deliveries.map(d => ({
        delivery_id: d.delivery_id,
        order_id: d.order_id,
        driver_name: d.driver_name,
        vehicle_id: d.vehicle_id,
        pickup_address: d.pickup_address,
        delivery_address: d.delivery_address,
        pickup_time: d.pickup_time,
        estimated_delivery_time: d.estimated_delivery_time,
        actual_delivery_time: d.actual_delivery_time,
        status: d.status,
        priority: d.priority,
        notes: d.notes
      }));
      
      if (deliveries.length > 0) {
        await MongoDelivery.insertMany(deliveries);
        console.log(`✅ Transferred ${deliveries.length} deliveries to MongoDB`);
      }

      // Transfer warehouses
      const warehouses = mockDataService.warehouses.map(w => ({
        warehouse_id: w.warehouse_id,
        name: w.name,
        location: w.location,
        capacity: w.capacity,
        current_utilization: w.current_utilization,
        manager_name: w.manager_name,
        phone: w.phone,
        email: w.email,
        operating_hours: w.operating_hours,
        status: w.status,
        zones: w.zones
      }));
      
      if (warehouses.length > 0) {
        await MongoWarehouse.insertMany(warehouses);
        console.log(`✅ Transferred ${warehouses.length} warehouses to MongoDB`);
      }

    } catch (error) {
      console.error('❌ Error transferring data to MongoDB:', error);
      throw error;
    }
  }
}

// Create singleton instance
const databaseService = new DatabaseService();

module.exports = databaseService;

const express = require('express');
const router = express.Router();
const databaseService = require('../services/databaseService');
const Product = require('../models/Product');
const { Validator } = require('../utils/helpers');

/**
 * GET /api/inventory
 * Get all products with optional filtering
 */
router.get('/', async (req, res) => {
  try {
    const { category, low_stock, status, page = 1, limit = 50, search } = req.query;
    
    const filters = {};
    
    if (category) {
      filters.category = category;
    }
    
    if (low_stock === 'true') {
      filters.low_stock = true;
    }
    
    if (status) {
      filters.status = status;
    }
    
    if (search) {
      filters.search = search;
    }
    
    let products = await databaseService.getProducts(filters);
    
    // Transform MongoDB field names to frontend-compatible names
    const transformedProducts = products.map(product => ({
      ...product,
      quantity: product.stock_quantity || product.quantity || 0, // Map stock_quantity to quantity for frontend
      min_stock_level: product.reorder_level || product.min_stock_level || 0, // Map reorder_level to min_stock_level
      bin_location: product.location || product.bin_location || '', // Map location to bin_location
      last_restocked: product.last_updated || product.last_restocked || new Date().toISOString()
    }));
    
    // Pagination
    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;
    const paginatedProducts = transformedProducts.slice(startIndex, endIndex);
    
    res.json({
      success: true,
      data: paginatedProducts,
      pagination: {
        current_page: parseInt(page),
        total_pages: Math.ceil(transformedProducts.length / limit),
        total_items: transformedProducts.length,
        items_per_page: parseInt(limit)
      },
      filters_applied: filters
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch inventory',
      message: error.message
    });
  }
});

/**
 * GET /api/inventory/:id
 * Get a specific product by ID
 */
router.get('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const product = mockDataService.getProductById(id);
    
    if (!product) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }
    
    res.json({
      success: true,
      data: product
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch product',
      message: error.message
    });
  }
});

/**
 * POST /api/inventory
 * Create a new product
 */
router.post('/', (req, res) => {
  try {
    const productData = req.body;
    
    // Validate required fields
    const requiredFields = ['name', 'category', 'price', 'cost', 'stock_quantity'];
    const missingFields = Validator.validateRequired(productData, requiredFields);
    
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        missing_fields: missingFields
      });
    }
    
    // Validate numeric fields
    if (!Validator.isPositiveNumber(productData.price) || 
        !Validator.isPositiveNumber(productData.cost) ||
        !Validator.isNonNegativeNumber(productData.stock_quantity)) {
      return res.status(400).json({
        success: false,
        error: 'Price and cost must be positive numbers, stock quantity must be non-negative'
      });
    }
    
    // Validate category
    if (!Product.getCategories().includes(productData.category)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid category',
        valid_categories: Product.getCategories()
      });
    }
    
    // Create new product
    const product = new Product({
      name: Validator.sanitizeString(productData.name),
      category: productData.category,
      price: parseFloat(productData.price),
      cost: parseFloat(productData.cost),
      stock_quantity: parseInt(productData.stock_quantity),
      reorder_level: parseInt(productData.reorder_level) || 10,
      supplier: Validator.sanitizeString(productData.supplier) || 'Unknown',
      description: Validator.sanitizeString(productData.description) || '',
      location: Validator.sanitizeString(productData.location) || ''
    });
    
    // Add to mock data
    mockDataService.products.push(product);
    
    res.status(201).json({
      success: true,
      message: 'Product created successfully',
      data: product.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to create product',
      message: error.message
    });
  }
});

/**
 * PUT /api/inventory/:id
 * Update an existing product
 */
router.put('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const updateData = req.body;
    
    const productIndex = mockDataService.products.findIndex(p => p.id == id);
    
    if (productIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }
    
    const product = mockDataService.products[productIndex];
    
    // Update allowed fields
    if (updateData.name) {
      product.name = Validator.sanitizeString(updateData.name);
      product.updated_at = new Date();
    }
    
    if (updateData.price && Validator.isPositiveNumber(updateData.price)) {
      product.price = parseFloat(updateData.price);
      product.updated_at = new Date();
    }
    
    if (updateData.cost && Validator.isPositiveNumber(updateData.cost)) {
      product.cost = parseFloat(updateData.cost);
      product.updated_at = new Date();
    }
    
    if (updateData.stock_quantity !== undefined && Validator.isNonNegativeNumber(updateData.stock_quantity)) {
      product.stock_quantity = parseInt(updateData.stock_quantity);
      product.updated_at = new Date();
    }
    
    if (updateData.reorder_level && Validator.isNonNegativeNumber(updateData.reorder_level)) {
      product.reorder_level = parseInt(updateData.reorder_level);
      product.updated_at = new Date();
    }
    
    if (updateData.supplier) {
      product.supplier = Validator.sanitizeString(updateData.supplier);
      product.updated_at = new Date();
    }
    
    if (updateData.description !== undefined) {
      product.description = Validator.sanitizeString(updateData.description);
      product.updated_at = new Date();
    }
    
    if (updateData.location !== undefined) {
      product.location = Validator.sanitizeString(updateData.location);
      product.updated_at = new Date();
    }
    
    if (updateData.status && Product.getValidStatuses().includes(updateData.status)) {
      product.status = updateData.status;
      product.updated_at = new Date();
    }
    
    res.json({
      success: true,
      message: 'Product updated successfully',
      data: product.toJSON()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update product',
      message: error.message
    });
  }
});

/**
 * DELETE /api/inventory/:id
 * Delete a product
 */
router.delete('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const productIndex = mockDataService.products.findIndex(p => p.id == id);
    
    if (productIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }
    
    mockDataService.products.splice(productIndex, 1);
    
    res.json({
      success: true,
      message: 'Product deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to delete product',
      message: error.message
    });
  }
});

/**
 * PATCH /api/inventory/:id/stock
 * Update product stock
 */
router.patch('/:id/stock', (req, res) => {
  try {
    const { id } = req.params;
    const { quantity, operation = 'set' } = req.body;
    
    if (quantity === undefined || !Validator.isNonNegativeNumber(quantity)) {
      return res.status(400).json({
        success: false,
        error: 'Valid quantity is required'
      });
    }
    
    const validOperations = ['add', 'subtract', 'set'];
    if (!validOperations.includes(operation)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid operation',
        valid_operations: validOperations
      });
    }
    
    const productIndex = mockDataService.products.findIndex(p => p.id == id);
    
    if (productIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }
    
    const product = mockDataService.products[productIndex];
    const newStock = product.updateStock(parseInt(quantity), operation);
    
    res.json({
      success: true,
      message: 'Stock updated successfully',
      data: {
        product_id: product.id,
        sku: product.sku,
        name: product.name,
        previous_stock: operation === 'set' ? quantity : (operation === 'add' ? newStock - quantity : newStock + quantity),
        new_stock: newStock,
        operation: operation,
        quantity_changed: quantity
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to update stock',
      message: error.message
    });
  }
});

/**
 * GET /api/inventory/analytics/summary
 * Get inventory analytics and summary
 */
router.get('/analytics/summary', (req, res) => {
  try {
    const analytics = mockDataService.getInventoryAnalytics();
    
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
 * GET /api/inventory/low-stock
 * Get products with low stock
 */
router.get('/low-stock', (req, res) => {
  try {
    const products = mockDataService.getProducts({ low_stock: true });
    
    res.json({
      success: true,
      data: products,
      count: products.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch low stock products',
      message: error.message
    });
  }
});

/**
 * GET /api/inventory/categories
 * Get available product categories
 */
router.get('/categories', (req, res) => {
  try {
    const categories = Product.getCategories();
    
    res.json({
      success: true,
      data: categories
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to fetch categories',
      message: error.message
    });
  }
});

module.exports = router;

class Product {
  constructor({
    id = null,
    sku,
    name,
    category,
    price,
    cost,
    stock_quantity,
    reorder_level = 10,
    supplier,
    description = '',
    location = '',
    status = 'active'
  }) {
    this.id = id || this.generateId();
    this.sku = sku || this.generateSKU();
    this.name = name;
    this.category = category;
    this.price = price;
    this.cost = cost;
    this.stock_quantity = stock_quantity;
    this.reorder_level = reorder_level;
    this.supplier = supplier;
    this.description = description;
    this.location = location;
    this.status = status;
    this.created_at = new Date();
    this.updated_at = new Date();
  }

  generateId() {
    return Math.floor(Math.random() * 10000) + 1;
  }

  generateSKU() {
    const prefix = 'PROD';
    const random = Math.floor(Math.random() * 9999) + 1;
    return `${prefix}-${random}`;
  }

  updateStock(quantity, operation = 'add') {
    if (operation === 'add') {
      this.stock_quantity += quantity;
    } else if (operation === 'subtract') {
      this.stock_quantity = Math.max(0, this.stock_quantity - quantity);
    } else if (operation === 'set') {
      this.stock_quantity = Math.max(0, quantity);
    }
    this.updated_at = new Date();
    return this.stock_quantity;
  }

  getStockStatus() {
    if (this.stock_quantity === 0) {
      return 'out_of_stock';
    } else if (this.stock_quantity <= this.reorder_level) {
      return 'low_stock';
    } else {
      return 'in_stock';
    }
  }

  calculateMargin() {
    if (this.cost && this.price) {
      return (((this.price - this.cost) / this.price) * 100).toFixed(2);
    }
    return 0;
  }

  getStockValue() {
    return (this.stock_quantity * this.cost).toFixed(2);
  }

  isLowStock() {
    return this.stock_quantity <= this.reorder_level;
  }

  static getCategories() {
    return [
      'Electronics',
      'Clothing',
      'Home & Garden',
      'Sports & Outdoors',
      'Health & Beauty',
      'Books',
      'Toys & Games',
      'Automotive',
      'Food & Beverage',
      'Office Supplies'
    ];
  }

  static getValidStatuses() {
    return ['active', 'inactive', 'discontinued'];
  }

  toJSON() {
    return {
      id: this.id,
      sku: this.sku,
      name: this.name,
      category: this.category,
      price: this.price,
      cost: this.cost,
      stock_quantity: this.stock_quantity,
      reorder_level: this.reorder_level,
      supplier: this.supplier,
      description: this.description,
      location: this.location,
      status: this.status,
      stock_status: this.getStockStatus(),
      margin: this.calculateMargin(),
      stock_value: this.getStockValue(),
      is_low_stock: this.isLowStock(),
      created_at: this.created_at,
      updated_at: this.updated_at
    };
  }
}

module.exports = Product;

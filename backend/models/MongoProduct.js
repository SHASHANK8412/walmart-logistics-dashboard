const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  sku: {
    type: String,
    required: true,
    unique: true,
    uppercase: true,
    index: true
  },
  name: {
    type: String,
    required: true,
    trim: true
  },
  category: {
    type: String,
    required: true,
    enum: [
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
    ]
  },
  price: {
    type: Number,
    required: true,
    min: 0
  },
  cost: {
    type: Number,
    required: true,
    min: 0
  },
  stock_quantity: {
    type: Number,
    required: true,
    min: 0,
    default: 0
  },
  reorder_level: {
    type: Number,
    required: true,
    min: 0,
    default: 10
  },
  supplier: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    trim: true,
    default: ''
  },
  location: {
    type: String,
    trim: true,
    default: ''
  },
  status: {
    type: String,
    required: true,
    enum: ['active', 'inactive', 'discontinued'],
    default: 'active'
  },
  weight: {
    type: Number,
    min: 0
  },
  dimensions: {
    length: Number,
    width: Number,
    height: Number
  },
  tags: [{
    type: String,
    trim: true
  }]
}, {
  timestamps: true,
  toJSON: { 
    virtuals: true,
    transform: function(doc, ret) {
      ret.id = ret._id;
      delete ret._id;
      delete ret.__v;
      return ret;
    }
  }
});

// Virtual fields
productSchema.virtual('stock_status').get(function() {
  if (this.stock_quantity === 0) {
    return 'out_of_stock';
  } else if (this.stock_quantity <= this.reorder_level) {
    return 'low_stock';
  } else {
    return 'in_stock';
  }
});

productSchema.virtual('margin').get(function() {
  if (this.cost && this.price) {
    return (((this.price - this.cost) / this.price) * 100).toFixed(2);
  }
  return '0.00';
});

productSchema.virtual('stock_value').get(function() {
  return (this.stock_quantity * this.cost).toFixed(2);
});

productSchema.virtual('is_low_stock').get(function() {
  return this.stock_quantity <= this.reorder_level;
});

// Indexes for better query performance
productSchema.index({ category: 1 });
productSchema.index({ status: 1 });
productSchema.index({ stock_quantity: 1 });
productSchema.index({ name: 'text', description: 'text' });

// Pre-save middleware to generate SKU if not provided
productSchema.pre('save', function(next) {
  if (!this.sku) {
    const prefix = 'PROD';
    const random = Math.floor(Math.random() * 9999) + 1;
    this.sku = `${prefix}-${random}`;
  }
  next();
});

// Static methods
productSchema.statics.getCategories = function() {
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
};

productSchema.statics.getValidStatuses = function() {
  return ['active', 'inactive', 'discontinued'];
};

productSchema.statics.getInventoryAnalytics = async function() {
  const analytics = await this.aggregate([
    {
      $facet: {
        totals: [
          {
            $group: {
              _id: null,
              total_products: { $sum: 1 },
              low_stock_items: {
                $sum: { $cond: [{ $lte: ['$stock_quantity', '$reorder_level'] }, 1, 0] }
              },
              out_of_stock_items: {
                $sum: { $cond: [{ $eq: ['$stock_quantity', 0] }, 1, 0] }
              },
              total_inventory_value: {
                $sum: { $multiply: ['$stock_quantity', '$cost'] }
              }
            }
          }
        ],
        by_category: [
          {
            $group: {
              _id: '$category',
              count: { $sum: 1 },
              total_value: { $sum: { $multiply: ['$stock_quantity', '$cost'] } }
            }
          }
        ]
      }
    }
  ]);

  const result = analytics[0];
  const totals = result.totals[0] || {
    total_products: 0,
    low_stock_items: 0,
    out_of_stock_items: 0,
    total_inventory_value: 0
  };

  return {
    ...totals,
    total_inventory_value: totals.total_inventory_value.toFixed(2),
    by_category: result.by_category
  };
};

// Instance methods
productSchema.methods.updateStock = function(quantity, operation = 'set') {
  switch (operation) {
    case 'add':
      this.stock_quantity += quantity;
      break;
    case 'subtract':
      this.stock_quantity = Math.max(0, this.stock_quantity - quantity);
      break;
    case 'set':
    default:
      this.stock_quantity = Math.max(0, quantity);
      break;
  }
  return this.stock_quantity;
};

module.exports = mongoose.model('Product', productSchema);

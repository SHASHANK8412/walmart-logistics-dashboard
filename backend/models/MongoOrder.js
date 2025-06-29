const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
  order_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  customer_name: {
    type: String,
    required: true,
    trim: true
  },
  customer_email: {
    type: String,
    required: true,
    lowercase: true,
    trim: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  product_id: {
    type: String,
    required: true
  },
  product_name: {
    type: String,
    required: true,
    trim: true
  },
  quantity: {
    type: Number,
    required: true,
    min: 1
  },
  price: {
    type: Number,
    required: true,
    min: 0
  },
  status: {
    type: String,
    required: true,
    enum: ['pending', 'shipped', 'delivered', 'cancelled'],
    default: 'pending'
  },
  order_date: {
    type: Date,
    default: Date.now
  },
  delivery_address: {
    type: String,
    required: true,
    trim: true
  },
  payment_method: {
    type: String,
    required: true,
    enum: ['Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery'],
    default: 'Credit Card'
  },
  notes: {
    type: String,
    trim: true,
    default: ''
  },
  tracking_number: {
    type: String,
    sparse: true
  }
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

// Virtual for total amount
orderSchema.virtual('total').get(function() {
  return (this.quantity * this.price).toFixed(2);
});

// Indexes for better query performance
orderSchema.index({ status: 1 });
orderSchema.index({ order_date: -1 });
orderSchema.index({ customer_email: 1 });
orderSchema.index({ product_id: 1 });

// Pre-save middleware to generate order_id if not provided
orderSchema.pre('save', function(next) {
  if (!this.order_id) {
    const year = new Date().getFullYear();
    const random = Math.floor(Math.random() * 9999) + 1;
    this.order_id = `ORD-${year}${random.toString().padStart(3, '0')}`;
  }
  next();
});

// Static methods
orderSchema.statics.getValidStatuses = function() {
  return ['pending', 'shipped', 'delivered', 'cancelled'];
};

orderSchema.statics.getPaymentMethods = function() {
  return ['Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery'];
};

orderSchema.statics.getOrdersAnalytics = async function() {
  const analytics = await this.aggregate([
    {
      $group: {
        _id: null,
        total_orders: { $sum: 1 },
        pending_orders: {
          $sum: { $cond: [{ $eq: ['$status', 'pending'] }, 1, 0] }
        },
        shipped_orders: {
          $sum: { $cond: [{ $eq: ['$status', 'shipped'] }, 1, 0] }
        },
        delivered_orders: {
          $sum: { $cond: [{ $eq: ['$status', 'delivered'] }, 1, 0] }
        },
        cancelled_orders: {
          $sum: { $cond: [{ $eq: ['$status', 'cancelled'] }, 1, 0] }
        },
        total_revenue: {
          $sum: {
            $cond: [
              { $eq: ['$status', 'delivered'] },
              { $multiply: ['$quantity', '$price'] },
              0
            ]
          }
        }
      }
    }
  ]);

  if (analytics.length === 0) {
    return {
      total_orders: 0,
      pending_orders: 0,
      shipped_orders: 0,
      delivered_orders: 0,
      cancelled_orders: 0,
      total_revenue: '0.00'
    };
  }

  const result = analytics[0];
  result.total_revenue = result.total_revenue.toFixed(2);
  delete result._id;
  return result;
};

// Instance methods
orderSchema.methods.updateStatus = function(newStatus) {
  const validStatuses = this.constructor.getValidStatuses();
  if (validStatuses.includes(newStatus)) {
    this.status = newStatus;
    return true;
  }
  return false;
};

module.exports = mongoose.model('Order', orderSchema);

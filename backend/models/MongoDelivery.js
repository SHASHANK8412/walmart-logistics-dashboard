const mongoose = require('mongoose');

const deliverySchema = new mongoose.Schema({
  delivery_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  order_id: {
    type: String,
    required: true,
    index: true
  },
  driver_name: {
    type: String,
    required: true,
    trim: true
  },
  vehicle_id: {
    type: String,
    required: true,
    trim: true
  },
  pickup_address: {
    type: String,
    required: true,
    trim: true
  },
  delivery_address: {
    type: String,
    required: true,
    trim: true
  },
  pickup_time: {
    type: Date
  },
  estimated_delivery_time: {
    type: Date
  },
  actual_delivery_time: {
    type: Date
  },
  status: {
    type: String,
    required: true,
    enum: ['pending', 'picked_up', 'in_transit', 'delivered', 'failed', 'cancelled'],
    default: 'pending'
  },
  priority: {
    type: String,
    required: true,
    enum: ['low', 'normal', 'high', 'urgent'],
    default: 'normal'
  },
  notes: {
    type: String,
    trim: true,
    default: ''
  },
  delivery_proof: {
    signature: String,
    photo_url: String,
    recipient_name: String
  },
  coordinates: {
    pickup: {
      latitude: Number,
      longitude: Number
    },
    delivery: {
      latitude: Number,
      longitude: Number
    }
  },
  distance_km: {
    type: Number,
    min: 0
  },
  estimated_duration_minutes: {
    type: Number,
    min: 0
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

// Virtual fields
deliverySchema.virtual('delivery_time_minutes').get(function() {
  if (this.pickup_time && this.actual_delivery_time) {
    const diffMs = new Date(this.actual_delivery_time) - new Date(this.pickup_time);
    return Math.round(diffMs / (1000 * 60));
  }
  return null;
});

deliverySchema.virtual('is_delayed').get(function() {
  if (this.estimated_delivery_time && this.status !== 'delivered') {
    return new Date() > new Date(this.estimated_delivery_time);
  }
  return false;
});

deliverySchema.virtual('delivery_window').get(function() {
  if (this.estimated_delivery_time) {
    const estimated = new Date(this.estimated_delivery_time);
    const start = new Date(estimated.getTime() - 30 * 60000); // 30 minutes before
    const end = new Date(estimated.getTime() + 30 * 60000); // 30 minutes after
    return { start, end };
  }
  return null;
});

// Indexes for better query performance
deliverySchema.index({ status: 1 });
deliverySchema.index({ driver_name: 1 });
deliverySchema.index({ priority: 1 });
deliverySchema.index({ pickup_time: 1 });
deliverySchema.index({ estimated_delivery_time: 1 });

// Pre-save middleware to generate delivery_id if not provided
deliverySchema.pre('save', function(next) {
  if (!this.delivery_id) {
    const prefix = 'DEL';
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const random = Math.floor(Math.random() * 999) + 1;
    this.delivery_id = `${prefix}-${date}-${random.toString().padStart(3, '0')}`;
  }
  next();
});

// Pre-save middleware to set timestamps based on status
deliverySchema.pre('save', function(next) {
  if (this.isModified('status')) {
    if (this.status === 'picked_up' && !this.pickup_time) {
      this.pickup_time = new Date();
    }
    if (this.status === 'delivered' && !this.actual_delivery_time) {
      this.actual_delivery_time = new Date();
    }
  }
  next();
});

// Static methods
deliverySchema.statics.getValidStatuses = function() {
  return ['pending', 'picked_up', 'in_transit', 'delivered', 'failed', 'cancelled'];
};

deliverySchema.statics.getPriorityLevels = function() {
  return ['low', 'normal', 'high', 'urgent'];
};

deliverySchema.statics.getPerformanceAnalytics = async function() {
  const analytics = await this.aggregate([
    {
      $facet: {
        status_counts: [
          {
            $group: {
              _id: '$status',
              count: { $sum: 1 }
            }
          }
        ],
        timing_stats: [
          {
            $match: {
              pickup_time: { $exists: true },
              actual_delivery_time: { $exists: true }
            }
          },
          {
            $addFields: {
              delivery_time_minutes: {
                $divide: [
                  { $subtract: ['$actual_delivery_time', '$pickup_time'] },
                  60000
                ]
              }
            }
          },
          {
            $group: {
              _id: null,
              avg_delivery_time: { $avg: '$delivery_time_minutes' },
              min_delivery_time: { $min: '$delivery_time_minutes' },
              max_delivery_time: { $max: '$delivery_time_minutes' },
              total_completed: { $sum: 1 }
            }
          }
        ],
        driver_stats: [
          {
            $group: {
              _id: '$driver_name',
              total_deliveries: { $sum: 1 },
              completed_deliveries: {
                $sum: { $cond: [{ $eq: ['$status', 'delivered'] }, 1, 0] }
              }
            }
          }
        ]
      }
    }
  ]);

  const result = analytics[0];
  
  // Process status counts
  const statusCounts = {};
  result.status_counts.forEach(item => {
    statusCounts[item._id] = item.count;
  });

  // Process timing stats
  const timingStats = result.timing_stats[0] || {};

  return {
    total_deliveries: Object.values(statusCounts).reduce((sum, count) => sum + count, 0),
    ...statusCounts,
    average_delivery_time_minutes: timingStats.avg_delivery_time ? Math.round(timingStats.avg_delivery_time) : 0,
    driver_performance: result.driver_stats
  };
};

// Instance methods
deliverySchema.methods.updateStatus = function(newStatus) {
  const validStatuses = this.constructor.getValidStatuses();
  if (validStatuses.includes(newStatus)) {
    this.status = newStatus;
    return true;
  }
  return false;
};

module.exports = mongoose.model('Delivery', deliverySchema);

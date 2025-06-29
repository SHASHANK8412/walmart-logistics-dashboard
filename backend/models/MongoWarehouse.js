const mongoose = require('mongoose');

const zoneSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  type: {
    type: String,
    required: true,
    enum: ['general', 'cold_storage', 'hazardous', 'fragile', 'bulk', 'electronics'],
    default: 'general'
  },
  capacity: {
    type: Number,
    required: true,
    min: 0
  },
  current_stock: {
    type: Number,
    required: true,
    min: 0,
    default: 0
  },
  temperature_controlled: {
    type: Boolean,
    default: false
  },
  temperature_range: {
    min: Number,
    max: Number
  },
  created_at: {
    type: Date,
    default: Date.now
  }
});

// Virtual for zone utilization
zoneSchema.virtual('utilization_percentage').get(function() {
  if (this.capacity > 0) {
    return ((this.current_stock / this.capacity) * 100).toFixed(2);
  }
  return '0.00';
});

const warehouseSchema = new mongoose.Schema({
  warehouse_id: {
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
  location: {
    type: String,
    required: true,
    trim: true
  },
  address: {
    street: String,
    city: String,
    state: String,
    zipCode: String,
    country: { type: String, default: 'USA' }
  },
  coordinates: {
    latitude: Number,
    longitude: Number
  },
  capacity: {
    type: Number,
    required: true,
    min: 0
  },
  current_utilization: {
    type: Number,
    required: true,
    min: 0,
    default: 0
  },
  manager_name: {
    type: String,
    required: true,
    trim: true
  },
  phone: {
    type: String,
    trim: true,
    match: [/^[\+]?[1-9][\d]{0,15}$/, 'Please enter a valid phone number']
  },
  email: {
    type: String,
    lowercase: true,
    trim: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  operating_hours: {
    start: {
      type: String,
      required: true,
      default: '08:00'
    },
    end: {
      type: String,
      required: true,
      default: '18:00'
    }
  },
  status: {
    type: String,
    required: true,
    enum: ['active', 'maintenance', 'closed', 'inactive'],
    default: 'active'
  },
  zones: [zoneSchema],
  equipment: [{
    name: String,
    type: String,
    quantity: Number,
    status: {
      type: String,
      enum: ['operational', 'maintenance', 'broken'],
      default: 'operational'
    }
  }],
  certifications: [String],
  security_level: {
    type: String,
    enum: ['basic', 'standard', 'high', 'maximum'],
    default: 'standard'
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
warehouseSchema.virtual('utilization_percentage').get(function() {
  if (this.capacity > 0) {
    return ((this.current_utilization / this.capacity) * 100).toFixed(2);
  }
  return '0.00';
});

warehouseSchema.virtual('available_capacity').get(function() {
  return Math.max(0, this.capacity - this.current_utilization);
});

warehouseSchema.virtual('is_near_capacity').get(function() {
  return parseFloat(this.utilization_percentage) >= 90;
});

warehouseSchema.virtual('is_operational').get(function() {
  const now = new Date();
  const currentHour = now.getHours().toString().padStart(2, '0') + ':' + 
                     now.getMinutes().toString().padStart(2, '0');
  
  return this.status === 'active' && 
         currentHour >= this.operating_hours.start && 
         currentHour <= this.operating_hours.end;
});

// Indexes for better query performance
warehouseSchema.index({ status: 1 });
warehouseSchema.index({ location: 1 });
warehouseSchema.index({ 'coordinates.latitude': 1, 'coordinates.longitude': 1 });

// Pre-save middleware to generate warehouse_id if not provided
warehouseSchema.pre('save', function(next) {
  if (!this.warehouse_id) {
    const prefix = 'WH';
    const random = Math.floor(Math.random() * 999) + 1;
    this.warehouse_id = `${prefix}-${random.toString().padStart(3, '0')}`;
  }
  next();
});

// Pre-save middleware to validate utilization doesn't exceed capacity
warehouseSchema.pre('save', function(next) {
  if (this.current_utilization > this.capacity) {
    const err = new Error('Current utilization cannot exceed warehouse capacity');
    err.name = 'ValidationError';
    return next(err);
  }
  next();
});

// Static methods
warehouseSchema.statics.getValidStatuses = function() {
  return ['active', 'maintenance', 'closed', 'inactive'];
};

warehouseSchema.statics.getZoneTypes = function() {
  return ['general', 'cold_storage', 'hazardous', 'fragile', 'bulk', 'electronics'];
};

warehouseSchema.statics.getUtilizationAnalytics = async function() {
  const analytics = await this.aggregate([
    {
      $group: {
        _id: null,
        total_warehouses: { $sum: 1 },
        total_capacity: { $sum: '$capacity' },
        total_utilization: { $sum: '$current_utilization' },
        near_capacity_count: {
          $sum: {
            $cond: [
              { $gte: [{ $divide: ['$current_utilization', '$capacity'] }, 0.9] },
              1,
              0
            ]
          }
        },
        active_warehouses: {
          $sum: { $cond: [{ $eq: ['$status', 'active'] }, 1, 0] }
        }
      }
    }
  ]);

  const warehouseDetails = await this.find({}, {
    warehouse_id: 1,
    name: 1,
    location: 1,
    capacity: 1,
    current_utilization: 1,
    status: 1
  });

  const result = analytics[0] || {
    total_warehouses: 0,
    total_capacity: 0,
    total_utilization: 0,
    near_capacity_count: 0,
    active_warehouses: 0
  };

  const overall_utilization = result.total_capacity > 0 
    ? ((result.total_utilization / result.total_capacity) * 100).toFixed(2)
    : '0.00';

  return {
    ...result,
    overall_utilization_percentage: overall_utilization,
    warehouse_details: warehouseDetails.map(w => ({
      warehouse_id: w.warehouse_id,
      name: w.name,
      location: w.location,
      utilization_percentage: w.capacity > 0 
        ? ((w.current_utilization / w.capacity) * 100).toFixed(2)
        : '0.00',
      is_near_capacity: w.capacity > 0 && (w.current_utilization / w.capacity) >= 0.9,
      available_capacity: Math.max(0, w.capacity - w.current_utilization),
      status: w.status
    }))
  };
};

// Instance methods
warehouseSchema.methods.updateUtilization = function(newUtilization) {
  if (newUtilization >= 0 && newUtilization <= this.capacity) {
    this.current_utilization = newUtilization;
    return true;
  }
  return false;
};

warehouseSchema.methods.addZone = function(zoneData) {
  this.zones.push({
    name: zoneData.name,
    type: zoneData.type || 'general',
    capacity: zoneData.capacity || 0,
    current_stock: zoneData.current_stock || 0,
    temperature_controlled: zoneData.temperature_controlled || false,
    temperature_range: zoneData.temperature_range
  });
};

warehouseSchema.methods.removeZone = function(zoneId) {
  this.zones = this.zones.filter(zone => zone._id.toString() !== zoneId.toString());
};

warehouseSchema.methods.getZoneUtilization = function() {
  return this.zones.map(zone => ({
    ...zone.toObject(),
    utilization_percentage: zone.capacity > 0 
      ? ((zone.current_stock / zone.capacity) * 100).toFixed(2)
      : '0.00'
  }));
};

module.exports = mongoose.model('Warehouse', warehouseSchema);

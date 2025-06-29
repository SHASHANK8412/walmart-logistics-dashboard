class Delivery {
  constructor({
    id = null,
    delivery_id = null,
    order_id,
    driver_name,
    vehicle_id,
    pickup_address,
    delivery_address,
    pickup_time = null,
    estimated_delivery_time = null,
    actual_delivery_time = null,
    status = 'pending',
    notes = '',
    priority = 'normal'
  }) {
    this.id = id || this.generateId();
    this.delivery_id = delivery_id || this.generateDeliveryId();
    this.order_id = order_id;
    this.driver_name = driver_name;
    this.vehicle_id = vehicle_id;
    this.pickup_address = pickup_address;
    this.delivery_address = delivery_address;
    this.pickup_time = pickup_time;
    this.estimated_delivery_time = estimated_delivery_time;
    this.actual_delivery_time = actual_delivery_time;
    this.status = status;
    this.notes = notes;
    this.priority = priority;
    this.created_at = new Date();
    this.updated_at = new Date();
  }

  generateId() {
    return Math.floor(Math.random() * 10000) + 1;
  }

  generateDeliveryId() {
    const prefix = 'DEL';
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const random = Math.floor(Math.random() * 999) + 1;
    return `${prefix}-${date}-${random.toString().padStart(3, '0')}`;
  }

  updateStatus(newStatus) {
    const validStatuses = ['pending', 'picked_up', 'in_transit', 'delivered', 'failed', 'cancelled'];
    if (validStatuses.includes(newStatus)) {
      this.status = newStatus;
      this.updated_at = new Date();
      
      // Auto-set timestamps based on status
      if (newStatus === 'picked_up' && !this.pickup_time) {
        this.pickup_time = new Date();
      }
      if (newStatus === 'delivered' && !this.actual_delivery_time) {
        this.actual_delivery_time = new Date();
      }
      
      return true;
    }
    return false;
  }

  calculateDeliveryTime() {
    if (this.pickup_time && this.actual_delivery_time) {
      const diffMs = new Date(this.actual_delivery_time) - new Date(this.pickup_time);
      return Math.round(diffMs / (1000 * 60)); // minutes
    }
    return null;
  }

  isDelayed() {
    if (this.estimated_delivery_time && this.status !== 'delivered') {
      return new Date() > new Date(this.estimated_delivery_time);
    }
    return false;
  }

  getDeliveryWindow() {
    if (this.estimated_delivery_time) {
      const estimated = new Date(this.estimated_delivery_time);
      const start = new Date(estimated.getTime() - 30 * 60000); // 30 minutes before
      const end = new Date(estimated.getTime() + 30 * 60000); // 30 minutes after
      return { start, end };
    }
    return null;
  }

  static getValidStatuses() {
    return ['pending', 'picked_up', 'in_transit', 'delivered', 'failed', 'cancelled'];
  }

  static getPriorityLevels() {
    return ['low', 'normal', 'high', 'urgent'];
  }

  toJSON() {
    return {
      id: this.id,
      delivery_id: this.delivery_id,
      order_id: this.order_id,
      driver_name: this.driver_name,
      vehicle_id: this.vehicle_id,
      pickup_address: this.pickup_address,
      delivery_address: this.delivery_address,
      pickup_time: this.pickup_time,
      estimated_delivery_time: this.estimated_delivery_time,
      actual_delivery_time: this.actual_delivery_time,
      status: this.status,
      notes: this.notes,
      priority: this.priority,
      delivery_time_minutes: this.calculateDeliveryTime(),
      is_delayed: this.isDelayed(),
      delivery_window: this.getDeliveryWindow(),
      created_at: this.created_at,
      updated_at: this.updated_at
    };
  }
}

module.exports = Delivery;

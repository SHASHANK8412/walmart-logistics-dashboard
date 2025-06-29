class Warehouse {
  constructor({
    id = null,
    warehouse_id = null,
    name,
    location,
    capacity,
    current_utilization = 0,
    manager_name,
    phone,
    email,
    operating_hours = { start: '08:00', end: '18:00' },
    status = 'active',
    zones = []
  }) {
    this.id = id || this.generateId();
    this.warehouse_id = warehouse_id || this.generateWarehouseId();
    this.name = name;
    this.location = location;
    this.capacity = capacity;
    this.current_utilization = current_utilization;
    this.manager_name = manager_name;
    this.phone = phone;
    this.email = email;
    this.operating_hours = operating_hours;
    this.status = status;
    this.zones = zones;
    this.created_at = new Date();
    this.updated_at = new Date();
  }

  generateId() {
    return Math.floor(Math.random() * 1000) + 1;
  }

  generateWarehouseId() {
    const prefix = 'WH';
    const random = Math.floor(Math.random() * 999) + 1;
    return `${prefix}-${random.toString().padStart(3, '0')}`;
  }

  updateUtilization(newUtilization) {
    if (newUtilization >= 0 && newUtilization <= this.capacity) {
      this.current_utilization = newUtilization;
      this.updated_at = new Date();
      return true;
    }
    return false;
  }

  getUtilizationPercentage() {
    if (this.capacity > 0) {
      return ((this.current_utilization / this.capacity) * 100).toFixed(2);
    }
    return 0;
  }

  getAvailableCapacity() {
    return Math.max(0, this.capacity - this.current_utilization);
  }

  isNearCapacity(threshold = 90) {
    return this.getUtilizationPercentage() >= threshold;
  }

  addZone(zone) {
    this.zones.push({
      id: this.zones.length + 1,
      name: zone.name,
      type: zone.type || 'general',
      capacity: zone.capacity || 0,
      current_stock: zone.current_stock || 0,
      temperature_controlled: zone.temperature_controlled || false,
      created_at: new Date()
    });
    this.updated_at = new Date();
  }

  removeZone(zoneId) {
    this.zones = this.zones.filter(zone => zone.id !== zoneId);
    this.updated_at = new Date();
  }

  getZoneUtilization() {
    return this.zones.map(zone => ({
      ...zone,
      utilization_percentage: zone.capacity > 0 
        ? ((zone.current_stock / zone.capacity) * 100).toFixed(2)
        : 0
    }));
  }

  isOperational() {
    const now = new Date();
    const currentHour = now.getHours().toString().padStart(2, '0') + ':' + 
                       now.getMinutes().toString().padStart(2, '0');
    
    return this.status === 'active' && 
           currentHour >= this.operating_hours.start && 
           currentHour <= this.operating_hours.end;
  }

  static getValidStatuses() {
    return ['active', 'maintenance', 'closed', 'inactive'];
  }

  static getZoneTypes() {
    return ['general', 'cold_storage', 'hazardous', 'fragile', 'bulk', 'electronics'];
  }

  toJSON() {
    return {
      id: this.id,
      warehouse_id: this.warehouse_id,
      name: this.name,
      location: this.location,
      capacity: this.capacity,
      current_utilization: this.current_utilization,
      manager_name: this.manager_name,
      phone: this.phone,
      email: this.email,
      operating_hours: this.operating_hours,
      status: this.status,
      zones: this.getZoneUtilization(),
      utilization_percentage: this.getUtilizationPercentage(),
      available_capacity: this.getAvailableCapacity(),
      is_near_capacity: this.isNearCapacity(),
      is_operational: this.isOperational(),
      created_at: this.created_at,
      updated_at: this.updated_at
    };
  }
}

module.exports = Warehouse;

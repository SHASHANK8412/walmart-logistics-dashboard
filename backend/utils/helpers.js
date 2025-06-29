const moment = require('moment');

/**
 * Utility functions for data validation
 */
class Validator {
  static isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  static isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s|-|\(|\)/g, ''));
  }

  static isValidDate(date) {
    return moment(date).isValid();
  }

  static isPositiveNumber(value) {
    return typeof value === 'number' && value > 0;
  }

  static isNonNegativeNumber(value) {
    return typeof value === 'number' && value >= 0;
  }

  static isValidStatus(status, validStatuses) {
    return validStatuses.includes(status);
  }

  static sanitizeString(str) {
    if (typeof str !== 'string') return '';
    return str.trim().replace(/[<>]/g, '');
  }

  static validateRequired(obj, requiredFields) {
    const missing = [];
    requiredFields.forEach(field => {
      if (!obj[field] || (typeof obj[field] === 'string' && obj[field].trim() === '')) {
        missing.push(field);
      }
    });
    return missing;
  }
}

/**
 * Utility functions for data formatting
 */
class Formatter {
  static formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(amount);
  }

  static formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
    return moment(date).format(format);
  }

  static formatPercentage(value, decimals = 2) {
    return `${parseFloat(value).toFixed(decimals)}%`;
  }

  static formatWeight(weight, unit = 'kg') {
    return `${parseFloat(weight).toFixed(2)} ${unit}`;
  }

  static formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  }

  static truncateText(text, maxLength = 100) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }
}

/**
 * Utility functions for calculations
 */
class Calculator {
  static calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in kilometers
  }

  static calculateTax(amount, taxRate = 0.08) {
    return amount * taxRate;
  }

  static calculateDiscount(amount, discountPercentage) {
    return amount * (discountPercentage / 100);
  }

  static calculateEstimatedDeliveryTime(distance, averageSpeed = 50) {
    // Returns estimated time in minutes
    return Math.round((distance / averageSpeed) * 60);
  }

  static calculateInventoryTurnover(costOfGoodsSold, averageInventory) {
    if (averageInventory === 0) return 0;
    return costOfGoodsSold / averageInventory;
  }

  static calculateReorderPoint(dailyUsage, leadTimeDays, safetyStock = 0) {
    return (dailyUsage * leadTimeDays) + safetyStock;
  }
}

/**
 * Utility functions for data generation
 */
class DataGenerator {
  static generateRandomId(prefix = '', length = 6) {
    const chars = '0123456789';
    let result = prefix;
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  static generateRandomName() {
    const firstNames = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Anna'];
    const lastNames = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Miller', 'Taylor', 'Anderson'];
    
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    
    return `${firstName} ${lastName}`;
  }

  static generateRandomEmail(name = null) {
    const domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com'];
    const domain = domains[Math.floor(Math.random() * domains.length)];
    
    if (name) {
      const cleanName = name.toLowerCase().replace(/\s+/g, '.');
      return `${cleanName}@${domain}`;
    }
    
    const username = DataGenerator.generateRandomId('user', 4);
    return `${username}@${domain}`;
  }

  static generateRandomAddress() {
    const streets = ['Main St', 'Oak Ave', 'Pine Rd', 'Elm St', 'Maple Dr', 'Cedar Ln'];
    const cities = ['Springfield', 'Franklin', 'Georgetown', 'Madison', 'Clinton', 'Chester'];
    const states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'];
    
    const streetNumber = Math.floor(Math.random() * 9999) + 1;
    const street = streets[Math.floor(Math.random() * streets.length)];
    const city = cities[Math.floor(Math.random() * cities.length)];
    const state = states[Math.floor(Math.random() * states.length)];
    const zipCode = Math.floor(Math.random() * 90000) + 10000;
    
    return `${streetNumber} ${street}, ${city}, ${state} ${zipCode}`;
  }

  static generateRandomPrice(min = 10, max = 1000) {
    return parseFloat((Math.random() * (max - min) + min).toFixed(2));
  }

  static generateRandomDate(daysBack = 30) {
    const now = new Date();
    const randomDays = Math.floor(Math.random() * daysBack);
    const randomDate = new Date(now.getTime() - (randomDays * 24 * 60 * 60 * 1000));
    return randomDate;
  }
}

module.exports = {
  Validator,
  Formatter,
  Calculator,
  DataGenerator
};

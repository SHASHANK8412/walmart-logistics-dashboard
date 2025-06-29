const { v4: uuidv4 } = require('uuid');
const moment = require('moment');

class Order {
  constructor({
    id = null,
    order_id = null,
    customer_name,
    customer_email,
    product_id,
    product_name,
    quantity,
    price,
    status = 'pending',
    order_date = new Date(),
    delivery_address,
    payment_method = 'Credit Card'
  }) {
    this.id = id || this.generateId();
    this.order_id = order_id || this.generateOrderId();
    this.customer_name = customer_name;
    this.customer_email = customer_email;
    this.product_id = product_id;
    this.product_name = product_name;
    this.quantity = quantity;
    this.price = price;
    this.status = status;
    this.order_date = order_date;
    this.delivery_address = delivery_address;
    this.payment_method = payment_method;
    this.created_at = new Date();
    this.updated_at = new Date();
  }

  generateId() {
    return Math.floor(Math.random() * 10000) + 1;
  }

  generateOrderId() {
    const year = new Date().getFullYear();
    const random = Math.floor(Math.random() * 9999) + 1;
    return `ORD-${year}${random.toString().padStart(3, '0')}`;
  }

  updateStatus(newStatus) {
    const validStatuses = ['pending', 'shipped', 'delivered', 'cancelled'];
    if (validStatuses.includes(newStatus)) {
      this.status = newStatus;
      this.updated_at = new Date();
      return true;
    }
    return false;
  }

  calculateTotal() {
    return (this.quantity * this.price).toFixed(2);
  }

  getFormattedDate() {
    return moment(this.order_date).format('YYYY-MM-DD HH:mm:ss');
  }

  static getValidStatuses() {
    return ['pending', 'shipped', 'delivered', 'cancelled'];
  }

  static getPaymentMethods() {
    return ['Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery'];
  }

  toJSON() {
    return {
      id: this.id,
      order_id: this.order_id,
      customer_name: this.customer_name,
      customer_email: this.customer_email,
      product_id: this.product_id,
      product_name: this.product_name,
      quantity: this.quantity,
      price: this.price,
      status: this.status,
      order_date: this.order_date,
      delivery_address: this.delivery_address,
      payment_method: this.payment_method,
      total: this.calculateTotal(),
      created_at: this.created_at,
      updated_at: this.updated_at
    };
  }
}

module.exports = Order;

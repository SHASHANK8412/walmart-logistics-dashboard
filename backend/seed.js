// Seed script for MongoDB inventory
require('dotenv').config();
const mongoose = require('mongoose');
const MongoProduct = require('./models/MongoProduct');

const MONGO_URI = process.env.MONGODB_URI;

const products = [
  {
    sku: 'SKU-10001',
    name: 'Laptop',
    description: 'High performance laptop',
    category: 'Electronics',
    stock_quantity: 20,
    price: 800,
    cost: 600,
    location: 'A1',
    reorder_level: 5,
    supplier: 'Supplier 1',
    status: 'active'
  },
  {
    sku: 'SKU-10002',
    name: 'Smartphone',
    description: 'Latest model smartphone',
    category: 'Electronics',
    stock_quantity: 30,
    price: 600,
    cost: 400,
    location: 'A2',
    reorder_level: 8,
    supplier: 'Supplier 2',
    status: 'active'
  },
  {
    sku: 'SKU-10003',
    name: 'Tablet',
    description: '10-inch display tablet',
    category: 'Electronics',
    stock_quantity: 15,
    price: 400,
    cost: 250,
    location: 'A3',
    reorder_level: 4,
    supplier: 'Supplier 3',
    status: 'active'
  },
  {
    sku: 'SKU-10004',
    name: 'Headphones',
    description: 'Wireless noise-canceling headphones',
    category: 'Electronics',
    stock_quantity: 25,
    price: 200,
    cost: 120,
    location: 'B1',
    reorder_level: 6,
    supplier: 'Supplier 4',
    status: 'active'
  },
  {
    sku: 'SKU-10005',
    name: 'Monitor',
    description: '24-inch LED monitor',
    category: 'Electronics',
    stock_quantity: 12,
    price: 300,
    cost: 180,
    location: 'B2',
    reorder_level: 3,
    supplier: 'Supplier 5',
    status: 'active'
  }
];

async function seed() {
  await mongoose.connect(MONGO_URI);
  await MongoProduct.deleteMany({});
  await MongoProduct.insertMany(products);
  console.log('Seeded inventory with products!');
  await mongoose.disconnect();
}

seed();

const mongoose = require('mongoose');
require('dotenv').config();

const connectDB = async () => {
  try {
    const mongoURI = process.env.MONGODB_URI || 'mongodb://localhost:27017/walmart_logistics';    const conn = await mongoose.connect(mongoURI, {
      serverSelectionTimeoutMS: 5000, // Keep trying to send operations for 5 seconds
      socketTimeoutMS: 45000, // Close sockets after 45 seconds of inactivity
      maxPoolSize: 10, // Maintain up to 10 socket connections
    });

    console.log(`✅ MongoDB Connected: ${conn.connection.host}`);
    console.log(`📂 Database: ${conn.connection.name}`);
    
    // Handle connection events
    mongoose.connection.on('error', (err) => {
      console.error('❌ MongoDB connection error:', err);
    });

    mongoose.connection.on('disconnected', () => {
      console.log('⚠️  MongoDB disconnected');
    });

    mongoose.connection.on('reconnected', () => {
      console.log('🔄 MongoDB reconnected');
    });

    return conn;
  } catch (error) {
    console.error('❌ MongoDB connection failed:', error.message);
    
    // If MongoDB is not available, show helpful message
    if (error.message.includes('ECONNREFUSED')) {
      console.log('\n📋 To start MongoDB locally:');
      console.log('1. Install MongoDB: https://www.mongodb.com/try/download/community');
      console.log('2. Start MongoDB service:');
      console.log('   - Windows: Start "MongoDB" service from Services');
      console.log('   - macOS: brew services start mongodb/brew/mongodb-community');
      console.log('   - Linux: sudo systemctl start mongod');
      console.log('3. Or use MongoDB Atlas (cloud): https://cloud.mongodb.com/');
      console.log('\n🔄 The server will continue using mock data until MongoDB is available.\n');
    }
    
    // Don't exit the process, continue with mock data
    return null;
  }
};

// Graceful connection close
const closeDB = async () => {
  try {
    await mongoose.connection.close();
    console.log('🔒 MongoDB connection closed');
  } catch (error) {
    console.error('❌ Error closing MongoDB connection:', error.message);
  }
};

// Handle app termination
process.on('SIGINT', async () => {
  await closeDB();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await closeDB();
  process.exit(0);
});

module.exports = { connectDB, closeDB };

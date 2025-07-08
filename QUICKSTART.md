# 🛒 Walmart Logistics Dashboard - Quick Start Guide

## Getting Started

### 📋 Prerequisites
- Python 3.8+ installed on your system
- Git (optional, for version control)
- Basic familiarity with command-line operations

### 🚀 Running the Application

#### Windows
1. Double-click the `run.bat` file
   - This will:
     - Create a virtual environment (if needed)
     - Install required dependencies
     - Start the dashboard

#### macOS/Linux
1. Open Terminal in the project directory
2. Make the script executable:
   ```bash
   chmod +x run.sh
   ```
3. Run the script:
   ```bash
   ./run.sh
   ```

4. Access the dashboard at: http://localhost:8501

### 🔐 Authentication

#### Admin Access
- Username: `admin`
- Password: `admin123`
- Full access to all dashboard features and tabs

#### Customer Registration
1. Click on "Register" tab on the login screen
2. Fill in the registration form:
   - Full Name
   - Email
   - Verification Method (Email or Phone)
   - Phone Number (if Phone verification selected)
   - Username
   - Password
   - Confirm Password
3. Accept Terms of Service
4. Click "Register"
5. You'll receive a 6-digit OTP code via email or SMS
6. Enter the verification code in the verification screen
7. Click "Verify" to complete registration

> **Note:** For testing purposes, the OTP will be displayed in the app if email/SMS credentials are not configured

## 📱 Key Features

### For Administrators
- Complete supply chain visibility
- Advanced problem-solving tools
- Real-time system monitoring
- User management capabilities
- Network status monitoring
- Alert and issue management

### For Customers
- Order tracking
- Personalized dashboard
- Purchase history and analytics
- Inventory visibility
- Delivery tracking
- Personalized recommendations

## 🧩 Supply Chain Problem Solver

Access the supply chain problem solver through:
1. Login as any user
2. Navigate to "Supply Chain" tab
3. Select "Problem Solver" tab
4. Choose a specific problem category to solve:
   - Transportation & Logistics
   - Inventory Optimization
   - Production Bottlenecks
   - Network Distribution
   - Reverse Logistics
   - Warehouse Optimization
   - Demand Forecasting (fully implemented)
   - Cost Reduction

## 📊 Demand Forecasting Quick Guide

The Demand Forecasting solver provides:
1. Historical data visualization
2. Multiple forecasting model options
3. Customizable forecast parameters
4. Performance comparison across models
5. Implementation recommendations
6. Downloadable forecast data

### Using the Demand Forecaster
1. Set your forecast horizon (4-52 weeks)
2. Select product categories
3. Adjust seasonality strength
4. Choose forecast models
5. Set confidence interval
6. Add external features
7. Click "Generate Forecast"
8. View results in the three tabs:
   - Forecast Results (visualization)
   - Model Comparison (performance metrics)
   - Implementation Plan (deployment steps)

## � Email and SMS Configuration

The application uses email and SMS for sending verification codes. For production use, configure the `.env` file:

1. Copy `.env.example` to `.env`
2. For email verification:
   - Set `SMTP_SERVER` and `SMTP_PORT` for your email provider
   - Set `EMAIL_USERNAME` and `EMAIL_PASSWORD` with your credentials
   - For Gmail, you'll need to use an App Password (2FA required)

3. For SMS verification:
   - Create a Twilio account (https://www.twilio.com)
   - Get your Account SID and Auth Token from the Twilio Console
   - Get a Twilio phone number
   - Set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER`

> **Note:** Without these configurations, the application will run in development mode and display the OTP codes in the app instead of sending them.

## �🔧 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed and in PATH
- Check for error messages in the terminal
- Verify all requirements are installed: `pip install -r requirements.txt`

### Login issues
- Default admin credentials: username=`admin`, password=`admin123`
- If you forgot your password, use the admin account to reset it

### Data visualization problems
- Ensure all dependencies are correctly installed
- Try refreshing the browser
- Check console for JavaScript errors

## 📞 Support

For additional help or feature requests, please contact:
- Email: support@walmart-logistics.com
- Internal Helpdesk: x1234

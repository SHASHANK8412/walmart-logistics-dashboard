#!/bin/bash

# Walmart Logistics Dashboard Setup Script
# This script sets up the complete enterprise warehouse management system

echo "🛒 Walmart Logistics Dashboard - Enterprise Setup"
echo "================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION is installed"
        
        # Check if Python version is 3.8 or higher
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_status "Python version is compatible"
        else
            print_error "Python 3.8 or higher is required"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        echo "Please install Python 3.8 or higher from https://python.org"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_step "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        print_status "pip is installed"
    else
        print_error "pip is not installed"
        echo "Please install pip using: sudo apt-get install python3-pip"
        exit 1
    fi
}

# Create virtual environment
setup_virtual_env() {
    print_step "Setting up virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
    else
        python3 -m venv venv
        print_status "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_status "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_step "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Setup environment variables
setup_environment() {
    print_step "Setting up environment variables..."
    
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Walmart Logistics Dashboard Configuration
DEBUG_MODE=true
BACKEND_URL=http://localhost:3000
AUTO_REFRESH_INTERVAL=30
MAX_CONCURRENT_USERS=100
SESSION_TIMEOUT=3600

# Feature Flags
ENABLE_ML_FEATURES=true
ENABLE_IOT_MONITORING=true
ENABLE_SECURITY_MODULE=true
ENABLE_SUSTAINABILITY=true
ENABLE_ADVANCED_ANALYTICS=true

# Database Configuration
DATABASE_URL=mongodb://localhost:27017/walmart
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200

# API Keys (Configure these with your actual keys)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TWILIO_API_KEY=your_twilio_api_key
EOF
        print_status "Environment configuration created"
        print_warning "Please update .env file with your actual API keys"
    else
        print_status "Environment configuration already exists"
    fi
}

# Create necessary directories
setup_directories() {
    print_step "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p data
    mkdir -p exports
    mkdir -p uploads
    mkdir -p temp
    
    print_status "Directories created"
}

# Setup mock data
setup_mock_data() {
    print_step "Setting up mock data..."
    
    if [ -d "mock_data" ]; then
        print_status "Mock data directory already exists"
    else
        mkdir -p mock_data
        
        # Create sample orders data
        cat > mock_data/orders.json << EOF
[
    {
        "order_id": "WM-2024-001",
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "order_date": "2024-01-15",
        "status": "shipped",
        "total_amount": 299.99,
        "items": [
            {"sku": "SKU-001", "name": "Wireless Headphones", "quantity": 2, "price": 149.99}
        ]
    },
    {
        "order_id": "WM-2024-002",
        "customer_name": "Jane Smith",
        "customer_email": "jane.smith@example.com",
        "order_date": "2024-01-16",
        "status": "processing",
        "total_amount": 1299.99,
        "items": [
            {"sku": "SKU-002", "name": "Gaming Laptop", "quantity": 1, "price": 1299.99}
        ]
    }
]
EOF
        
        print_status "Mock data created"
    fi
}

# Check system requirements
check_system_requirements() {
    print_step "Checking system requirements..."
    
    # Check available memory
    if command -v free &> /dev/null; then
        MEM_MB=$(free -m | grep "Mem:" | awk '{print $2}')
        if [ $MEM_MB -lt 2048 ]; then
            print_warning "Less than 2GB RAM available. Application may run slowly."
        else
            print_status "Memory requirements met"
        fi
    fi
    
    # Check available disk space
    if command -v df &> /dev/null; then
        DISK_MB=$(df -m . | tail -1 | awk '{print $4}')
        if [ $DISK_MB -lt 1024 ]; then
            print_warning "Less than 1GB disk space available"
        else
            print_status "Disk space requirements met"
        fi
    fi
}

# Create launcher script
create_launcher() {
    print_step "Creating launcher script..."
    
    cat > start_dashboard.sh << 'EOF'
#!/bin/bash

# Walmart Logistics Dashboard Launcher
echo "🛒 Starting Walmart Logistics Dashboard..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start the application
streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false

echo "Dashboard stopped"
EOF
    
    chmod +x start_dashboard.sh
    print_status "Launcher script created"
}

# Create Windows batch file
create_windows_launcher() {
    print_step "Creating Windows launcher..."
    
    cat > start_dashboard.bat << 'EOF'
@echo off
echo 🛒 Starting Walmart Logistics Dashboard...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Start the application
streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false

echo Dashboard stopped
pause
EOF
    
    print_status "Windows launcher created"
}

# Run system health check
run_health_check() {
    print_step "Running system health check..."
    
    # Check if all required files exist
    REQUIRED_FILES=("app.py" "requirements.txt" "tabs/__init__.py" "utils/api.py" "utils/helpers.py")
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            print_status "✓ $file exists"
        else
            print_error "✗ $file missing"
            exit 1
        fi
    done
    
    # Check if Python can import main modules
    python3 -c "import streamlit, pandas, numpy, plotly, matplotlib, folium, sklearn, PIL, qrcode" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "✓ All Python modules can be imported"
    else
        print_error "✗ Some Python modules are missing"
        exit 1
    fi
}

# Main setup function
main() {
    echo "Starting Walmart Logistics Dashboard setup..."
    echo ""
    
    # Run all setup steps
    check_python
    check_pip
    setup_virtual_env
    install_dependencies
    setup_environment
    setup_directories
    setup_mock_data
    check_system_requirements
    create_launcher
    create_windows_launcher
    run_health_check
    
    echo ""
    echo "================================================="
    echo -e "${GREEN}✅ Setup completed successfully!${NC}"
    echo "================================================="
    echo ""
    echo "🚀 To start the dashboard:"
    echo "   Linux/Mac: ./start_dashboard.sh"
    echo "   Windows:   start_dashboard.bat"
    echo "   Manual:    streamlit run app.py"
    echo ""
    echo "📖 The dashboard will be available at:"
    echo "   http://localhost:8501"
    echo ""
    echo "📚 Advanced features include:"
    echo "   • 🏪 Integrated Dashboard"
    echo "   • 📦 Order Management"
    echo "   • 📚 Inventory Management"
    echo "   • 🚚 Delivery & Logistics"
    echo "   • 🏢 Warehouse Operations"
    echo "   • 🧠 AI Optimization"
    echo "   • 📊 Advanced Analytics"
    echo "   • 👥 Staff Management"
    echo "   • 🔗 Supply Chain"
    echo "   • 🔍 Quality Control"
    echo "   • 🌐 IoT Monitoring"
    echo "   • 🤖 ML & Predictive"
    echo "   • 🔐 Security & Access"
    echo "   • 🌱 Sustainability"
    echo ""
    echo "⚠️  Remember to:"
    echo "   • Update .env file with your API keys"
    echo "   • Configure database connections"
    echo "   • Review security settings"
    echo ""
    echo "📞 For support, see README_ADVANCED.md"
    echo ""
}

# Run main function
main

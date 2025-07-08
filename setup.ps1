# Walmart Logistics Dashboard Setup Script for Windows
# PowerShell script to set up the complete enterprise warehouse management system

Write-Host "🛒 Walmart Logistics Dashboard - Enterprise Setup" -ForegroundColor Blue
Write-Host "=================================================" -ForegroundColor Blue
Write-Host ""

# Function to print colored output
function Write-Status {
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Step {
    param($Message)
    Write-Host "[STEP] $Message" -ForegroundColor Cyan
}

# Check if Python is installed
function Check-Python {
    Write-Step "Checking Python installation..."
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -like "*Python 3.*") {
            Write-Status "Python is installed: $pythonVersion"
            
            # Check if Python version is 3.8 or higher
            $version = ($pythonVersion -split ' ')[1]
            $majorMinor = $version.Split('.')[0..1] -join '.'
            if ([version]$majorMinor -ge [version]"3.8") {
                Write-Status "Python version is compatible"
            } else {
                Write-Error "Python 3.8 or higher is required"
                exit 1
            }
        } else {
            Write-Error "Python 3 is not installed"
            Write-Host "Please install Python 3.8 or higher from https://python.org"
            exit 1
        }
    } catch {
        Write-Error "Python is not installed or not in PATH"
        Write-Host "Please install Python 3.8 or higher from https://python.org"
        exit 1
    }
}

# Check if pip is installed
function Check-Pip {
    Write-Step "Checking pip installation..."
    
    try {
        $pipVersion = pip --version 2>&1
        Write-Status "pip is installed: $pipVersion"
    } catch {
        Write-Error "pip is not installed"
        Write-Host "Please install pip or reinstall Python with pip included"
        exit 1
    }
}

# Create virtual environment
function Setup-VirtualEnv {
    Write-Step "Setting up virtual environment..."
    
    if (Test-Path "venv") {
        Write-Warning "Virtual environment already exists"
    } else {
        python -m venv venv
        Write-Status "Virtual environment created"
    }
    
    # Activate virtual environment
    & "venv\Scripts\Activate.ps1"
    Write-Status "Virtual environment activated"
}

# Install dependencies
function Install-Dependencies {
    Write-Step "Installing Python dependencies..."
    
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
        Write-Status "Dependencies installed successfully"
    } else {
        Write-Error "requirements.txt not found"
        exit 1
    }
}

# Setup environment variables
function Setup-Environment {
    Write-Step "Setting up environment variables..."
    
    if (!(Test-Path ".env")) {
        @"
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
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Status "Environment configuration created"
        Write-Warning "Please update .env file with your actual API keys"
    } else {
        Write-Status "Environment configuration already exists"
    }
}

# Create necessary directories
function Setup-Directories {
    Write-Step "Creating necessary directories..."
    
    $directories = @("logs", "data", "exports", "uploads", "temp")
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    Write-Status "Directories created"
}

# Setup mock data
function Setup-MockData {
    Write-Step "Setting up mock data..."
    
    if (Test-Path "mock_data") {
        Write-Status "Mock data directory already exists"
    } else {
        New-Item -ItemType Directory -Path "mock_data" -Force | Out-Null
        
        # Create sample orders data
        @"
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
"@ | Out-File -FilePath "mock_data\orders.json" -Encoding UTF8
        
        Write-Status "Mock data created"
    }
}

# Check system requirements
function Check-SystemRequirements {
    Write-Step "Checking system requirements..."
    
    # Check available memory
    $totalMemory = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory / 1GB
    if ($totalMemory -lt 2) {
        Write-Warning "Less than 2GB RAM available. Application may run slowly."
    } else {
        Write-Status "Memory requirements met ($([math]::Round($totalMemory, 1))GB available)"
    }
    
    # Check available disk space
    $freeSpace = (Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB
    if ($freeSpace -lt 1) {
        Write-Warning "Less than 1GB disk space available"
    } else {
        Write-Status "Disk space requirements met ($([math]::Round($freeSpace, 1))GB available)"
    }
}

# Create launcher script
function Create-Launcher {
    Write-Step "Creating launcher script..."
    
    @"
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
"@ | Out-File -FilePath "start_dashboard.bat" -Encoding UTF8
    
    Write-Status "Launcher script created"
}

# Create PowerShell launcher
function Create-PowerShellLauncher {
    Write-Step "Creating PowerShell launcher..."
    
    @"
# Walmart Logistics Dashboard Launcher (PowerShell)
Write-Host "🛒 Starting Walmart Logistics Dashboard..." -ForegroundColor Blue

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Set environment variables
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"

# Start the application
streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false

Write-Host "Dashboard stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"
"@ | Out-File -FilePath "start_dashboard.ps1" -Encoding UTF8
    
    Write-Status "PowerShell launcher created"
}

# Run system health check
function Run-HealthCheck {
    Write-Step "Running system health check..."
    
    # Check if all required files exist
    $requiredFiles = @("app.py", "requirements.txt", "tabs\__init__.py", "utils\api.py", "utils\helpers.py")
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Status "✓ $file exists"
        } else {
            Write-Error "✗ $file missing"
            exit 1
        }
    }
    
    # Check if Python can import main modules
    try {
        python -c "import streamlit, pandas, numpy, plotly, matplotlib, folium, sklearn, PIL, qrcode" 2>$null
        Write-Status "✓ All Python modules can be imported"
    } catch {
        Write-Error "✗ Some Python modules are missing"
        exit 1
    }
}

# Main setup function
function Main {
    Write-Host "Starting Walmart Logistics Dashboard setup..." -ForegroundColor Blue
    Write-Host ""
    
    # Run all setup steps
    Check-Python
    Check-Pip
    Setup-VirtualEnv
    Install-Dependencies
    Setup-Environment
    Setup-Directories
    Setup-MockData
    Check-SystemRequirements
    Create-Launcher
    Create-PowerShellLauncher
    Run-HealthCheck
    
    Write-Host ""
    Write-Host "=================================================" -ForegroundColor Blue
    Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
    Write-Host "=================================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "🚀 To start the dashboard:" -ForegroundColor Yellow
    Write-Host "   Batch file:    start_dashboard.bat" -ForegroundColor White
    Write-Host "   PowerShell:    .\start_dashboard.ps1" -ForegroundColor White
    Write-Host "   Manual:        streamlit run app.py" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 The dashboard will be available at:" -ForegroundColor Yellow
    Write-Host "   http://localhost:8501" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Advanced features include:" -ForegroundColor Yellow
    Write-Host "   • 🏪 Integrated Dashboard" -ForegroundColor White
    Write-Host "   • 📦 Order Management" -ForegroundColor White
    Write-Host "   • 📚 Inventory Management" -ForegroundColor White
    Write-Host "   • 🚚 Delivery & Logistics" -ForegroundColor White
    Write-Host "   • 🏢 Warehouse Operations" -ForegroundColor White
    Write-Host "   • 🧠 AI Optimization" -ForegroundColor White
    Write-Host "   • 📊 Advanced Analytics" -ForegroundColor White
    Write-Host "   • 👥 Staff Management" -ForegroundColor White
    Write-Host "   • 🔗 Supply Chain" -ForegroundColor White
    Write-Host "   • 🔍 Quality Control" -ForegroundColor White
    Write-Host "   • 🌐 IoT Monitoring" -ForegroundColor White
    Write-Host "   • 🤖 ML & Predictive" -ForegroundColor White
    Write-Host "   • 🔐 Security & Access" -ForegroundColor White
    Write-Host "   • 🌱 Sustainability" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️  Remember to:" -ForegroundColor Yellow
    Write-Host "   • Update .env file with your API keys" -ForegroundColor White
    Write-Host "   • Configure database connections" -ForegroundColor White
    Write-Host "   • Review security settings" -ForegroundColor White
    Write-Host ""
    Write-Host "📞 For support, see README_ADVANCED.md" -ForegroundColor Yellow
    Write-Host ""
}

# Run main function
Main

@echo off
echo Installing Walmart Logistics Backend dependencies...
cd backend
npm install

echo.
echo Starting the backend server...
npm run dev

echo.
echo Backend is now running on http://localhost:3000
echo.
echo Available endpoints:
echo - Health check: http://localhost:3000/health
echo - API documentation: http://localhost:3000/
echo - Orders: http://localhost:3000/api/orders
echo - Inventory: http://localhost:3000/api/inventory
echo - Delivery: http://localhost:3000/api/delivery
echo - Warehouse: http://localhost:3000/api/warehouse
echo - Optimizer: http://localhost:3000/api/optimizer
echo - Dashboard: http://localhost:3000/api/dashboard
echo.
pause

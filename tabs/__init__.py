# This file makes the tabs directory a Python package
from tabs import orders, inventory, delivery, warehouse, optimizer, integrated_dashboard

TABS = {
    "🏪 Dashboard": integrated_dashboard,
    "📦 Orders": orders,
    "📚 Inventory": inventory,
    "🚚 Delivery": delivery,
    "🏢 Warehouse": warehouse,
    "🧠 Optimizer": optimizer
}

"""
Product Catalog and Category Management for Walmart Logistics Dashboard
Provides comprehensive product categorization with images and detailed information.
"""

import random
import re

# Define product categories with styling and descriptions
CATEGORIES = {
    "Electronics": {
        "icon": "💻",
        "color": "#3498db",
        "description": "Computers, phones, tablets, and electronic accessories"
    },
    "Grocery": {
        "icon": "🛒",
        "color": "#27ae60",
        "description": "Fresh food, pantry items, beverages, and household essentials"
    },
    "Home & Garden": {
        "icon": "🏠",
        "color": "#e67e22",
        "description": "Furniture, decor, gardening tools, and home improvement"
    },
    "Clothing": {
        "icon": "👕",
        "color": "#9b59b6",
        "description": "Men's, women's, and children's clothing and accessories"
    },
    "Sports & Outdoors": {
        "icon": "⚽",
        "color": "#e74c3c",
        "description": "Sports equipment, outdoor gear, and fitness accessories"
    },
    "Toys & Games": {
        "icon": "🎮",
        "color": "#f39c12",
        "description": "Children's toys, board games, and entertainment"
    },
    "Health & Beauty": {
        "icon": "💄",
        "color": "#1abc9c",
        "description": "Personal care, cosmetics, supplements, and wellness products"
    }
}

# Comprehensive product catalog organized by categories
PRODUCTS = {
    "Electronics": {
        "MacBook Pro 16-inch": {
            "brand": "Apple",
            "description": "Powerful laptop with M2 Pro chip, perfect for professionals",
            "price_range": "$2,499 - $3,999",
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop",
            "stock_level": 25,
            "category": "Electronics"
        },
        "iPhone 15 Pro": {
            "brand": "Apple", 
            "description": "Latest iPhone with titanium design and advanced camera system",
            "price_range": "$999 - $1,499",
            "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop",
            "stock_level": 50,
            "category": "Electronics"
        },
        "Samsung Galaxy S24 Ultra": {
            "brand": "Samsung",
            "description": "Premium Android phone with S Pen and AI features",
            "price_range": "$1,199 - $1,599",
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop",
            "stock_level": 35,
            "category": "Electronics"
        },
        "iPad Pro 12.9-inch": {
            "brand": "Apple",
            "description": "Professional tablet with M2 chip and Liquid Retina display",
            "price_range": "$1,099 - $2,199",
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop",
            "stock_level": 30,
            "category": "Electronics"
        },
        "Dell XPS 13": {
            "brand": "Dell",
            "description": "Ultra-portable laptop with InfinityEdge display",
            "price_range": "$899 - $1,799",
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
            "stock_level": 20,
            "category": "Electronics"
        },
        "Sony WH-1000XM5": {
            "brand": "Sony",
            "description": "Premium noise-canceling wireless headphones",
            "price_range": "$349 - $399",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",
            "stock_level": 45,
            "category": "Electronics"
        }
    },
    
    "Grocery": {
        "Organic Bananas": {
            "brand": "Great Value",
            "description": "Fresh organic bananas, perfect for snacks and smoothies",
            "price_range": "$1.98 - $2.48/lb",
            "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=300&fit=crop",
            "stock_level": 100,
            "category": "Grocery"
        },
        "Whole Milk Gallon": {
            "brand": "Great Value",
            "description": "Fresh whole milk, vitamin D fortified",
            "price_range": "$3.48 - $4.98/gallon",
            "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
            "stock_level": 80,
            "category": "Grocery"
        },
        "Free Range Eggs": {
            "brand": "Eggland's Best",
            "description": "Farm fresh free-range eggs, dozen pack",
            "price_range": "$3.98 - $5.48/dozen",
            "image_url": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&h=300&fit=crop",
            "stock_level": 60,
            "category": "Grocery"
        },
        "Whole Wheat Bread": {
            "brand": "Wonder Bread",
            "description": "Nutritious whole wheat bread loaf",
            "price_range": "$2.48 - $3.48/loaf",
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop",
            "stock_level": 75,
            "category": "Grocery"
        },
        "Greek Yogurt": {
            "brand": "Chobani",
            "description": "Creamy Greek yogurt with live probiotics",
            "price_range": "$1.28 - $1.98/container",
            "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop",
            "stock_level": 90,
            "category": "Grocery"
        },
        "Premium Ground Coffee": {
            "brand": "Folgers",
            "description": "Rich medium roast ground coffee",
            "price_range": "$8.98 - $12.98/bag",
            "image_url": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=300&fit=crop",
            "stock_level": 55,
            "category": "Grocery"
        }
    },
    
    "Home & Garden": {
        "Modern Sofa Set": {
            "brand": "Better Homes & Gardens",
            "description": "3-piece modern sectional sofa in neutral fabric",
            "price_range": "$899 - $1,499",
            "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop",
            "stock_level": 15,
            "category": "Home & Garden"
        },
        "Dining Table Set": {
            "brand": "Mainstays",
            "description": "6-person dining table with matching chairs",
            "price_range": "$299 - $599",
            "image_url": "https://images.unsplash.com/photo-1449247709967-d4461a6a6103?w=400&h=300&fit=crop",
            "stock_level": 12,
            "category": "Home & Garden"
        },
        "Garden Tool Set": {
            "brand": "Fiskars",
            "description": "Complete gardening tools with ergonomic handles",
            "price_range": "$49.99 - $89.99",
            "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop",
            "stock_level": 40,
            "category": "Home & Garden"
        },
        "LED Floor Lamp": {
            "brand": "Mainstays",
            "description": "Modern LED floor lamp with adjustable brightness",
            "price_range": "$39.99 - $79.99",
            "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop",
            "stock_level": 35,
            "category": "Home & Garden"
        },
        "Outdoor Patio Set": {
            "brand": "Better Homes & Gardens",
            "description": "4-piece outdoor furniture set with cushions",
            "price_range": "$299 - $599",
            "image_url": "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=400&h=300&fit=crop",
            "stock_level": 18,
            "category": "Home & Garden"
        },
        "Indoor Plant Collection": {
            "brand": "Costa Farms",
            "description": "Set of 3 air-purifying indoor plants",
            "price_range": "$29.99 - $49.99",
            "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=300&fit=crop",
            "stock_level": 50,
            "category": "Home & Garden"
        }
    },
    
    "Clothing": {
        "Men's Casual Shirt": {
            "brand": "George",
            "description": "Comfortable cotton casual shirt, various colors",
            "price_range": "$12.97 - $19.97",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop",
            "stock_level": 75,
            "category": "Clothing"
        },
        "Women's Dress": {
            "brand": "Time and Tru",
            "description": "Elegant midi dress perfect for work or casual wear",
            "price_range": "$19.97 - $39.97",
            "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=300&fit=crop",
            "stock_level": 60,
            "category": "Clothing"
        },
        "Kids' Sneakers": {
            "brand": "Athletic Works",
            "description": "Comfortable running shoes for active kids",
            "price_range": "$15.97 - $29.97",
            "image_url": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=300&fit=crop",
            "stock_level": 85,
            "category": "Clothing"
        },
        "Denim Jeans": {
            "brand": "Faded Glory",
            "description": "Classic straight-fit denim jeans",
            "price_range": "$15.97 - $24.97",
            "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop",
            "stock_level": 95,
            "category": "Clothing"
        },
        "Winter Jacket": {
            "brand": "Climate Right",
            "description": "Warm insulated jacket for cold weather",
            "price_range": "$39.97 - $79.97",
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=300&fit=crop",
            "stock_level": 45,
            "category": "Clothing"
        },
        "Summer Sandals": {
            "brand": "Time and Tru",
            "description": "Comfortable summer sandals with arch support",
            "price_range": "$12.97 - $22.97",
            "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=300&fit=crop",
            "stock_level": 70,
            "category": "Clothing"
        }
    },
    
    "Sports & Outdoors": {
        "Basketball": {
            "brand": "Spalding",
            "description": "Official size basketball for indoor/outdoor play",
            "price_range": "$19.97 - $39.97",
            "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=300&fit=crop",
            "stock_level": 40,
            "category": "Sports & Outdoors"
        },
        "Yoga Mat": {
            "brand": "EverlastFlex",
            "description": "Non-slip yoga mat with carrying strap",
            "price_range": "$15.97 - $29.97",
            "image_url": "https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=400&h=300&fit=crop",
            "stock_level": 55,
            "category": "Sports & Outdoors"
        },
        "Camping Tent": {
            "brand": "Ozark Trail",
            "description": "4-person dome tent for camping adventures",
            "price_range": "$49.97 - $99.97",
            "image_url": "https://images.unsplash.com/photo-1487730116645-74489c95b41b?w=400&h=300&fit=crop",
            "stock_level": 25,
            "category": "Sports & Outdoors"
        },
        "Fishing Rod Set": {
            "brand": "Zebco",
            "description": "Complete fishing rod and reel combo",
            "price_range": "$29.97 - $59.97",
            "image_url": "https://images.unsplash.com/photo-1445991842772-097fea258e7b?w=400&h=300&fit=crop",
            "stock_level": 30,
            "category": "Sports & Outdoors"
        },
        "Bike Helmet": {
            "brand": "Bell",
            "description": "Safety certified bike helmet with adjustable fit",
            "price_range": "$19.97 - $39.97",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop",
            "stock_level": 65,
            "category": "Sports & Outdoors"
        },
        "Dumbbells Set": {
            "brand": "Weider",
            "description": "Adjustable dumbbell set for home workouts",
            "price_range": "$99.97 - $199.97",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop",
            "stock_level": 20,
            "category": "Sports & Outdoors"
        }
    },
    
    "Toys & Games": {
        "LEGO Creator Set": {
            "brand": "LEGO",
            "description": "Creative building set with 500+ pieces",
            "price_range": "$39.97 - $79.97",
            "image_url": "https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400&h=300&fit=crop",
            "stock_level": 35,
            "category": "Toys & Games"
        },
        "Board Game Collection": {
            "brand": "Hasbro",
            "description": "Classic family board games variety pack",
            "price_range": "$24.97 - $49.97",
            "image_url": "https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=400&h=300&fit=crop",
            "stock_level": 45,
            "category": "Toys & Games"
        },
        "Remote Control Car": {
            "brand": "Adventure Force",
            "description": "Fast RC car with rechargeable battery",
            "price_range": "$29.97 - $59.97",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop",
            "stock_level": 30,
            "category": "Toys & Games"
        },
        "Art Supply Kit": {
            "brand": "Crayola",
            "description": "Complete art set with crayons, markers, and paper",
            "price_range": "$19.97 - $39.97",
            "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=300&fit=crop",
            "stock_level": 60,
            "category": "Toys & Games"
        },
        "Puzzle Set": {
            "brand": "Buffalo Games",
            "description": "1000-piece jigsaw puzzles, various themes",
            "price_range": "$12.97 - $24.97",
            "image_url": "https://images.unsplash.com/photo-1594736797933-d0d3dc5f66a0?w=400&h=300&fit=crop",
            "stock_level": 50,
            "category": "Toys & Games"
        },
        "Action Figures": {
            "brand": "Marvel",
            "description": "Superhero action figures with accessories",
            "price_range": "$14.97 - $29.97",
            "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop",
            "stock_level": 70,
            "category": "Toys & Games"
        }
    },
    
    "Health & Beauty": {
        "Skincare Set": {
            "brand": "Olay",
            "description": "Complete facial skincare routine kit",
            "price_range": "$24.97 - $49.97",
            "image_url": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=300&fit=crop",
            "stock_level": 55,
            "category": "Health & Beauty"
        },
        "Vitamin Supplements": {
            "brand": "Nature Made",
            "description": "Daily multivitamin tablets, 90-day supply",
            "price_range": "$12.97 - $24.97",
            "image_url": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=300&fit=crop",
            "stock_level": 80,
            "category": "Health & Beauty"
        },
        "Hair Care Set": {
            "brand": "TRESemmé",
            "description": "Shampoo and conditioner for all hair types",
            "price_range": "$8.97 - $16.97",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop",
            "stock_level": 75,
            "category": "Health & Beauty"
        },
        "Makeup Kit": {
            "brand": "Maybelline",
            "description": "Complete makeup starter kit with essentials",
            "price_range": "$19.97 - $39.97",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=300&fit=crop",
            "stock_level": 65,
            "category": "Health & Beauty"
        },
        "Electric Toothbrush": {
            "brand": "Oral-B",
            "description": "Rechargeable electric toothbrush with timer",
            "price_range": "$29.97 - $59.97",
            "image_url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=300&fit=crop",
            "stock_level": 40,
            "category": "Health & Beauty"
        },
        "Body Lotion Set": {
            "brand": "Vaseline",
            "description": "Moisturizing body lotion variety pack",
            "price_range": "$12.97 - $24.97",
            "image_url": "https://images.unsplash.com/photo-1556228841-d0613db5e3b4?w=400&h=300&fit=crop",
            "stock_level": 85,
            "category": "Health & Beauty"
        }
    }
}

def get_all_categories():
    """Return all product categories with their metadata"""
    return CATEGORIES

def get_all_products():
    """Return all products from all categories as a flat dictionary"""
    all_products = {}
    for category, products in PRODUCTS.items():
        all_products.update(products)
    return all_products

def get_products_by_category(category):
    """Return all products in a specific category"""
    return PRODUCTS.get(category, {})

def get_product_info(product_name):
    """Get detailed information for a specific product"""
    all_products = get_all_products()
    product_info = all_products.get(product_name)
    
    if product_info:
        return product_info
    else:
        # Return default product info if not found
        return {
            "brand": "Generic",
            "description": "Product information not available",
            "price_range": "$0.00 - $0.00",
            "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop",
            "stock_level": 0,
            "category": "General"
        }

def display_product_card(product_name, quantity=1, price=0.0, show_details=False):
    """Generate HTML for a product card display"""
    from .styles import get_product_card_style, get_image_style, get_metric_style, COMMON_STYLES
    
    product_info = get_product_info(product_name)
    category_info = CATEGORIES.get(product_info['category'], {'color': '#95a5a6', 'icon': '📦'})
    total_price = quantity * price if price > 0 else 0
    
    # Build card content without inline styling
    card_content = f"""
    <div class="product-card" style="{get_product_card_style(category_info['color'])}">
        <div style="display: flex; gap: 15px; align-items: center;">
            <img src="{product_info['image_url']}" alt="{product_name}" style="{get_image_style()}; border: 2px solid {category_info['color']};">
            <div style="flex: 1;">
                <h4 style="margin: 0 0 5px 0; color: {COMMON_STYLES['text_color']}; font-size: 16px;">{product_name}</h4>
                <p style="margin: 2px 0; color: {category_info['color']}; font-size: 12px; font-weight: bold;">
                    {category_info['icon']} {product_info['category']}
                </p>
                <p style="margin: 2px 0; color: {COMMON_STYLES['secondary_color']}; font-size: 11px;">Brand: {product_info['brand']}</p>
                {f"<p style='margin: 2px 0; color: #34495e; font-size: 11px;'>{product_info['description']}</p>" if show_details else ""}
                <div style="display: flex; gap: 10px; margin-top: 8px;">
                    {f"<span style='{get_metric_style('#3498db')}; font-size: 10px;'>Qty: {quantity}</span>" if quantity > 0 else ""}
                    {f"<span style='{get_metric_style(COMMON_STYLES['success_color'])}; font-size: 10px;'>${price:.2f}/unit</span>" if price > 0 else ""}
                    {f"<span style='{get_metric_style(COMMON_STYLES['danger_color'])}; font-size: 10px; font-weight: bold;'>Total: ${total_price:.2f}</span>" if total_price > 0 else ""}
                </div>
            </div>
        </div>
    </div>
    """
    return card_content

def display_product_grid(products_dict, max_items=6):
    """Generate HTML for a grid of product cards"""
    from .styles import get_grid_container_style, get_product_card_style, COMMON_STYLES
    
    if not products_dict:
        return "<p>No products available.</p>"
    
    grid_html = f'<div style="{get_grid_container_style()}">'
    
    for i, (product_name, product_info) in enumerate(list(products_dict.items())[:max_items]):
        category_info = CATEGORIES.get(product_info['category'], {'color': '#95a5a6', 'icon': '📦'})
        
        grid_html += f"""
        <div style="{get_product_card_style(category_info['color'])}; text-align: center;">
            <img src="{product_info['image_url']}" alt="{product_name}" 
                 style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;">
            <h5 style="margin: 10px 0 5px 0; color: {COMMON_STYLES['text_color']}; font-size: 14px;">{product_name}</h5>
            <p style="margin: 5px 0; color: {category_info['color']}; font-size: 12px; font-weight: bold;">
                {category_info['icon']} {product_info['category']}
            </p>
            <p style="margin: 5px 0; color: {COMMON_STYLES['secondary_color']}; font-size: 11px;">{product_info['brand']}</p>
            <p style="margin: 5px 0; color: #34495e; font-size: 10px; line-height: 1.3;">{product_info['description'][:50]}...</p>
            <p style="margin: 10px 0; color: {COMMON_STYLES['success_color']}; font-weight: bold; font-size: 12px;">{product_info['price_range']}</p>
            <div style="background: {COMMON_STYLES['light_bg']}; padding: 5px; border-radius: 5px; margin-top: 10px;">
                <span style="font-size: 10px; color: {COMMON_STYLES['secondary_color']};">
                    Stock: {product_info['stock_level']} units
                </span>
            </div>
        </div>
        """
    
    grid_html += "</div>"
    
    if len(products_dict) > max_items:
        grid_html += f"<p style='text-align: center; color: {COMMON_STYLES['secondary_color']}; font-style: italic;'>Showing {max_items} of {len(products_dict)} products</p>"
    
    return grid_html

def display_category_selector(selected_category=None):
    """Generate HTML for category selection interface"""
    from .styles import get_category_selector_style, get_grid_container_style
    
    selector_html = f'<div style="{get_grid_container_style()}">'
    
    for category, info in CATEGORIES.items():
        is_selected = category == selected_category
        
        selector_html += f"""
        <div style="{get_category_selector_style(info['color'], is_selected)}">
            <div style="font-size: 32px; margin-bottom: 10px;">{info['icon']}</div>
            <h4 style="margin: 0 0 8px 0; font-size: 16px;">{category}</h4>
            <p style="margin: 0; font-size: 11px; opacity: 0.8;">{info['description']}</p>
            {"<div style='margin-top: 10px; font-weight: bold; font-size: 12px;'>✓ SELECTED</div>" if is_selected else ""}
        </div>
        """
    
    selector_html += "</div>"
    return selector_html

def get_random_products(count=3):
    """Get random products for demo purposes"""
    all_products = get_all_products()
    product_names = list(all_products.keys())
    random_names = random.sample(product_names, min(count, len(product_names)))
    return {name: all_products[name] for name in random_names}

def search_products(query, category=None):
    """Search products by name or description"""
    query = query.lower()
    results = {}
    
    search_space = PRODUCTS.get(category, {}) if category else get_all_products()
    
    for product_name, product_info in search_space.items():
        if (query in product_name.lower() or 
            query in product_info['description'].lower() or 
            query in product_info['brand'].lower()):
            results[product_name] = product_info
    
    return results

def get_low_stock_products(threshold=30):
    """Get products with stock below threshold"""
    low_stock = {}
    all_products = get_all_products()
    
    for product_name, product_info in all_products.items():
        if product_info['stock_level'] < threshold:
            low_stock[product_name] = product_info
    
    return low_stock

def update_stock_level(product_name, quantity_change):
    """Update stock level for a product (positive for restock, negative for sale)"""
    all_products = get_all_products()
    
    # Find the product in the appropriate category
    for category, products in PRODUCTS.items():
        if product_name in products:
            current_stock = products[product_name]['stock_level']
            new_stock = max(0, current_stock + quantity_change)
            PRODUCTS[category][product_name]['stock_level'] = new_stock
            
            return {
                'product_name': product_name,
                'old_stock': current_stock,
                'new_stock': new_stock,
                'change': quantity_change,
                'low_stock_alert': new_stock < 30
            }
    
    return None

def get_category_stats():
    """Get statistics for each category"""
    stats = {}
    
    for category, products in PRODUCTS.items():
        total_products = len(products)
        total_stock = sum(p['stock_level'] for p in products.values())
        low_stock_count = sum(1 for p in products.values() if p['stock_level'] < 30)
        
        stats[category] = {
            'total_products': total_products,
            'total_stock': total_stock,
            'low_stock_count': low_stock_count,
            'info': CATEGORIES[category]
        }
    
    return stats

def display_cart_item(item):
    """Generate HTML for a single cart item"""
    from .styles import get_cart_item_style, get_image_style, get_metric_style, COMMON_STYLES
    
    product_name = item['name']
    quantity = item['quantity']
    price = item['price']
    category = item['category']
    image_url = item['image_url']
    
    item_total = quantity * price
    category_info = CATEGORIES.get(category, {'color': '#95a5a6', 'icon': '📦'})
    
    danger_style = get_metric_style(COMMON_STYLES['danger_color'])
    
    return f"""
    <div style="{get_cart_item_style()}; border: 2px solid {category_info['color']};">
        <div style="display: flex; gap: 15px; align-items: center;">
            <img src="{image_url}" alt="{product_name}" 
                 style="{get_image_style()}; border: 2px solid {category_info['color']};">
            <div style="flex: 1;">
                <h5 style="margin: 0 0 5px 0; color: {COMMON_STYLES['text_color']};">{product_name}</h5>
                <p style="margin: 2px 0; color: {category_info['color']}; font-size: 12px; font-weight: bold;">
                    {category_info['icon']} {category}
                </p>
                <div style="display: flex; gap: 10px; margin-top: 8px; align-items: center;">
                    <span style="{get_metric_style('#3498db')}">Qty: {quantity}</span>
                    <span style="{get_metric_style(COMMON_STYLES['success_color'])}">${price:.2f}/unit</span>
                    <span style="{danger_style}; font-weight: bold;">Total: ${item_total:.2f}</span>
                </div>
            </div>
        </div>
    </div>
    """

def display_simple_product_card(product_name, product_info):
    """Simple product card without styling complexity"""
    category_info = CATEGORIES.get(product_info['category'], {'color': '#95a5a6', 'icon': '📦'})
    
    return f"""
    <div class="product-card">
        <img src="{product_info['image_url']}" alt="{product_name}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px;">
        <h5>{product_name}</h5>
        <p>{category_info['icon']} {product_info['category']}</p>
        <p>Brand: {product_info['brand']}</p>
        <p>Price: {product_info['price_range']}</p>
    </div>
    """

def extract_price_from_range(price_range):
    """Extract a numeric price from a price range string like '$999 - $1,499'"""
    if not price_range or price_range == "":
        return 0.0
    
    # Remove dollar signs and commas, then find all numbers
    clean_price = price_range.replace('$', '').replace(',', '')
    
    # Find all decimal numbers in the string
    numbers = re.findall(r'\d+\.?\d*', clean_price)
    
    if numbers:
        # If there are multiple numbers (price range), take the first one (minimum price)
        return float(numbers[0])
    
    return 0.0

def get_product_actual_price(product_name):
    """Get the actual numeric price for a product"""
    product_info = get_product_info(product_name)
    if product_info and 'price_range' in product_info:
        return extract_price_from_range(product_info['price_range'])
    return 0.0

from components import Agent
from typing import Optional


def lookup_new_sales(args: dict, history: Optional[list[dict]] = None) -> dict:
    """Checks for current promotions, discounts, or special deals."""
    category = args.get("category")
    print("[toolLogic] calling lookupNewSales(), category:", category)
    
    items = [
        {
            "item_id": 101,
            "type": "snowboard",
            "name": "Alpine Blade",
            "retail_price_usd": 450,
            "sale_price_usd": 360,
            "sale_discount_pct": 20,
        },
        {
            "item_id": 102,
            "type": "snowboard",
            "name": "Peak Bomber",
            "retail_price_usd": 499,
            "sale_price_usd": 374,
            "sale_discount_pct": 25,
        },
        {
            "item_id": 201,
            "type": "apparel",
            "name": "Thermal Jacket",
            "retail_price_usd": 120,
            "sale_price_usd": 84,
            "sale_discount_pct": 30,
        },
        {
            "item_id": 202,
            "type": "apparel",
            "name": "Insulated Pants",
            "retail_price_usd": 150,
            "sale_price_usd": 112,
            "sale_discount_pct": 25,
        },
        {
            "item_id": 301,
            "type": "boots",
            "name": "Glacier Grip",
            "retail_price_usd": 250,
            "sale_price_usd": 200,
            "sale_discount_pct": 20,
        },
        {
            "item_id": 302,
            "type": "boots",
            "name": "Summit Steps",
            "retail_price_usd": 300,
            "sale_price_usd": 210,
            "sale_discount_pct": 30,
        },
        {
            "item_id": 401,
            "type": "accessories",
            "name": "Goggles",
            "retail_price_usd": 80,
            "sale_price_usd": 60,
            "sale_discount_pct": 25,
        },
        {
            "item_id": 402,
            "type": "accessories",
            "name": "Warm Gloves",
            "retail_price_usd": 60,
            "sale_price_usd": 48,
            "sale_discount_pct": 20,
        },
    ]

    filtered_items = items if category == "any" else [item for item in items if item["type"] == category]
    
    # Sort by largest discount first
    filtered_items.sort(key=lambda x: x["sale_discount_pct"], reverse=True)
    
    return {
        "sales": filtered_items,
    }


def add_to_cart(args: dict, history: Optional[list[dict]] = None) -> dict:
    """Adds an item to the user's shopping cart."""
    item_id = args.get("item_id")
    # Implementation would go here
    return {"success": True, "item_id": item_id}


def checkout(args: dict, history: Optional[list[dict]] = None) -> dict:
    """Initiates a checkout process with the user's selected items."""
    item_ids = args.get("item_ids")
    phone_number = args.get("phone_number")
    # Implementation would go here
    return {"success": True, "item_ids": item_ids, "phone_number": phone_number}


sales_agent = Agent(
    name="salesAgent",
    public_description="Handles sales-related inquiries, including new product details, recommendations, promotions, and purchase flows. Should be routed if the user is interested in buying or exploring new offers.",
    instructions="You are a helpful sales assistant. Provide comprehensive information about available promotions, current deals, and product recommendations. Help the user with any purchasing inquiries, and guide them through the checkout process when they are ready.",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "lookupNewSales",
                "description": "Checks for current promotions, discounts, or special deals. Respond with available offers relevant to the user's query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["snowboard", "apparel", "boots", "accessories", "any"],
                            "description": "The product category or general area the user is interested in (optional).",
                        },
                    },
                    "required": ["category"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "addToCart",
                "description": "Adds an item to the user's shopping cart.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to add to the cart.",
                        },
                    },
                    "required": ["item_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "checkout",
                "description": "Initiates a checkout process with the user's selected items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_ids": {
                            "type": "array",
                            "description": "An array of item IDs the user intends to purchase.",
                            "items": {
                                "type": "string",
                            },
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "User's phone number used for verification. Formatted like '(111) 222-3333'",
                            "pattern": "^\\(\\d{3}\\) \\d{3}-\\d{4}$",
                        },
                    },
                    "required": ["item_ids", "phone_number"],
                },
            },
        },
    ],
    tool_logic={
        "lookupNewSales": lookup_new_sales,
        "addToCart": add_to_cart,
        "checkout": checkout,
    },
)
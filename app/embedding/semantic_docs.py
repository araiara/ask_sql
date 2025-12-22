ORDERS = """
Table: orders
Purpose: Stores customer purchase events.
Grain: One row per order.
Joins:
- orders.customer_id → customers.customer_id
Filters:
- status = 'completed' for revenue queries
Common analytics:
- Orders per customer
"""

ORDER_ITEMS = """
Table: order_items
Purpose: Stores customer purchase events.
Grain: One row per order.
Joins:
- products.product_id → order_items.product_id
- orders.order_id → order_items.order_id
Common analytics:
- Orders per product
- Monthly revenue
"""

CUSTOMERS = """
Table: customers
Purpose: Stores customer profile information.
Grain: One row per customer.
Common analytics:
- Orders per customer
- Customer lifetime value
"""

PRODUCTS = """
Table: products
Purpose: Product catalog.
Grain: One row per product.
Joins:
- products.category_id → categories.category_id
Common analytics:
- Revenue by product
"""

CATEGORIES = """
Table: categories
Purpose: Product classification.
Grain: One row per category.
Common analytics:
- Revenue by category
"""


def get_semantic_docs() -> dict[str, str]:
    return {
        "orders": ORDERS,
        "order_items": ORDER_ITEMS,
        "customers": CUSTOMERS,
        "products": PRODUCTS,
        "categories": CATEGORIES,
    }

"""
Shop Module - Calculate shopping cart totals with tax.

This module provides functionality to calculate the total cost of items
with automatic tax application, ignoring items not in the price catalog.
"""


def get_total(prices: dict, items: list, tax_rate: float) -> float:
    """Calculate total cost of items with tax application.
    
    Sums the prices of items from the prices dictionary, applies a tax rate,
    and returns the result rounded to two decimal places. Items not found in
    the prices dictionary are silently ignored.
    
    Args:
        prices: Dictionary mapping item names (str) to their prices (float/int).
        items: List of item names (str) to purchase.
        tax_rate: Tax rate as a decimal (e.g., 0.09 for 9% tax).
    
    Returns:
        Total cost rounded to 2 decimal places as a float.
    
    Example:
        >>> prices = {'socks': 5, 'shoes': 60, 'sweater': 30}
        >>> items = ['socks', 'shoes']
        >>> tax_rate = 0.09
        >>> get_total(prices, items, tax_rate)
        70.85
        
        Calculation:
        - 5 + 60 = 65 (subtotal)
        - 65 * 1.09 = 70.85 (with 9% tax)
    """
    # Calculate subtotal from items found in prices dict
    subtotal = sum(prices.get(item, 0) for item in items)
    
    # Apply tax and round to 2 decimal places
    total_with_tax = subtotal * (1 + tax_rate)
    
    return round(total_with_tax, 2)

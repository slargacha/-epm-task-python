"""
Unit tests for the Shop module.

Comprehensive test suite for the get_total function covering:
- Basic tax calculations
- Floating point precision
- Edge cases (empty carts, missing items, zero tax)
- Various tax rates and prices
"""

import pytest
from src.shop import get_total


class TestGetTotal:
    """Test cases for the get_total function."""
    
    # Basic functionality tests
    def test_basic_calculation(self) -> None:
        """Test basic shopping cart total calculation."""
        prices = {'socks': 5, 'shoes': 60, 'sweater': 30}
        items = ['socks', 'shoes']
        tax_rate = 0.09
        
        # 5 + 60 = 65, then 65 * 1.09 = 70.85
        result = get_total(prices, items, tax_rate)
        assert result == 70.85
    
    def test_single_item(self) -> None:
        """Test with a single item in the cart."""
        prices = {'apple': 1.5}
        items = ['apple']
        tax_rate = 0.10
        
        # 1.5 * 1.10 = 1.65
        result = get_total(prices, items, tax_rate)
        assert result == 1.65
    
    def test_multiple_items_same_product(self) -> None:
        """Test with multiple quantities of the same item."""
        prices = {'apple': 1.5}
        items = ['apple', 'apple', 'apple']
        tax_rate = 0.10
        
        # 1.5 + 1.5 + 1.5 = 4.5, then 4.5 * 1.10 = 4.95
        result = get_total(prices, items, tax_rate)
        assert result == 4.95
    
    # Tax rate variations
    def test_zero_tax_rate(self) -> None:
        """Test with 0% tax rate."""
        prices = {'item': 10}
        items = ['item']
        tax_rate = 0.0
        
        result = get_total(prices, items, tax_rate)
        assert result == 10.0
    
    def test_high_tax_rate(self) -> None:
        """Test with high tax rate (50%)."""
        prices = {'item': 100}
        items = ['item']
        tax_rate = 0.50
        
        # 100 * 1.50 = 150.0
        result = get_total(prices, items, tax_rate)
        assert result == 150.0
    
    def test_small_tax_rate(self) -> None:
        """Test with very small tax rate."""
        prices = {'item': 100}
        items = ['item']
        tax_rate = 0.001
        
        # 100 * 1.001 = 100.1
        result = get_total(prices, items, tax_rate)
        assert result == 100.1
    
    # Empty and missing items
    def test_empty_cart(self) -> None:
        """Test with an empty shopping cart."""
        prices = {'item': 10}
        items = []
        tax_rate = 0.10
        
        result = get_total(prices, items, tax_rate)
        assert result == 0.0
    
    def test_all_items_missing(self) -> None:
        """Test when all items are missing from price list."""
        prices = {'socks': 5, 'shoes': 60}
        items = ['hat', 'gloves', 'scarf']  # None in prices
        tax_rate = 0.10
        
        result = get_total(prices, items, tax_rate)
        assert result == 0.0
    
    def test_partial_items_missing(self) -> None:
        """Test when some items are missing from price list."""
        prices = {'socks': 5, 'shoes': 60}
        items = ['socks', 'hat', 'shoes', 'gloves']
        tax_rate = 0.10
        
        # Only 5 + 60 = 65, ignoring 'hat' and 'gloves'
        # 65 * 1.10 = 71.5
        result = get_total(prices, items, tax_rate)
        assert result == 71.5
    
    # Decimal precision tests
    def test_rounding_to_two_decimals(self) -> None:
        """Test that results are correctly rounded to 2 decimal places."""
        prices = {'item': 10.01}
        items = ['item']
        tax_rate = 0.07
        
        # 10.01 * 1.07 = 10.7107, should round to 10.71
        result = get_total(prices, items, tax_rate)
        assert result == 10.71
    
    def test_rounding_up(self) -> None:
        """Test rounding up to 2 decimal places."""
        prices = {'item': 10.005}
        items = ['item']
        tax_rate = 0.10
        
        # 10.005 * 1.10 = 11.0055, should round to 11.01
        result = get_total(prices, items, tax_rate)
        assert result == 11.01
    
    def test_rounding_down(self) -> None:
        """Test rounding down to 2 decimal places."""
        prices = {'item': 10.001}
        items = ['item']
        tax_rate = 0.10
        
        # 10.001 * 1.10 = 11.0011, should round to 11.00
        result = get_total(prices, items, tax_rate)
        assert result == 11.00
    
    def test_multiple_items_rounding(self) -> None:
        """Test rounding with multiple items."""
        prices = {'a': 3.33, 'b': 4.44, 'c': 5.55}
        items = ['a', 'b', 'c']
        tax_rate = 0.06
        
        # 3.33 + 4.44 + 5.55 = 13.32
        # 13.32 * 1.06 = 14.1192, should round to 14.12
        result = get_total(prices, items, tax_rate)
        assert result == 14.12
    
    # Large numbers
    def test_large_prices(self) -> None:
        """Test with large price values."""
        prices = {'luxury_item': 10000}
        items = ['luxury_item']
        tax_rate = 0.20
        
        # 10000 * 1.20 = 12000.0
        result = get_total(prices, items, tax_rate)
        assert result == 12000.0
    
    def test_many_items(self) -> None:
        """Test with many items in cart."""
        prices = {f'item{i}': i for i in range(1, 101)}
        items = [f'item{i}' for i in range(1, 101)]
        tax_rate = 0.05
        
        # Sum of 1 to 100 = 5050
        # 5050 * 1.05 = 5302.5
        result = get_total(prices, items, tax_rate)
        assert result == 5302.5
    
    # Real-world scenarios
    def test_iva_colombia(self) -> None:
        """Test with Colombian IVA (19%)."""
        prices = {'coffee': 5, 'sandwich': 8, 'juice': 3}
        items = ['coffee', 'sandwich', 'juice']
        tax_rate = 0.19
        
        # 5 + 8 + 3 = 16
        # 16 * 1.19 = 19.04
        result = get_total(prices, items, tax_rate)
        assert result == 19.04
    
    def test_usa_sales_tax(self) -> None:
        """Test with US-style sales tax (8.5%)."""
        prices = {'book': 15.99, 'pen': 2.50}
        items = ['book', 'pen']
        tax_rate = 0.085
        
        # 15.99 + 2.50 = 18.49
        # 18.49 * 1.085 = 20.0616...→ 20.06
        result = get_total(prices, items, tax_rate)
        assert result == 20.06
    
    def test_eu_vat(self) -> None:
        """Test with EU VAT (21%)."""
        prices = {'wine': 12.5, 'cheese': 8.75}
        items = ['wine', 'cheese']
        tax_rate = 0.21
        
        # 12.5 + 8.75 = 21.25
        # 21.25 * 1.21 = 25.7125→ 25.71
        result = get_total(prices, items, tax_rate)
        assert result == 25.71
    
    # Float precision edge cases
    def test_float_precision(self) -> None:
        """Test handling of floating-point precision."""
        prices = {'item': 0.1}
        items = ['item'] * 10
        tax_rate = 0.1
        
        # 0.1 * 10 = 1.0
        # 1.0 * 1.1 = 1.1
        result = get_total(prices, items, tax_rate)
        assert result == 1.1
    
    def test_negative_prices_ignored(self) -> None:
        """Test behavior with negative prices (discounts via negative prices)."""
        prices = {'item': -5}
        items = ['item']
        tax_rate = 0.10
        
        # -5 * 1.10 = -5.5
        result = get_total(prices, items, tax_rate)
        assert result == -5.5
    
    def test_zero_price_item(self) -> None:
        """Test with items priced at zero."""
        prices = {'free_item': 0, 'paid_item': 10}
        items = ['free_item', 'paid_item']
        tax_rate = 0.10
        
        # 0 + 10 = 10
        # 10 * 1.10 = 11.0
        result = get_total(prices, items, tax_rate)
        assert result == 11.0

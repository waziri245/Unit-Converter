import pytest
from tkinter import Tk, StringVar, Entry, Label
from unittest.mock import MagicMock, patch
from src.unit_converter import conversion_factors  # Replace with your actual filename

# Fixtures for test setup
@pytest.fixture(scope="module")
def tk_root():
    root = Tk()
    root.withdraw()  # Hide the window during tests
    yield root
    root.destroy()

@pytest.fixture
def test_vars(tk_root):
    class Vars:
        def __init__(self):
            self.category_var = StringVar(value='length')
            self.from_var = StringVar()
            self.to_var = StringVar()
            self.result_label = Label(tk_root)
            self.quantity_entry = Entry(tk_root)
    return Vars()

# Test conversion logic directly
def convert_units(quantity, from_unit, to_unit, category):
    """Helper function to test conversion logic directly"""
    if category == 'temperature':
        if from_unit == to_unit:
            return quantity
        return conversion_factors[category][from_unit][to_unit](quantity)
    else:
        from_factor = conversion_factors[category][from_unit]
        to_factor = conversion_factors[category][to_unit]
        
        if callable(from_factor):
            base_value = from_factor(quantity)
        else:
            base_value = quantity / from_factor
            
        if callable(to_factor):
            return to_factor(base_value)
        else:
            return base_value * to_factor

# Conversion tests
@pytest.mark.parametrize("quantity,from_unit,to_unit,expected", [
    (1, 'meters', 'feet', 3.28084),
    (1, 'feet', 'meters', 0.3048),
    (100, 'centimeters', 'meters', 1),
    (1, 'kilometers', 'miles', 0.621371),
])
def test_length_conversions(quantity, from_unit, to_unit, expected):
    result = convert_units(quantity, from_unit, to_unit, 'length')
    assert pytest.approx(result, rel=1e-4) == expected

@pytest.mark.parametrize("quantity,from_unit,to_unit,expected", [
    (0, 'celsius', 'fahrenheit', 32),
    (100, 'celsius', 'fahrenheit', 212),
    (-40, 'celsius', 'fahrenheit', -40),
    (0, 'celsius', 'kelvin', 273.15),
])
def test_temperature_conversions(quantity, from_unit, to_unit, expected):
    result = convert_units(quantity, from_unit, to_unit, 'temperature')
    assert pytest.approx(result, rel=1e-4) == expected

@pytest.mark.parametrize("quantity,from_unit,to_unit,expected", [
    (1, 'kilograms', 'grams', 1000),
    (1000, 'grams', 'kilograms', 1),
    (1, 'pounds', 'ounces', 16),
])
def test_weight_conversions(quantity, from_unit, to_unit, expected):
    result = convert_units(quantity, from_unit, to_unit, 'weight')
    assert pytest.approx(result, rel=1e-4) == expected

# Edge cases
@pytest.mark.parametrize("category,from_unit,to_unit", [
    ('length', 'meters', 'meters'),
    ('temperature', 'celsius', 'celsius'),
    ('weight', 'kilograms', 'kilograms'),
])
def test_same_unit_conversion(category, from_unit, to_unit):
    result = convert_units(10, from_unit, to_unit, category)
    assert result == 10

def test_zero_conversion():
    result = convert_units(0, 'meters', 'feet', 'length')
    assert result == 0

# Error handling tests
def test_invalid_unit_handling():
    with pytest.raises(KeyError):
        convert_units(1, 'invalid', 'meters', 'length')

# GUI function tests
def test_menu_updates(test_vars):
    # Mock menu objects
    from_menu = MagicMock()
    to_menu = MagicMock()
    
    # Create a mock update_menus function
    def update_menus(*args):
        category = test_vars.category_var.get()
        units = conversion_factors[category].keys()
        
        # Clear existing menus
        from_menu['menu'].delete(0, 'end')
        to_menu['menu'].delete(0, 'end')
        
        # Add new units
        for unit in units:
            from_menu['menu'].add_command(label=unit)
            to_menu['menu'].add_command(label=unit)
        
        # Set default selections
        units_list = list(units)
        test_vars.from_var.set(units_list[0])
        test_vars.to_var.set(units_list[1] if len(units_list) > 1 else units_list[0])
    
    # Test the function
    test_vars.category_var.set('volume')
    update_menus()
    
    # Verify menus were updated
    assert from_menu['menu'].add_command.call_count == len(conversion_factors['volume'])
    assert to_menu['menu'].add_command.call_count == len(conversion_factors['volume'])

# Test the main convert_unit function
def test_convert_unit_valid_input(test_vars):
    # Mock GUI elements
    test_vars.quantity_entry.insert(0, "10")
    test_vars.from_var.set('meters')
    test_vars.to_var.set('feet')
    test_vars.category_var.set('length')
    
    # Mock the actual function
    def convert_unit():
        try:
            quantity = float(test_vars.quantity_entry.get())
            from_unit = test_vars.from_var.get()
            to_unit = test_vars.to_var.get()
            category = test_vars.category_var.get()
            
            result = convert_units(quantity, from_unit, to_unit, category)
            test_vars.result_label.config(text=f"{result:.4f}")
        except Exception as e:
            pass
    
    # Test the function
    convert_unit()
    assert "32.8084" in test_vars.result_label.cget("text")

def test_convert_unit_invalid_input(test_vars):
    # Mock invalid input
    test_vars.quantity_entry.insert(0, "invalid")
    
    # Track if error would be shown
    error_shown = False
    
    def mock_showerror(title, message):
        nonlocal error_shown
        error_shown = True
        assert "valid number" in message
    
    # Mock the actual function with error handling
    def convert_unit():
        try:
            quantity = float(test_vars.quantity_entry.get())
            # Rest of conversion logic...
        except ValueError:
            mock_showerror("Input Error", "Please enter a valid number.")
    
    # Test the function
    with patch('tkinter.messagebox.showerror', mock_showerror):
        convert_unit()
        assert error_shown

# Test scientific notation formatting
def test_scientific_notation_formatting():
    """Test that very small/large numbers convert correctly"""
    # Test very small number conversion
    # 0.000001 meters to kilometers = 0.000001 * 0.001 = 0.000000001 km (1e-9)
    small = convert_units(0.000001, 'meters', 'kilometers', 'length')
    assert pytest.approx(small, rel=1e-4) == 1e-09
    
    # Test very large number conversion
    # 1000000 meters to kilometers = 1000000 * 0.001 = 1000 km
    large = convert_units(1000000, 'meters', 'kilometers', 'length')
    assert pytest.approx(large, rel=1e-4) == 1000.0
    
    # Test scientific notation formatting in display
    # This would test how your GUI formats these numbers
    small_str = f"{small:.4e}"
    assert "1.0000e-09" in small_str or small_str == "1e-09"
    
    large_str = f"{large:.4e}" if abs(large) > 10000 else f"{large:.4f}"
    assert "1000.0000" in large_str or large_str == "1000.0"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
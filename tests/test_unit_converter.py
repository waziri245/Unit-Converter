import pytest
from unittest.mock import patch, MagicMock
from src.unit_converter import conversion_factors

# Global mocks for all tests
@pytest.fixture(autouse=True)
def mock_gui(monkeypatch):
    """Mock all Tkinter components to run headlessly"""
    monkeypatch.setattr('tkinter.Tk', MagicMock())
    monkeypatch.setattr('tkinter.PhotoImage', MagicMock())
    monkeypatch.setattr('tkinter.StringVar', MagicMock())
    monkeypatch.setattr('tkinter.OptionMenu', MagicMock())
    monkeypatch.setattr('tkinter.Label', MagicMock())
    monkeypatch.setattr('tkinter.Entry', MagicMock())
    monkeypatch.setattr('tkinter.Frame', MagicMock())
    monkeypatch.setattr('tkinter.messagebox.showerror', MagicMock())

def test_conversion_categories():
    """Verify all expected conversion categories exist"""
    expected_categories = {
        'length', 'weight', 'temperature',
        'time', 'volume', 'speed',
        'pressure', 'area'
    }
    assert set(conversion_factors.keys()) == expected_categories

@pytest.mark.parametrize("category,unit,expected", [
    ('length', 'meters', 1.0),       # Base unit
    ('length', 'feet', 3.28084),     # 1m = 3.28084ft
    ('weight', 'grams', 1000.0),     # 1kg = 1000g
    ('time', 'hours', 1/3600.0),     # 1s = 1/3600h
    ('volume', 'milliliters', 1000.0) # 1L = 1000mL
])
def test_base_unit_conversions(category, unit, expected):
    """Test conversion factors relative to base units"""
    base_unit = next(iter(conversion_factors[category].values()))
    if isinstance(base_unit, dict):  # Skip temperature
        pytest.skip("Temperature handled separately")
    assert pytest.approx(conversion_factors[category][unit], rel=1e-4) == expected

def test_temperature_conversions():
    """Test temperature conversion formulas"""
    # Celsius to Fahrenheit
    c_to_f = conversion_factors['temperature']['celsius']['fahrenheit']
    assert pytest.approx(c_to_f(0)) == 32.0      # 0°C = 32°F
    assert pytest.approx(c_to_f(100)) == 212.0   # 100°C = 212°F
    
    # Fahrenheit to Celsius
    f_to_c = conversion_factors['temperature']['fahrenheit']['celsius']
    assert pytest.approx(f_to_c(32)) == 0.0      # 32°F = 0°C
    assert pytest.approx(f_to_c(212)) == 100.0   # 212°F = 100°C

def test_invalid_unit_handling():
    """Test error handling for invalid units"""
    with patch('tkinter.messagebox.showerror') as mock_error:
        # Simulate invalid unit access
        try:
            _ = conversion_factors['invalid_category']
            assert False, "Should raise KeyError"
        except KeyError:
            assert True
            mock_error.assert_not_called()  # Verify GUI not involved
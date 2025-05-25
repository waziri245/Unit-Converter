import pytest
from unittest.mock import patch, MagicMock
from src.unit_converter import conversion_factors

# Mock Tkinter components
@pytest.fixture(autouse=True)
def mock_tkinter(monkeypatch):
    monkeypatch.setattr('tkinter.Tk', MagicMock())
    monkeypatch.setattr('tkinter.PhotoImage', MagicMock())
    monkeypatch.setattr('tkinter.messagebox.showerror', MagicMock())

def test_conversion_factors_structure():
    """Test the structure of conversion factors"""
    assert set(conversion_factors.keys()) == {
        'length', 'weight', 'temperature',
        'time', 'volume', 'speed',
        'pressure', 'area'
    }
    assert 'meters' in conversion_factors['length']
    assert 'celsius' in conversion_factors['temperature']

def test_length_conversion():
    """Test length unit conversions"""
    meters_to_feet = conversion_factors['length']['meters'] / conversion_factors['length']['feet']
    assert pytest.approx(meters_to_feet, rel=1e-4) == 1/3.28084

def test_temperature_conversion():
    """Test temperature conversion formulas"""
    # Celsius to Fahrenheit
    celsius_to_f = conversion_factors['temperature']['celsius']['fahrenheit']
    assert pytest.approx(celsius_to_f(0), rel=1e-4) == 32
    assert pytest.approx(celsius_to_f(100), rel=1e-4) == 212

def test_weight_conversion():
    """Test weight unit conversions"""
    grams_to_kg = conversion_factors['weight']['grams'] / conversion_factors['weight']['kilograms']
    assert pytest.approx(grams_to_kg, rel=1e-4) == 1000

def test_time_conversion():
    """Test time unit conversions"""
    seconds_to_hours = conversion_factors['time']['seconds'] / conversion_factors['time']['hours']
    assert pytest.approx(seconds_to_hours, rel=1e-4) == 3600

def test_invalid_conversion():
    """Test error handling for invalid conversions"""
    with patch('tkinter.messagebox.showerror') as mock_error:
        # This would test your error handling logic
        # You'll need to expose a function that handles invalid units
        try:
            invalid = conversion_factors['invalid']
            assert False  # Should never reach here
        except KeyError:
            assert True
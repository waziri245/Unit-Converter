import pytest
from unittest.mock import MagicMock, patch
from src.unit_converter import conversion_factors

# Lightweight mocks only
@pytest.fixture(autouse=True)
def mock_gui():
    with patch('tkinter.Tk', MagicMock()), \
         patch('tkinter.PhotoImage', MagicMock()), \
         patch('tkinter.messagebox.showerror', MagicMock()):
        yield

def test_conversion_structure():
    """Verify core structure exists"""
    assert 'length' in conversion_factors
    assert 'meters' in conversion_factors['length']
    assert 'celsius' in conversion_factors['temperature']

@pytest.mark.parametrize("test_input,expected", [
    (('length', 'meters', 'feet'), 3.28084),
    (('weight', 'kilograms', 'grams'), 1000),
    (('time', 'hours', 'seconds'), 3600)
])
def test_conversion_ratios(test_input, expected):
    """Fast ratio-based testing"""
    cat, from_u, to_u = test_input
    if isinstance(conversion_factors[cat][from_u], dict):  # Skip temp
        pytest.skip("Temperature tested separately")
    ratio = conversion_factors[cat][to_u] / conversion_factors[cat][from_u]
    assert pytest.approx(ratio, rel=1e-4) == expected

def test_temperature_formulas():
    """Targeted temperature tests"""
    c_to_f = conversion_factors['temperature']['celsius']['fahrenheit']
    assert pytest.approx(c_to_f(0)) == 32
    assert pytest.approx(c_to_f(100)) == 212
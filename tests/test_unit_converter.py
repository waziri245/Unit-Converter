import pytest
from unittest.mock import MagicMock, call
import sys

@pytest.fixture(scope="module", autouse=True)
def mock_tkinter():
    """Comprehensive Tkinter mock with full StringVar functionality"""
    tk_mock = MagicMock()
    
    # Enhanced StringVar mock with trace support
    class StringVarMock:
        def __init__(self, value=None):
            self._value = value
            self.trace_handlers = []
            
        def get(self):
            return self._value
            
        def set(self, value):
            self._value = value
            
        def trace(self, mode, callback):
            # Store the callback to simulate actual trace behavior
            self.trace_handlers.append(callback)
    
    # Configure Tkinter mock
    tk_mock.Frame = MagicMock()
    tk_mock.Tk = MagicMock(return_value=MagicMock())
    tk_mock.Label = MagicMock()
    tk_mock.StringVar = StringVarMock
    tk_mock.OptionMenu = MagicMock()
    tk_mock.Button = MagicMock()
    tk_mock.Entry = MagicMock()
    tk_mock.messagebox = MagicMock()
    tk_mock.PhotoImage = MagicMock()
    
    # OptionMenu configuration to set default values
    def option_menu_wrapper(parent, variable, *values):
        variable.set(values[0] if values else "")
        return MagicMock()
    tk_mock.OptionMenu.side_effect = option_menu_wrapper
    
    # Handle wildcard imports
    tk_mock.__all__ = ['Frame', 'Tk', 'Label', 'StringVar', 
                      'OptionMenu', 'Button', 'Entry', 'messagebox']
    
    sys.modules['tkinter'] = tk_mock
    sys.modules['tkinter.messagebox'] = tk_mock.messagebox
    
    # Mock pathlib for image loading
    pathlib_mock = MagicMock()
    pathlib_mock.Path.return_value.__truediv__.return_value = "mocked_path"
    sys.modules['pathlib'] = pathlib_mock
    
    yield
    
    # Cleanup
    del sys.modules['tkinter']
    del sys.modules['tkinter.messagebox']
    del sys.modules['pathlib']

# Keep the test functions the same as before
def test_conversion_factors_structure():
    """Test the structure of conversion factors without GUI"""
    from src.unit_converter import conversion_factors
    assert 'length' in conversion_factors
    assert 'meters' in conversion_factors['length']
    assert 'celsius' in conversion_factors['temperature']

@pytest.mark.parametrize("test_input,expected", [
    (('length', 'meters', 'feet'), 3.28084),
    (('weight', 'kilograms', 'grams'), 1000),
    (('time', 'hours', 'seconds'), 3600)
])
def test_conversion_ratios(test_input, expected):
    """Test conversion ratios"""
    from src.unit_converter import conversion_factors
    cat, from_u, to_u = test_input
    
    if isinstance(conversion_factors[cat][from_u], dict):
        pytest.skip("Temperature tested separately")
        
    ratio = conversion_factors[cat][to_u] / conversion_factors[cat][from_u]
    assert pytest.approx(ratio, rel=1e-4) == expected

def test_temperature_formulas():
    """Test temperature conversion formulas"""
    from src.unit_converter import conversion_factors
    c_to_f = conversion_factors['temperature']['celsius']['fahrenheit']
    assert pytest.approx(c_to_f(0)) == 32
    assert pytest.approx(c_to_f(100)) == 212
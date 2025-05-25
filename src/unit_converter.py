
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Conversion factors dictionary
conversion_factors = {
    'length': {
        'meters': 1,
        'feet': 3.28084,
        'inches': 39.3701,
        'centimeters': 100,
        'kilometers': 0.001,
        'miles': 0.000621371,
    },
    'weight': {
        'kilograms': 1,
        'pounds': 2.20462,
        'ounces': 35.274,
        'grams': 1000,
    },
    'temperature': {
        'celsius': {
            'fahrenheit': lambda x: (x * 9/5) + 32,
            'kelvin': lambda x: x + 273.15,
            'celsius': lambda x: x
        },
        'fahrenheit': {
            'celsius': lambda x: (x - 32) * 5/9,
            'kelvin': lambda x: (x - 32) * 5/9 + 273.15,
            'fahrenheit': lambda x: x
        },
        'kelvin': {
            'celsius': lambda x: x - 273.15,
            'fahrenheit': lambda x: (x - 273.15) * 9/5 + 32,
            'kelvin': lambda x: x
        }
    },
    'time': {
        'seconds': 1,
        'minutes': 1/60,
        'hours': 1/3600,
        'days': 1/86400,
    },
    'volume': {
        'liters': 1,
        'gallons': 0.264172,
        'fluid ounces': 33.814,
        'milliliters': 1000,
    },
    'speed': {
        'meters/second': 1,
        'kilometers/hour': 3.6,
        'miles/hour': 2.23694,
    },
    'pressure': {
        'pascals': 1,
        'bars': 1e-5,
        'atmospheres': 9.86923e-6,
        'psi': 0.000145038,
    },
    'area': {
        'square meters': 1,
        'square feet': 10.7639,
        'square inches': 1550,
        'square centimeters': 10000,
        'hectares': 0.0001,
        'acres': 0.000247105,
    },
}

def convert_unit():
    """Handle unit conversion when convert button is clicked"""
    try:
        # Get and validate input quantity
        quantity_str = quantity_entry.get().strip()
        if not quantity_str:
            messagebox.showerror("Input Error", "Please enter a quantity to convert.")
            return
            
        try:
            quantity = float(quantity_str)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")
            return
            
        # Get selected units and category
        from_unit = from_var.get()
        to_unit = to_var.get()
        category = category_var.get()
        
        # Validate unit selection
        if from_unit not in conversion_factors[category] or to_unit not in conversion_factors[category]:
            messagebox.showerror("Conversion Error", "Invalid unit selection.")
            return
            
        # Handle temperature conversion (special case)
        if category == 'temperature':
            if from_unit == to_unit:
                result = quantity
            else:
                result = conversion_factors[category][from_unit][to_unit](quantity)
        else:
            # Standard conversion for other categories
            from_factor = conversion_factors[category][from_unit]
            to_factor = conversion_factors[category][to_unit]
            
            # Convert to base unit first
            if callable(from_factor):
                base_value = from_factor(quantity)
            else:
                base_value = quantity / from_factor
                
            # Convert from base unit to target unit
            if callable(to_factor):
                result = to_factor(base_value)
            else:
                result = base_value * to_factor
        
        # Format result for display
        if abs(result) < 0.001 or abs(result) > 10000:
            result_str = f"{result:.4e}"  # Scientific notation for extreme values
        else:
            result_str = f"{result:.4f}"  # Normal decimal format
            
        result_label.config(text=f"{quantity} {from_unit} = {result_str} {to_unit}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def update_menus(*args):
    """Update unit dropdown menus when category changes"""
    from_menu['menu'].delete(0, 'end')
    to_menu['menu'].delete(0, 'end')
    for unit in conversion_factors[category_var.get()].keys():
        from_menu['menu'].add_command(label=unit, command=tk._setit(from_var, unit))
        to_menu['menu'].add_command(label=unit, command=tk._setit(to_var, unit))
    from_var.set(list(conversion_factors[category_var.get()].keys())[0])
    to_var.set(list(conversion_factors[category_var.get()].keys())[1])

# Initialize main window
root = tk.Tk()
root.geometry("900x450+100+100")  # Set fixed window size
root.resizable(False, False)  # This line alone is sufficient to disable resizing
root.configure(bg="#305065")
root.title("Unit Converter")

# Additional measure to completely prevent resizing
root.overrideredirect(False)  # Ensures window decorations remain but size is fixed
root.minsize(900, 450)  # Set minimum size
root.maxsize(900, 450) 

# Try to load window icon (fails gracefully if image not found)
try:
    image_icon = PhotoImage(file=BASE_DIR / "assets" / "icons" / "calculator.png")
    root.iconphoto(False, image_icon)
except:
    pass

# Create top header frame with logos and title
Top_frame = Frame(root, bg="white", width=900, height=80)
Top_frame.place(x=0, y=0)

# Load and display logo images (if available)
try:
    Logo = PhotoImage(file=BASE_DIR / "assets" / "icons" / "calculator.png") 
    Label(Top_frame, image=Logo, bg="white").place(x=10, y=5)
except:
    pass

try:
    logo2 = PhotoImage(file=BASE_DIR / "assets" / "icons" / "ruler.png")
    Label(Top_frame, image=logo2, bg="white").place(x=90, y=5)
except:
    pass

try:
    logo3 = PhotoImage(file=BASE_DIR / "assets" / "icons" / "volume.png")
    Label(Top_frame, image=logo3, bg="white").place(x=170, y=5)
except:
    pass

try:
    logo4 = PhotoImage(file=BASE_DIR / "assets" / "icons" / "area.png")
    Label(Top_frame, image=logo4, bg="white").place(x=270, y=5)
except:
    pass

# Application title in header
Label(Top_frame, text="UNIT CONVERTER", font="arial 20 bold", bg="white", fg="black").place(x=450, y=30)

# Create input frame (left side controls)
input_frame = tk.Frame(root, padx=20, pady=20)
input_frame.pack(side="left")
input_frame.place(relx=0.35, rely=0.28)  # Exact original position

# Quantity input
quantity_label = tk.Label(input_frame, text="Quantity:")
quantity_label.grid(row=0, column=0, sticky="w")
quantity_entry = tk.Entry(input_frame, width=10)
quantity_entry.grid(row=0, column=1)

# Category dropdown
category_label = tk.Label(input_frame, text="Category:")
category_label.grid(row=3, column=0, sticky="w")
category_var = tk.StringVar(root)
category_var.set('length')
category_menu = tk.OptionMenu(input_frame, category_var, *conversion_factors.keys())
category_menu.grid(row=3, column=1)

# From unit dropdown
from_label = tk.Label(input_frame, text="From:")
from_label.grid(row=6, column=0, sticky="w")
from_var = tk.StringVar(root)
from_var.set(list(conversion_factors[category_var.get()].keys())[0])
from_menu = tk.OptionMenu(input_frame, from_var, *conversion_factors[category_var.get()].keys())
from_menu.grid(row=6, column=1)

# To unit dropdown
to_label = tk.Label(input_frame, text="To:")
to_label.grid(row=9, column=0, sticky="w")
to_var = tk.StringVar(root)
to_var.set(list(conversion_factors[category_var.get()].keys())[1])
to_menu = tk.OptionMenu(input_frame, to_var, *conversion_factors[category_var.get()].keys())
to_menu.grid(row=9, column=1)

# Convert button with icon (falls back to text if image missing)
try:
    icon = PhotoImage(file=BASE_DIR / "assets" / "icons" / "convert.png")
    convert_button = tk.Button(input_frame, text="Convert", compound="left", image=icon, 
                             command=convert_unit, width=130, height=70, bg="white")
except:
    convert_button = tk.Button(input_frame, text="Convert", command=convert_unit, 
                             width=130, height=70, bg="white")
convert_button.grid(row=12, column=0, pady=(15,0))

# Create output frame (bottom center result display)
output_frame = tk.Frame(root, width=200, height=200, bg="white")
output_frame.place(relx=0.5, rely=0.93, anchor="center")

result_label = tk.Label(output_frame, text="", font=("Arial bold", 22), fg="white", bg="#305065")
result_label.pack()

# Set up event handler for category changes
category_var.trace('w', update_menus)

# Start main event loop
root.mainloop()
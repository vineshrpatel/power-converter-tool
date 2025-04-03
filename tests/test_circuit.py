from power_converter.boost_circuit import display_boost
from power_converter.buck_circuit import display_buck
from power_converter.buckboost_circuit import display_buckboost
from power_converter.cuk_circuit import display_cuk
from power_converter.zeta_circuit import display_zeta
from power_converter.sepic_circuit import display_sepic
from power_converter.flyback_circuit import display_flyback
from power_converter.forward_circuit import display_forward
from power_converter.pushpull_circuit import display_pushpull
from power_converter.halfbridge_circuit import display_halfbridge
from power_converter.fullbridge_circuit import display_fullbridge
import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Converter Test")

# Create canvas with scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame, bg='white', width=800, height=900)
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Pack widgets
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Test values
Vin = 12      # Input voltage (V)
Lc = 0.001    # Inductance (H)
C = 0.0001    # Capacitance (F)
R_load = 10   # Load resistance (Ω)
I_load = 1.2  # Load current (A)

# Display the converter
display_boost(Vin, Lc, C, R_load, I_load, canvas)

# Start the main loop
root.mainloop()
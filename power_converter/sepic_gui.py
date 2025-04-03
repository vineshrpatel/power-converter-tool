import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from power_converter.sepic_calcs import solve_sepic_converter
from power_converter.unit_prefixes import format_value
from power_converter.sepic_circuit import display_sepic
from power_converter.sepic_simulation import ltspice_sepic_simulation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def run_sepic_gui():
    results_data = {"User Inputs": {}, "Calculations": {}}
    def calculate():
        """Fetch inputs, compute values, and update GUI."""
        try:
            Vin = float(entry_Vin.get())
            Vout = float(entry_Vout.get())
            f = float(entry_f.get())
            R_load = float(entry_Rload.get())
            rippleL_percent = float(entry_rippleL_percent.get())
            rippleVC1 = float(entry_rippleVC1.get())
            rippleVC2 = float(entry_rippleVC2.get())

            # Store user inputs
            results_data["User Inputs"] = {
                "Vin": f"{format_value(Vin)}V",
                "Vout": f"{format_value(Vout)}V",
                "f": f"{format_value(f)}Hz",
                "R_load": f"{format_value(R_load)}Ω",
                "Vripple_L_percentage": f"{format_value(rippleL_percent)}V",
                "Vripple_C1": f"{format_value(rippleVC1)}V",
                "Vripple_C2": f"{format_value(rippleVC2)}V"
            }

            results = solve_sepic_converter(Vin, Vout, f, R_load, rippleL_percent, rippleVC1, rippleVC2)

            # Store calculated results
            results_data["Calculations"] = {
                "D": f"{results['D']}",
                "I_load": f"{results['I_load']}A",
                "IL_ripple": f"{results['ripple_IL']}A",
                "L": f"{results['L']}H",
                "I_max_switch": f"{results['I_sw_max']}H",
                "C1": f"{results['C1']}F",
                "C2": f"{results['C2']}F"
            }

            # Show results labels
            results_heading.configure(text="---Results---")
            results_heading.grid(row=0, column=0, columnspan=2, sticky='w')
            D_label.configure(text=f"Duty Cycle: ")
            D_label.grid(row=1, column=0, sticky='w', pady=0)
            Iload_label.configure(text=f"Load Current: ")
            Iload_label.grid(row=2, column=0, sticky='w', pady=3)
            deltaIL_label.configure(text=f"Inductor current ripple: ")
            deltaIL_label.grid(row=3, column=0, sticky='w', pady=3)
            Lcrit_label.configure(text=f"Critical Inductance: ")
            Lcrit_label.grid(row=4, column=0, sticky='w' ,pady=3)
            max_Isw_label.configure(text=f"Max switch current: ")
            max_Isw_label.grid(row=5, column=0, sticky='w' ,pady=3)
            C1_label.configure(text=f"Capacitance 1: ")
            C1_label.grid(row=6, column=0, sticky='w', pady=3)
            C2_label.configure(text=f"Capacitance 2: ")
            C2_label.grid(row=7, column=0, sticky='w', pady=3)

            # Show results values
            D_val.configure(text=f"{results['D']}")
            D_val.grid(row=1, column=1, sticky='w')
            Iload_val.configure(text=f"{results['I_load']}A")
            Iload_val.grid(row=2, column=1, sticky='w')
            deltaIL_val.configure(text=f"{results['rippleIL']}A")
            deltaIL_val.grid(row=3, column=1, sticky='w')
            Lcrit_val.configure(text=f"{results['L']}H")
            Lcrit_val.grid(row=4, column=1, sticky='w')
            max_Isw_val.configure(text=f"{results['I_sw_max']}H")
            max_Isw_val.grid(row=5, column=1, sticky='w')
            C1_val.configure(text=f"{results['C1']}F")
            C1_val.grid(row=6, column=1, sticky='w')
            C2_val.configure(text=f"{results['C2']}F")
            C2_val.grid(row=7, column=1, sticky='w')

            display_sepic(Vin, results["L"], results["C1"], results['C2'], R_load, results["I_load"], circuit_canvas)

            # Clear previous simulation plot
            for widget in simul_frame.winfo_children():
                widget.destroy() 

            # Get simulation figure
            fig = ltspice_sepic_simulation(f,
                                        f"{str(results['D']).replace(' ', '')}",
                                        Vin,
                                        f"{str(results['L']).replace(' ', '')}",
                                        f"{str(results['C1']).replace(' ', '')}",
                                        f"{str(results['C2']).replace(' ', '')}",
                                        R_load)

            # Create canvas for the plot
            plot_canvas = FigureCanvasTkAgg(fig, master=simul_frame)
            plot_canvas.draw()
            
            # Add toolbar
            toolbar = NavigationToolbar2Tk(plot_canvas, simul_frame)
            toolbar.update()
            
            # Pack the canvas and toolbar
            toolbar.pack(side="bottom", fill="x")
            plot_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

            plt.close(fig)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    # GUI setup
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("SEPIC Converter Design")
    root.geometry("1200x500")
    root.configure(fg_color="white")  # Set root window background to white

    # Create main container with padding
    main_container = ctk.CTkFrame(root, border_width=0, fg_color='white', corner_radius=0)
    main_container.pack(fill="x", expand=True, padx=10, pady=5)

    # Create input and results within main container
    top_frame = ctk.CTkFrame(main_container, border_width=0, fg_color='white', corner_radius=0)
    top_frame.pack(fill="x", pady=(0,10))
    left_frame = ctk.CTkFrame(top_frame, border_width=0, fg_color='white', corner_radius=0)
    left_frame.pack(side="left", fill="y", padx=(0, 10))
    separator = ttk.Separator(top_frame, orient='vertical')
    separator.pack(side="left", fill="y", padx=20)
    right_frame = ctk.CTkFrame(top_frame, border_width=0, fg_color='white', corner_radius=0)
    right_frame.pack(side="left", fill="y", padx=(10, 0))

    # Create frame for circuit and simulation
    display_frame = ctk.CTkFrame(main_container, border_width=0, fg_color='white', corner_radius=0)
    display_frame.pack(fill="both", expand=True, pady=5)
    circuit_frame = ctk.CTkFrame(display_frame, border_width=1, fg_color='white', corner_radius=0, width=500, height=300)
    circuit_frame.pack(side="left", fill="both", expand=True, padx=0)
    circuit_frame.grid_rowconfigure(0, weight=1)
    circuit_frame.grid_columnconfigure(0, weight=1)
    simul_frame = ctk.CTkFrame(display_frame, border_width=1, fg_color='white', corner_radius=0, height=300, width=400)
    simul_frame.pack(side="left", fill="both", expand=True, padx=0)

    # Create canvas for circuit diagram with expanded size
    circuit_canvas = ctk.CTkCanvas(circuit_frame, bg='white')
    circuit_scrollbar = ctk.CTkScrollbar(circuit_frame, orientation="vertical", command=circuit_canvas.yview)
    circuit_canvas.configure(yscrollcommand=circuit_scrollbar.set)
    circuit_canvas.grid(row=0, column=0, sticky="nsew")
    circuit_scrollbar.grid(row=0, column=1, sticky="ns")

    set_font = ("Helvetica", 12)
    #######
    # Display Input data
    ctk.CTkLabel(left_frame, text="---Input Data---", font=set_font, height=0).grid(row=0, column=0, columnspan=2, sticky='w')
    ctk.CTkLabel(left_frame, text="Input Voltage (V): ", font=set_font, height=0).grid(row=1, column=0, sticky='w')
    entry_Vin = ctk.CTkEntry(left_frame, height=0, width=80, border_width=1, corner_radius=3, font=set_font)
    entry_Vin.grid(row=1, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Output Voltage (V): ", font=set_font, height=0).grid(row=2, column=0, sticky='w')
    entry_Vout = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_Vout.grid(row=2, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Frequency (Hz): ", font=set_font, height=0).grid(row=3, column=0, sticky='w')
    entry_f = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_f.grid(row=3, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Load Resistance (Ω): ", font=set_font, height=0).grid(row=4, column=0, sticky='w')
    entry_Rload = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_Rload.grid(row=4, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Inductor Current Ripple (%): ", font=set_font, height=0).grid(row=5, column=0, sticky='w')
    entry_rippleL_percent = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_rippleL_percent.grid(row=5, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="C1 Voltage Ripple (V): ", font=set_font, height=0).grid(row=6, column=0, sticky='w')
    entry_rippleVC1 = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_rippleVC1.grid(row=6, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="C2 Voltage Ripple (V): ", font=set_font, height=0).grid(row=7, column=0, sticky='w')
    entry_rippleVC2 = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_rippleVC2.grid(row=7, column=1, pady=1)    
    
    ctk.CTkButton(left_frame, text="Calculate", command=calculate, font=set_font, height=2, width=80, corner_radius=3).grid(row=8, column=1, pady=(5,5))

    ########
    # Results
    results_heading = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    # Create labels but don't grid them yet
    D_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Iload_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Lcrit_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    max_Isw_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C1_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C2_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    # Corresponding values for labels (don't grid yet)
    D_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Iload_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Lcrit_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    max_Isw_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C1_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C2_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    
    def on_mouse_wheel(event):
        direction = - event.delta / 600
        circuit_canvas.yview_scroll(int(direction * 5), "units")

    circuit_canvas.bind("<MouseWheel>", on_mouse_wheel)

    root.mainloop()
    
    return results_data
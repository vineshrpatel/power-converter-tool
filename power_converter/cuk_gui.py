import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from power_converter.cuk_calcs import solve_cuk_converter
from power_converter.unit_prefixes import format_value
from power_converter.cuk_circuit import display_cuk
from power_converter.cuk_simulation import ltspice_cuk_simulation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def run_cuk_gui():
    results_data = {"User Inputs": {}, "Calculations": {}}
    def calculate():
        """Fetch inputs, compute values, and update GUI."""
        try:
            Vin = float(entry_Vin.get())
            Vout = float(entry_Vout.get())
            f = float(entry_f.get())
            R_load = float(entry_Rload.get())
            rippleV1 = float(entry_rippleV1.get())
            rippleVout = float(entry_rippleVout.get())
            
            try:
                L1 = float(entry_L1.get()) if entry_L1.get().strip() else None
                L2 = float(entry_L2.get()) if entry_L2.get().strip() else None
            except ValueError:
                L1 = None
                L2 = None


            # Store user inputs
            results_data["User Inputs"] = {
                "Vin": f"{format_value(Vin)}V",
                "Vout": f"{format_value(Vout)}V",
                "f": f"{format_value(f)}Hz",
                "R_load": f"{format_value(R_load)}Ω",
                "Vripple_C1": f"{format_value(rippleV1)}V",
                "Vripple_Cout": f"{format_value(rippleVout)}V",
                "L1": f"{format_value(L1)}H",
                "L2": f"{format_value(L2)}H",
            }

            results = solve_cuk_converter(Vin, Vout, f, R_load, rippleV1, rippleVout, L1, L2)

            # Store calculated results
            results_data["Calculations"] = {
                "D": f"{results['D']}",
                "I_load": f"{results['I_load']}A",
                "L_primary": f"{results['L1c']}H",
                "L_secondary": f"{results['L2c']}H",
                "C1": f"{results['C1_min']}F",
                "Cout": f"{results['Cout_min']}F",
                "IL_primary_ripple": f"{results['IL1_ripple']}A",
                "IL_secondary_ripple": f"{results['IL2_ripple']}A",          
                "IL_max_switch": f"{results['I_sw_max']}A",
            }
            
            # Show results labels
            results_heading.configure(text="---Results---")
            results_heading.grid(row=0, column=0, columnspan=2, sticky='w')
            D_label.configure(text=f"Duty Cycle: ")
            D_label.grid(row=1, column=0, sticky='w', pady=0)
            Iload_label.configure(text=f"Load Current: ")
            Iload_label.grid(row=2, column=0, sticky='w', pady=3)
            L1crit_label.configure(text=f"Critical Inductance 1: ")
            L1crit_label.grid(row=3, column=0, sticky='w' ,pady=3)
            L2crit_label.configure(text=f"Critical Inductance 2: ")
            L2crit_label.grid(row=4, column=0, sticky='w', pady=3)
            C1_label.configure(text=f"Capacitance 1: ")
            C1_label.grid(row=5, column=0, sticky='w', pady=3)
            C2_label.configure(text=f"Capacitance 2: ")
            C2_label.grid(row=6, column=0, sticky='w', pady=3)
            deltaIL1_label.configure(text=f"Inductor 1 current ripple: ")
            deltaIL1_label.grid(row=7, column=0, sticky='w', pady=3)
            deltaIL2_label.configure(text=f"Inductor 1 current ripple: ")
            deltaIL2_label.grid(row=8, column=0, sticky='w', pady=3)
            maxIsw_label.configure(text=f"Maximum switch current: ")
            maxIsw_label.grid(row=9, column=0, sticky='w', pady=3)

            # Show results values
            D_val.configure(text=f"{results['D']}")
            D_val.grid(row=1, column=1, sticky='w')
            Iload_val.configure(text=f"{results['I_load']}A")
            Iload_val.grid(row=2, column=1, sticky='w')
            L1crit_val.configure(text=f"{results['L1c']}H")
            L1crit_val.grid(row=3, column=1, sticky='w')
            L12crit_val.configure(text=f"{results['L2c']}H")
            L12crit_val.grid(row=4, column=1, sticky='w')
            C1_val.configure(text=f"{results['C1_min']}F")
            C1_val.grid(row=5, column=1, sticky='w')
            C2_val.configure(text=f"{results['Cout_min']}F")
            C2_val.grid(row=6, column=1, sticky='w')
            deltaIL1_val.configure(text=f"{results['IL1_ripple']}A")
            deltaIL1_val.grid(row=7, column=1, sticky='w')
            deltaIL2_val.configure(text=f"{results['IL2_ripple']}A")
            deltaIL2_val.grid(row=8, column=1, sticky='w')
            maxIsw_val.configure(text=f"{results['I_sw_max']}A")
            maxIsw_val.grid(row=9, column=1, sticky='w')

            # Only show second set of results if L was provided
            if L1 is not None or L2 is not None:
                L1 = format_value(L1)
                L2 = format_value(L2)

                results2_heading.configure(text=f"For L1 = {L1}H and L2= {L2}H:")
                results2_heading.grid(row=1, column=2, columnspan=2, sticky='w', pady=5)
                C2_changed_label.configure(text=f"Capacitor 2: ")
                C2_changed_label.grid(row=2, column=2, sticky='w', pady=5)
                deltaIL1_changed_label.configure(text=f"Inductor 1 current ripple: ")
                deltaIL1_changed_label.grid(row=3, column=2, sticky='w', pady=5)
                deltaIL2_changed_label.configure(text=f"Inductor 2 current ripple: ")
                deltaIL2_changed_label.grid(row=4, column=2, sticky='w', pady=5)
                maxIsw_changed_label.configure(text=f"Maximum switch current: ")
                maxIsw_changed_label.grid(row=5, column=2, sticky='w', pady=5)

                C2_changed_val.configure(text=f"{results['Cout_min2']}A")
                C2_changed_val.grid(row=2, column=3, sticky='w')
                delta_IL1_changed_val.configure(text=f"{results['L1ripple2']}A")
                delta_IL1_changed_val.grid(row=3, column=3, sticky='w')
                deltaIL2_changed_val.configure(text=f"{results['L2ripple2']}A")
                deltaIL2_changed_val.grid(row=4, column=3, sticky='w')
                maxIsw_changed_val.configure(text=f"{results['I_sw_max2']}A")
                maxIsw_changed_val.grid(row=5, column=3, sticky='w')
                L1 = results['L1c']
                L2 = results['L2c']

                results_data["Additional Calculations"] = {
                    "Custom_L1": f"{L1}H",
                    "Custom_L2": f"{L2}H",
                    "Cout_(for custom L)": f"{results['Cout_min2']}F",
                    "IL_ripple_(for custom L1)": f"{results['L1ripple2']}A",
                    "IL_ripple_(for custom L2)": f"{results['L2ripple2']}A",
                    "I_max_switch_(for custom L)": f"{results['I_sw_max2']}A"
                }
            else:
                # Clear second set of results if L is not provided
                results2_heading.configure(text="")
                C2_changed_label.configure(text="")
                deltaIL2_changed_label.configure(text="")
                deltaIL2_changed_label.configure(text="")
                maxIsw_changed_label.configure(text="")

                C2_changed_val.configure(text="")
                deltaIL2_changed_val.configure(text="")
                deltaIL2_changed_val.configure(text="")
                maxIsw_changed_val.configure(text="")

                L1 = results['L1c']
                L2 = results['L2c']

                if "Additional Calculations" in results_data:
                    del results_data["Additional Calculations"]

            # Clear previous circuit drawing
            # circuit_canvas.delete("all")
            # Draw circuit with updated values
            display_cuk(Vin, L1, results["C1_min"], L2, results['Cout_min'], R_load, results["I_load"], circuit_canvas)

            # Clear previous simulation plot
            for widget in simul_frame.winfo_children():
                widget.destroy() 

            # Get simulation figure
            fig = ltspice_cuk_simulation(f,
                                        f"{str(results['D']).replace(' ', '')}",
                                        Vin,
                                        f"{str(L1).replace(' ', '')}", 
                                        f"{str(results['C1_min']).replace(' ', '')}",
                                        f"{str(L2).replace(' ', '')}",
                                        f"{str(results['Cout_min']).replace(' ', '')}",
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
    root.title("Ćuk Converter Design")
    root.geometry("1200x600")
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
    circuit_frame = ctk.CTkFrame(display_frame, border_width=1, fg_color='white', corner_radius=0, width=500, height=315)
    circuit_frame.pack(side="left", fill="both", expand=True, padx=0)
    circuit_frame.grid_rowconfigure(0, weight=1)
    circuit_frame.grid_columnconfigure(0, weight=1)
    simul_frame = ctk.CTkFrame(display_frame, border_width=1, fg_color='white', corner_radius=0, height=315, width=400)
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
    ctk.CTkLabel(left_frame, text="C1 Ripple Voltage (V): ", font=set_font, height=0).grid(row=5, column=0, sticky='w')
    entry_rippleV1 = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_rippleV1.grid(row=5, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Cout Ripple Voltage (V): ", font=set_font, height=0).grid(row=6, column=0, sticky='w')
    entry_rippleVout = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_rippleVout.grid(row=6, column=1, pady=1)
    
    ctk.CTkButton(left_frame, text="Calculate", command=calculate, font=set_font, height=2, width=80, corner_radius=3).grid(row=7, column=1, pady=(5,5))

    ########
    # Results
    results_heading = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    # Create labels but don't grid them yet
    D_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Iload_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    L1crit_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    L2crit_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C1_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C2_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL1_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL2_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    maxIsw_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    # Corresponding values for labels (don't grid yet)
    D_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Iload_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    L1crit_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    L12crit_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C1_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C2_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL1_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL2_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    maxIsw_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    #######
    # Additional inputs and results
    L_frame = ctk.CTkFrame(left_frame, border_width=0, fg_color='white', corner_radius=0)
    L_frame.grid(row=8, column=0, columnspan=2, sticky='ew')

    ctk.CTkLabel(L_frame, text="Enter desired inductances for CCM or DCM.", font=set_font, height=0).grid(row=0, column=0, columnspan=2, sticky='w')
    ctk.CTkLabel(L_frame, text="Inductance 1 (H):", font=set_font, height=0).grid(row=1, column=0, sticky='w')
    ctk.CTkLabel(L_frame, text="Inductance 2 (H):", font=set_font, height=0).grid(row=2, column=0, sticky='w')
    entry_L1 = ctk.CTkEntry(L_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_L1.grid(row=1, column=1, pady=1)
    entry_L2 = ctk.CTkEntry(L_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_L2.grid(row=2, column=1, pady=1)

    results2_heading = ctk.CTkLabel(right_frame, text="", font=set_font)
    results2_heading.grid(row=1, column=2, columnspan=2, sticky='w', padx=(40,0))
    C2_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C2_changed_label.grid(row=2, column=2, sticky='w', padx=(40,0))
    deltaIL1_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL1_changed_label.grid(row=3, column=2, sticky='w', padx=(40,0))
    deltaIL2_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL2_changed_label.grid(row=4, column=2, sticky='w', padx=(40,0))
    maxIsw_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    maxIsw_changed_label.grid(row=5, column=2, sticky='w', padx=(40,0))

    C2_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)    
    delta_IL1_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL2_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    maxIsw_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    ctk.CTkButton(L_frame, text="Updated L", command=calculate, font=set_font, height=5, width=80, corner_radius=3).grid(row=3, column=1, pady=(5,0))

    def on_mouse_wheel(event):
        direction = - event.delta / 600
        circuit_canvas.yview_scroll(int(direction * 5), "units")

    circuit_canvas.bind("<MouseWheel>", on_mouse_wheel)

    root.mainloop()

    return results_data
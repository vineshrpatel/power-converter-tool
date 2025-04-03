import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from power_converter.halfbridge_calcs import solve_halfbridge_converter
from power_converter.unit_prefixes import format_value
from power_converter.halfbridge_circuit import display_halfbridge
from power_converter.halfbridge_simulation import ltspice_halfbridge_simulation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def run_halfbridge_gui():
    results_data = {"User Inputs": {}, "Calculations": {}}
    def calculate():
        """Fetch inputs, compute values, and update GUI."""
        try:
            Vin = float(entry_Vin.get())
            Vout = float(entry_Vout.get())
            f = float(entry_f.get())
            n = float(entry_n.get())
            R_load = float(entry_Rload.get())
            rippleV = float(entry_rippleV.get())
            
            # Try to get inductance value, set to None if empty or invalid
            try:
                L = float(entry_L.get()) if entry_L.get().strip() else None
            except ValueError:
                L = None

            # Store user inputs
            results_data["User Inputs"] = {
                "Vin": f"{format_value(Vin)}V",
                "Vout": f"{format_value(Vout)}V",
                "f": f"{format_value(f)}Hz",
                "Turn Ratio": n,
                "R_load": f"{format_value(R_load)}Ω",
                "Vripple": f"{format_value(rippleV)}V",
                "L": f"{format_value(L)}H"
            }

            results = solve_halfbridge_converter(Vin, Vout, f, n, R_load, rippleV, L)

            # Store calculated results
            results_data["Calculations"] = {
                "D": f"{results['D']}",
                "I_load": f"{results['I_load']}A",
                "L_primary": f"{results['Lcrit']}H",
                "L_secondary": f"{results['Ls']}H",
                "C": f"{results['C']}F",
                "IL_primary_ripple": f"{results['ripple_IL']}A"
            }

            # Update and show labels
            results_heading.configure(text="---Results---")
            results_heading.grid(row=0, column=0, columnspan=2, sticky='w')
            D_label.configure(text=f"Duty Cycle: ")
            D_label.grid(row=1, column=0, sticky='w')
            Iload_label.configure(text=f"Load Current: ")
            Iload_label.grid(row=2, column=0, sticky='w', pady=3)
            Lcrit_label.configure(text=f"Critical Inductance: ")
            Lcrit_label.grid(row=3, column=0, sticky='w', pady=3)
            Ls_label.configure(text=f"Critical Inductance (secondary): ")
            Ls_label.grid(row=4, column=0, sticky='w', pady=3)  
            C_label.configure(text=f"Capacitance: ")
            C_label.grid(row=5, column=0, sticky='w', pady=3)
            deltaIL_label.configure(text=f"Inductor current ripple: ")
            deltaIL_label.grid(row=6, column=0, sticky='w', pady=3)

            # Update and show values
            D_val.configure(text=f"{results['D']}")
            D_val.grid(row=1, column=1, sticky='w')
            Iload_val.configure(text=f"{results['I_load']}A")
            Iload_val.grid(row=2, column=1, sticky='w')
            Lcrit_val.configure(text=f"{results['Lcrit']}H")
            Lcrit_val.grid(row=3, column=1, sticky='w')
            Ls_val.configure(text=f"{results['Ls']}H")
            Ls_val.grid(row=4, column=1, sticky='w')
            C_val.configure(text=f"{results['C']}F")
            C_val.grid(row=5, column=1, sticky='w')
            deltaIL_val.configure(text=f"{results['ripple_IL']}A")
            deltaIL_val.grid(row=6, column=1, sticky='w')

            # Only show second set of results if L was provided
            if L is not None:
                L = format_value(L)
                Ls = results['Ls_changed']
                results2_heading.configure(text=f"For L = {L}H:")
                results2_heading.grid(row=1, column=2, columnspan=2, sticky='w')
                Ls_changed_label.configure(text=f"Secondary Inductance: ")
                Ls_changed_label.grid(row=2, column=2, sticky='w')
                deltaIL_changed_label.configure(text=f"Inductor current ripple: ")
                deltaIL_changed_label.grid(row=3, column=2, sticky='w')
                C_changed_label.configure(text=f"Capacitance: ")
                C_changed_label.grid(row=4, column=2, sticky='w')

                Ls_changed_val.configure(text=f"{results['Ls_changed']}H")
                Ls_changed_val.grid(row=2, column=3, sticky='w')
                deltaIL_changed_val.configure(text=f"{results['ripple_IL_changed']}A")
                deltaIL_changed_val.grid(row=3, column=3, sticky='w')
                C_changed_val.configure(text=f"{results['C_changed']}F")
                C_changed_val.grid(row=4, column=3, sticky='w')

                results_data["Additional Calculations"] = {
                    "Custom_L": f"{L}H",
                    "Ls_(for custom L)": f"{results['Ls_changed']}H",
                    "IL_ripple_(for custom L)": f"{results['ripple_IL_changed']}A",
                    "C_(for custom L)": f"{results['C_changed']}F"
                }
            else:
                # Clear second set of results if L is not provided
                results2_heading.configure(text="")
                Ls_changed_label.configure(text="")
                deltaIL_changed_label.configure(text="")
                C_changed_label.configure(text="")

                Ls_changed_val.configure(text="")
                deltaIL_changed_val.configure(text="")
                C_changed_val.configure(text="")
                
                L = results['Lcrit']
                Ls = results['Ls']

                if "Additional Calculations" in results_data:
                    del results_data["Additional Calculations"]

            # Clear previous circuit drawing
            circuit_canvas.delete("all")
            # Draw circuit with updated values
            display_halfbridge(Vin, L, Ls, results["C"], R_load, results["I_load"], circuit_canvas)

            # Clear previous simulation plot
            for widget in simul_frame.winfo_children():
                widget.destroy() 

            # Get simulation figure
            fig = ltspice_halfbridge_simulation(f,
                                        f"{str(results['D']).replace(' ', '')}",
                                        Vin,
                                        f"{str(L).replace(' ', '')}", 
                                        f"{str(results['Ls']).replace(' ', '')}",
                                        f"{str(results['C']).replace(' ', '')}",
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
    root.title("Half Bridge Converter Calculator")
    root.geometry("1200x600")
    root.configure(fg_color='white')

    # Create main container with padding
    main_container = ctk.CTkFrame(root, border_width=0, fg_color='white', corner_radius=0)
    main_container.pack(fill="x", expand=True, padx=10, pady=(10,10))

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
    display_frame.pack(fill="both", expand=True, pady=(5,0))
    circuit_frame = ctk.CTkFrame(display_frame, border_width=1, fg_color='white', corner_radius=0, width=500, height=350)
    circuit_frame.pack(side="left", fill="both", expand=True, padx=0)
    circuit_frame.grid_rowconfigure(0, weight=1)
    circuit_frame.grid_columnconfigure(0, weight=1)
    simul_frame = ctk.CTkFrame(display_frame, border_width=1, fg_color='white', corner_radius=0, height=350, width=400)
    simul_frame.pack(side="left", fill="both", expand=True, padx=0)

    # Create canvas for circuit diagram with expanded size
    circuit_canvas = ctk.CTkCanvas(circuit_frame, bg='white')
    circuit_scrollbar = ctk.CTkScrollbar(circuit_frame, orientation="vertical", command=circuit_canvas.yview)
    circuit_canvas.configure(yscrollcommand=circuit_scrollbar.set)
    circuit_canvas.grid(row=0, column=0, sticky="nsew")
    circuit_scrollbar.grid(row=0, column=1, sticky="ns")

    #####
    # Display Input data
    set_font = ("Helvetica", 12)
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
    ctk.CTkLabel(left_frame, text="Turns Ratio: ", font=set_font, height=0).grid(row=4, column=0, sticky='w')
    entry_n = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_n.grid(row=4, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Load Resistance (Ω): ", font=set_font, height=0).grid(row=5, column=0, sticky='w')
    entry_Rload = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_Rload.grid(row=5, column=1, pady=1)
    ctk.CTkLabel(left_frame, text="Ripple Voltage (V): ", font=set_font, height=0).grid(row=6, column=0, sticky='w')
    entry_rippleV = ctk.CTkEntry(left_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_rippleV.grid(row=6, column=1, pady=1)
    
    ctk.CTkButton(left_frame, text="Calculate", command=calculate, font=set_font, height=2, width=80, corner_radius=3).grid(row=7, column=1, pady=(5,5))

    ########
    # Display Results
    results_heading = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    # Create labels but don't grid them yet
    D_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Iload_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Lcrit_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Ls_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    # Corresponding values for labels (don't grid yet)
    D_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Iload_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Lcrit_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Ls_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    #######
    # Additional inputs and results
    L_frame = ctk.CTkFrame(left_frame, border_width=0, fg_color='white', corner_radius=0)
    L_frame.grid(row=8, column=0, columnspan=2, sticky='ew')

    ctk.CTkLabel(L_frame, text="Enter desired inductance for CCM or DCM.", font=set_font, height=0).grid(row=0, column=0, columnspan=2, sticky='w')
    ctk.CTkLabel(L_frame, text="Inductance (H):", font=set_font, height=0).grid(row=1, column=0, sticky='w')
    entry_L = ctk.CTkEntry(L_frame, font=set_font, height=0, width=80, border_width=1, corner_radius=3)
    entry_L.grid(row=1, column=1, pady=1)

    results2_heading = ctk.CTkLabel(right_frame, text="", font=set_font)
    results2_heading.grid(row=1, column=2, columnspan=2, sticky='w', padx=(40,0))
    Ls_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Ls_changed_label.grid(row=2, column=2, sticky='w', padx=(40,0))
    deltaIL_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    deltaIL_changed_label.grid(row=3, column=2, sticky='w', padx=(40,0))
    C_changed_label = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C_changed_label.grid(row=4, column=2, sticky='w', padx=(40,0))

    deltaIL_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    Ls_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)
    C_changed_val = ctk.CTkLabel(right_frame, text="", font=set_font, height=0)

    ctk.CTkButton(L_frame, text="Updated L", command=calculate, font=set_font, height=5, width=80, corner_radius=3).grid(row=3, column=1, pady=(5,0))

    def on_mouse_wheel(event):
        direction = - event.delta / 600
        circuit_canvas.yview_scroll(int(direction * 5), "units")

    circuit_canvas.bind("<MouseWheel>", on_mouse_wheel)

    return root.mainloop()
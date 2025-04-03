from power_converter.unit_prefixes import format_value

# Ned Mohan & https://www.ti.com/lit/pdf/slva721
def solve_buckboost_converter(Vin, Vout, f, R_load, rippleV, L):    
    if Vin != Vout:
        # Equations
        D = Vout / (Vin + Vout) # Duty cycle
        I_load = Vout / R_load # Load current
        Lc = (R_load * ((1-D)**2)) / (2 * f) # Critical inductance
        IL_ripple = (Vin * D) / (f * Lc) # Inductor ripple current
        I_sw_max = (((IL_ripple / 2) * (Vin / (Vin-Vout))) * ((Vin-Vout)/Vin)) + (IL_ripple / 2)  # Max current switching devices must handle
        C_min = (D * Vout) / (rippleV * R_load * f) # Capacitance for desired voltage ripple
    else:
        Vout = Vin + (0.001*Vin)
        D = Vout / (Vin + Vout) # Duty cycle
        I_load = Vout / R_load # Load current
        Lc = (R_load * ((1-D)**2)) / (2 * f) # Critical inductance
        IL_ripple = (Vin * D) / (f * Lc) # Inductor ripple current
        I_sw_max = (((IL_ripple / 2) * (Vin / (Vin-Vout))) * ((Vin-Vout)/Vin)) + (IL_ripple / 2)  # Max current switching devices must handle
        C_min = (D * Vout) / (rippleV * R_load * f) # Capacitance for desired voltage ripple

    IL_ripple2 = ""
    I_sw_max2 = ""
    if L is not None:
        IL_ripple2 = (Vin * D) / (f * L) # Inductor ripple current
        I_sw_max2 = (IL_ripple2 / 2) + (I_load / (1-D)) # Max current switching devices must handle
        
        # Format these values
        IL_ripple2 = format_value(IL_ripple2)
        I_sw_max2 = format_value(I_sw_max2)

    # Format values
    I_load = format_value(I_load)
    Lc = format_value(Lc)
    IL_ripple = format_value(IL_ripple)
    I_sw_max = format_value(I_sw_max)
    C_min = format_value(C_min)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "Lc": Lc,
        "C_min": C_min,
        "IL_ripple": IL_ripple,
        "I_sw_max": I_sw_max,
        "Lripple2": IL_ripple2,
        "Maxsw2": I_sw_max2
    }

# print(solve_buckboost_converter(10, 10, 12e3, 10, 2, 12e-3))
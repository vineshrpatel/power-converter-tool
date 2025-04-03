from power_converter.unit_prefixes import format_value

# Ned Mohan & https://www.ti.com/lit/slva372
def solve_boost_converter(Vin, Vout, f, R_load, rippleV, L):    
    # Equations
    D = 1 - (Vin / Vout) # Duty cycle
    I_load = Vout / R_load # Load current
    Lc = (R_load * D * ((1-D)**2)) / (2 * f) # Critical inductance
    IL_ripple = (Vin * D) / (f * Lc) # Inductor ripple current
    I_sw_max = (IL_ripple / 2) + (I_load / (1-D)) # Max current switching devices must handle
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
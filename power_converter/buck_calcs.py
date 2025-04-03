from power_converter.unit_prefixes import format_value

# Ned Mohan & https://www.ti.com/lit/pdf/slva477
def solve_buck_converter(Vin, Vout, f, R_load, rippleV, L):    
    # Equations
    D = (Vout / Vin) # Duty cycle
    I_load = Vout / R_load # Load current
    Lc = ((1-D) * R_load) / (2 * f) # Critical inductance
    IL_ripple = ((Vin-Vout) * D) / (f * Lc) # Inductor ripple current
    I_sw_max = (IL_ripple / 2) + I_load # Max current switching devices must handle
    C = ((1-D) * Vout) / (8 * f**(2) * Lc * rippleV) # Capacitance for desired voltage ripple

    IL_ripple2 = ""
    I_sw_max2 = ""
    C2 = ""
    if L is not None:
        IL_ripple2 = (Vin * D) / (f * L)
        I_sw_max2 = (IL_ripple2 / 2) + (I_load / (1-D))
        C2 = ((1-D) * Vout) / (8 * f**(2) * L * rippleV)
        
        # Format these values
        IL_ripple2 = format_value(IL_ripple2)
        I_sw_max2 = format_value(I_sw_max2)
        C2 = format_value(C2)

    # Format values
    I_load = format_value(I_load)
    Lc = format_value(Lc)
    IL_ripple = format_value(IL_ripple)
    I_sw_max = format_value(I_sw_max)
    C = format_value(C)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "Lc": Lc,
        "C": C,
        "IL_ripple": IL_ripple,
        "I_sw_max": I_sw_max,
        "Lripple2": IL_ripple2,
        "Maxsw2": I_sw_max2,
        "C2": C2,
    }
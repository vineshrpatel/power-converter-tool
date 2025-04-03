from power_converter.unit_prefixes import format_value

# Rashid & https://www.ti.com/lit/gpn/LM2611
def solve_cuk_converter(Vin, Vout, f, R_load, rippleV1, rippleVout, L1, L2):
    # Equations
    D = Vout / (Vin + Vout) # Duty cycle
    I_load = Vout / R_load # Load current
    Lc1 = ((1-D) * R_load) / (2 * D * f) # Critical inductance1
    Lc2 = ((1-D) * R_load) / (2 * f) # Critical inductance2
    C1_min = (D * Vout) / (rippleV1 * R_load * f) # High side capacitor
    Cout_min = ((1-D) * Vout) / (8 * rippleVout * Lc2 * f**2) # Output capacitor
    I_L1_ripple = (Vin * D) / (2 * Lc1 * f)
    I_L2_ripple = (Vin * D) / (2 * Lc2 * f)
    I_max_switch = (I_load * (1+(D/(1-D)))) + (((Vin * D)/(2 * f)) * ((1/Lc1)+(1/Lc2)))

    Cout_min2 = ""
    I_L1_ripple2 = ""
    I_L2_ripple2 = ""
    I_max_switch2 = ""
    # Calculate with user-provided inductors when available
    if L1 is not None or L2 is not None:
        L1_input = L1 if L1 is not None else Lc1
        L2_input = L2 if L2 is not None else Lc2

        Cout_min2 = ((1-D) * Vout) / (8 * rippleVout * L2_input * f**2)
        I_L1_ripple2 = (Vin * D) / (2 * L1_input * f)
        I_L2_ripple2 = (Vin * D) / (2 * L2_input * f)
        I_max_switch2 = (I_load * (1+(D/(1-D)))) + (((Vin * D)/(2 * f)) * ((1/L1_input)+(1/L2_input)))
        
        # Format these values
        Cout_min2 = format_value(Cout_min2)
        I_L1_ripple2 = format_value(I_L1_ripple2)
        I_L2_ripple2 = format_value(I_L2_ripple2)
        I_max_switch2 = format_value(I_max_switch2)    

    # Format values
    I_load = format_value(I_load)
    Lc1 = format_value(Lc1)
    Lc2 = format_value(Lc2)
    C1_min = format_value(C1_min)
    Cout_min = format_value(Cout_min)
    I_L1_ripple = format_value(I_L1_ripple)
    I_L2_ripple = format_value(I_L2_ripple)
    I_max_switch = format_value(I_max_switch)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "L1c": Lc1,
        "L2c": Lc2,
        "C1_min": C1_min,
        "Cout_min": Cout_min,
        "IL1_ripple": I_L1_ripple,
        "IL2_ripple": I_L2_ripple,
        "I_sw_max": I_max_switch,
        "Cout_min2": Cout_min2,
        "L1ripple2": I_L1_ripple2,
        "L2ripple2": I_L2_ripple2,
        "I_sw_max2": I_max_switch2
    }
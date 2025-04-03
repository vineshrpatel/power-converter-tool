from power_converter.unit_prefixes import format_value

# https://vbn.aau.dk/ws/portalfiles/portal/450754731/abj_zeta_techrxiv.pdf
def solve_zeta_converter(Vin, Vout, f, R_load, rippleV, L1, L2):    
    # Equations
    D = Vout / (Vin + Vout) # Duty cycle
    I_load = Vout / R_load # Load current
    Lc1 = ((1-D)**2 * R_load) / (2 * D * f) # Critical inductance1
    Lc2 = ((1-D) * R_load) / (2 * f) # Critical inductance2
    C1 = (I_load * D) / (rippleV * f)
    C2 = (Vout * (1-D)) / (8 * Lc2 * f**2 * rippleV)
    I_L1_ripple = (Vout * (1-D))/(Lc1 * f)
    I_L2_ripple = (Vout * (1-D))/(Lc2 * f)

    C2_changed = ""
    I_L1_ripple_changed = ""
    I_L2_ripple_changed = ""
    if L1 is not None or L2 is not None:
        L1_input = L1 if L1 is not None else Lc1
        L2_input = L2 if L2 is not None else Lc2

        C2_changed = (Vout * (1-D)) / (8 * L2_input * f**2 * rippleV)
        I_L1_ripple_changed = (Vout * (1-D))/(L1_input * f)
        I_L2_ripple_changed = (Vout * (1-D))/(L2_input * f)
        
        # Format these values
        C2_changed = format_value(C2_changed)
        I_L1_ripple_changed = format_value(I_L1_ripple_changed)
        I_L2_ripple_changed = format_value(I_L2_ripple_changed)

    # Format values
    I_load = format_value(I_load)
    Lc1 = format_value(Lc1)
    Lc2 = format_value(Lc2)
    I_L1_ripple = format_value(I_L1_ripple)
    I_L2_ripple = format_value(I_L2_ripple)
    C1 = format_value(C1)
    C2 = format_value(C2)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "Lc1": Lc1,
        "Lc2": Lc2,
        "C1": C1,
        "C2": C2,
        "IL1_ripple": I_L1_ripple,
        "IL2_ripple": I_L2_ripple,
        "C2_changed": C2_changed,
        "I_L1_ripple_changed": I_L1_ripple_changed,
        "I_L2_ripple_changed": I_L2_ripple_changed
    }
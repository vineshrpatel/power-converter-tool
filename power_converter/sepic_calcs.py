from power_converter.unit_prefixes import format_value

# https://www.onsemi.com/pub/collateral/and90136-d.pdf
def solve_sepic_converter(Vin, Vout, f, R_load, rippleL_percent, rippleC1, rippleC2):
    # Equations
    D = Vout / (Vin + Vout) # Duty cycle
    I_load = Vout / R_load # Load current
    rippleIL = I_load * (Vout/Vin) * (rippleL_percent/100)
    L = (Vin * D)/(rippleIL * f)
    I_sw_max = I_load*(1+(rippleL_percent/100))*((Vout/Vin)+1)
    C1 = (I_load * D)/(rippleC1 * Vin * f)
    C2 = (I_load * D)/(rippleC2 * Vin * f)

    # Format values
    I_load = format_value(I_load)
    rippleIL = format_value(rippleIL)
    L = format_value(L)
    I_sw_max = format_value(I_sw_max)
    C1 = format_value(C1)
    C2 = format_value(C2)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "rippleIL": rippleIL,
        "L": L,
        "I_sw_max": I_sw_max,
        "C1": C1,
        "C2": C2,
    }
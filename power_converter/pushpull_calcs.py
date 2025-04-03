from power_converter.unit_prefixes import format_value

# Rashid
def solve_pushpull_converter(Vin, Vout, f, n, R_load, rippleV, L):
    # Equations
    D = (Vout*n)/(2*Vin)
    I_load = Vout/R_load
    Lcrit = ((1-(2*D))*R_load)/(4*f)
    Ls = Lcrit/(n**2)
    IL_ripple = (Vout(1-(2*D))) / (f * Lcrit)
    C = ((1-(2*D))*Vout)/(32*rippleV*Lcrit*f**2)

    Ls_changed = ""
    IL_ripple_changed= ""
    C_changed = ""
    if L is not None:
        L_input = L if L is not None else Lcrit

        Ls_changed = L_input/(n**2)
        IL_ripple_changed = ((Vin-Vout) * D) / (f * L_input)
        C_changed = ((1-D)*Vout)/(8*rippleV*L_input*f**2)
        
        # Format these values
        Ls_changed = format_value(Ls_changed)
        IL_ripple_changed = format_value(IL_ripple_changed)
        C_changed = format_value(C_changed)

    # Format values
    I_load = format_value(I_load)
    Lcrit = format_value(Lcrit)
    Ls = format_value(Ls)
    IL_ripple = format_value(IL_ripple)
    C = format_value(C)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "Lcrit": Lcrit,
        "Ls": Ls,
        "ripple_IL": IL_ripple,
        "C": C,
        "Ls_changed": Ls_changed,
        "ripple_IL_changed": IL_ripple_changed,
        "C_changed": C_changed,
    }

# print(solve_pushpull_converter(25, 20, 12e3, 0.3, 5, 2, None))
from power_converter.unit_prefixes import format_value

# https://www.ti.com/lit/pdf/snva994 & Rashid
def solve_flyback_converter(Vin, Vout, n, f, R_load, rippleV, L):
    # Equations
    D = (Vout*n)/(Vin+(Vout*n))
    I_load = Vout/R_load
    # Np = 1 # primary turns assumed to be 1
    # Ns = (Vout*(1-D)*Np)/(Vin*D) # secondary turns
    # n = Np/Ns # turn ratio
    Lp_crit = (n**2 * (1-D)**2 * R_load)/(2 *f) # primary inductance
    Ls_crit = Lp_crit/(n**2) # secondary inductance
    ripple_I_Lp = (Vin*D)/(Lp_crit*f) # primary inductor ripple current
    ripple_I_Ls = (Vin*D)/(Ls_crit*f) # secondary inductor ripple current
    # Vrev = ((Ns*Vin)/Np) + Vout # reverse bias volatge of diode
    C = (D*Vout)/(rippleV*R_load*f)

    Ls_changed = ""
    ripple_I_Lp_changed = ""
    ripple_I_Ls_changed = ""
    if L is not None:
        Lp_input = L if L is not None else Lp_crit

        Ls_changed = Lp_input/(n**2)
        ripple_I_Lp_changed = (Vin*D)/(Lp_input*f)
        ripple_I_Ls_changed = (Vin*D)/(Ls_changed*f)
        
        # Format these values
        Ls_changed = format_value(Ls_changed)
        ripple_I_Lp_changed = format_value(ripple_I_Lp_changed)
        ripple_I_Ls_changed = format_value(ripple_I_Ls_changed)

    # Format values
    I_load = format_value(I_load)
    Lp_crit = format_value(Lp_crit)
    Ls_crit = format_value(Ls_crit)
    ripple_I_Lp = format_value(ripple_I_Lp)
    ripple_I_Ls = format_value(ripple_I_Ls)
    # Vrev = format_value(Vrev)
    C = format_value(C)
    Vin = format_value(Vin)
    R_load = format_value(R_load)

    return {
        "D": f"{D:.3f}".rstrip('0').rstrip('.'),
        "I_load": I_load,
        "Lpcrit": Lp_crit,
        "Lscrit": Ls_crit,
        "ripple_I_Lp": ripple_I_Lp,
        "ripple_I_Ls": ripple_I_Ls,
        # "Vrev": Vrev,
        "C": C,
        "Ls_changed": Ls_changed,
        "ripple_I_Lp_changed": ripple_I_Lp_changed,
        "ripple_I_Ls_changed": ripple_I_Ls_changed
    }

# print(solve_flyback_converter(20, 40, 1, 12e3, 5, 0.5, None))
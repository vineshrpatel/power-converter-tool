def format_value(value):
    if value is not None:
        """Convert values to mH, uH, nH if required"""
        if value >= 1:
            return f"{value:.3f}".rstrip('0').rstrip('.') + " "
        elif value >= 1e-3:
            return f"{value * 1e3:.3f}".rstrip('0').rstrip('.') + " m"
        elif value >= 1e-6:
            return f"{value * 1e6:.3f}".rstrip('0').rstrip('.') + " u"
        elif value >= 1e-9:
            return f"{value * 1e9:.3f}".rstrip('0').rstrip('.') + " n"
        else:
            return f"{value:.7f} "
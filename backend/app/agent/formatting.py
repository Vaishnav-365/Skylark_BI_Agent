def format_inr(value: float | int | None) -> str:
    """
    Format a numeric value using the Indian numbering system.
    """

    if value is None:
        return "₹0.00"

    value = float(value)

    negative = value < 0
    value = abs(value)

    integer_part = int(value)
    decimal_part = round(value - integer_part, 2)

    # Handle rounding to 1.00
    if decimal_part >= 1:
        integer_part += 1
        decimal_part = 0

    integer_str = str(integer_part)

    if len(integer_str) > 3:
        last_three = integer_str[-3:]
        remaining = integer_str[:-3]

        groups = []

        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            groups.insert(0, remaining)

        integer_str = ",".join(groups + [last_three])

    formatted = f"₹{integer_str}.{int(round(decimal_part * 100)):02d}"

    if negative:
        formatted = f"-{formatted}"

    return formatted
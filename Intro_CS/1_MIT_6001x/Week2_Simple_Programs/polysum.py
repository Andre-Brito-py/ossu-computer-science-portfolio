import math

def polysum(n, s):
    """
    Input: n (number of sides), s (length of each side)
    Returns: sum of the area and square of the perimeter of the regular polygon.
    The sum is rounded to 4 decimal places.
    """
    area = (0.25 * n * s**2) / (math.tan(math.pi / n))
    perimeter = n * s
    total = area + perimeter**2
    return round(total, 4)

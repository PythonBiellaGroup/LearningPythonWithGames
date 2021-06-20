import math

def xy_from_angle_mag(angle, mag):
    # SOCAHTOA to get x and y
    return (math.cos(angle) * mag, math.sin(angle) * mag)

def angle_mag_from_xy(x, y):
    # Arctan and Pythagoras to get angle and magnitude/distance
    return (math.atan2(y, x), math.sqrt(x ** 2 + y ** 2))

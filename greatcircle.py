from math import sin, cos, asin, sqrt, degrees, radians

def great_circle(a_lat, a_lon, b_lat, b_lon):
    if (a_lon==b_lon) and (a_lat==b_lat):
        return 0
    else:
        delta_lat = abs(a_lat - b_lat)
        delta_lon = abs(a_lon - b_lon)
        a = 2.0 * sin(radians(0.5 * delta_lat))
        b = 2.0 * sin(radians(0.5 * delta_lon)) * cos(radians(a_lat))
        c = 2.0 * sin(radians(0.5 * delta_lon)) * cos(radians(b_lat))
        s = sqrt(a*a + (b*c))
        angle = 2.0 * ( degrees(asin(0.5*s)) )
        # distance in nautical miles
        distance = (angle / 360.0) * 21600.0
        return distance

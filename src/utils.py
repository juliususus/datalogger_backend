import math

def coordinatesToSpeed(lat1, lon1, timestamp1, lat2, lon2, timestamp2):
    try:
        # convert degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # mean earth radius in meters
        EARTH_RADIUS = (2*6378137+6356752)/3

        # projection onto spherical model
        x1 = EARTH_RADIUS * math.cos(lat1) * math.cos(lon1)
        y1 = EARTH_RADIUS * math.cos(lat1) * math.sin(lon1)
        z1 = EARTH_RADIUS * math.sin(lat1)

        x2 = EARTH_RADIUS * math.cos(lat2) * math.cos(lon2)
        y2 = EARTH_RADIUS * math.cos(lat2) * math.sin(lon2)
        z2 = EARTH_RADIUS * math.sin(lat2)

        dot_product = (x1 * x2 + y1 * y2 + z1 * z2)
        cos_theta = dot_product / (EARTH_RADIUS**2)
        cos_theta = 1 if cos_theta > 1 else -1 if cos_theta < -1 else cos_theta
        theta = math.acos(cos_theta)

        # distance between coordinates in meters
        dist = EARTH_RADIUS * theta

        time_seconds = abs(timestamp2 - timestamp1)
        print(time_seconds)
        speed_mps = dist / time_seconds
        speed_knots = speed_mps * 3600 / 1852
    except ZeroDivisionError:
        return 0

    return speed_knots

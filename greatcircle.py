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

def printTrips(trips,airports,portFilter):
    for key in trips:
        A, B = key.split(':')
#        if A==portFilter or B==portFilter:
        if True:
            a=str('| %10s %10s | %-30s %3s | %-30s %3s | %9.1f | %9i | %8.1f |' % (trips[key].FirstDate.isoformat(),  trips[key].LastDate.isoformat(), airports[A].Title, airports[A].State, airports[B].Title, airports[B].State, trips[key].Miles, trips[key].Flights, trips[key].Hours))
            if trips[key].RevFlights>0:
                b=str('\n| %10s %10s | %-30s %3s | %-30s %3s | %9.1f | %9i | %8.1f |' % (trips[key].RevFirstDate.isoformat(),  trips[key].RevLastDate.isoformat(), airports[B].Title, airports[B].State, airports[A].Title, airports[A].State, trips[key].Miles, trips[key].RevFlights, trips[key].RevHours))
            else:
                b=''
            c= str('\n+%23s+%36s+%36s+%11s+%11s+%9s-+' % ('-'*23, '-'*36,'-'*36, '-'*11, '-'*11,'-'*9))
        out=a+b+c
        print(out)


from math import sin, cos, asin, sqrt, degrees, radians
from sys import stdout
#from operator import itemgetter, attrgetter, methodcaller

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

def printTrips(trips,airports,sortOn,sortFilter,portFilter):
    out = ''
    st = reversed(sorted(trips.items(), key=lambda e: getattr(e[1],sortOn)))
    a=str('+%23s+%36s+%36s+%11s+%11s+%9s-+' % ('-'*23, '-'*36,'-'*36, '-'*11, '-'*11,'-'*9))
    for x in st:
        key = x[0]
        # check for filter by sortOn
        if sortFilter==None or getattr(trips[key],sortOn)>=sortFilter:
            A, B = key.split(':')
            if portFilter==None or A==portFilter or B==portFilter:
                b=str('\n| %10s %10s | %-30s %3s | %-30s %3s | %9.1f | %9i | %8.1f |\n' % (trips[key].FirstDate.isoformat(),  trips[key].LastDate.isoformat(), airports[A].Title, airports[A].State, airports[B].Title, airports[B].State, trips[key].Miles, trips[key].Flights, trips[key].Hours))
                if trips[key].RevFlights>0:
                    c=str('| %10s %10s | %-30s %3s | %-30s %3s | %9.1f | %9i | %8.1f |\n' % (trips[key].RevFirstDate.isoformat(),  trips[key].RevLastDate.isoformat(), airports[B].Title, airports[B].State, airports[A].Title, airports[A].State, trips[key].Miles, trips[key].RevFlights, trips[key].RevHours))
                else:
                    c=''
                # we use wite rather than print to suppress trailing characters
                stdout.write(out+a+b+c)
    stdout.write(a+'\n')

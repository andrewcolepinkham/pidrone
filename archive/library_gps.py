from gps import *
import time

# TPV REPORT -----------------

#return json responce from gps
def get_gps_report(gps):
    return gpsd.next()

# returns GPS position (lon,lat)
def get_position_data(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        # print "Your position: lon = " + str(longitude) + ", lat = " + str(latitude)
        return str(longitude),str(latitude)

# GPS fix status: 1=Normal fix, 2=DGPS fix, 3=RTK Fixed point, 
# 4=RTK Floating point, 5=DR fix, 6=GNSSDR fix, 7=Time (surveyed) fix, 
# 8=Simulated, 9=P(Y) fix, otherwise not present. Similar to FAA Quality Indicator in NM
def get_status(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        status = getattr(nx, 'status', "Unknown")
        return str(status)
    else:
        return ""

# NMEA mode: 0=no mode value yet seen, 1=no fix, 2=2D, 3=3D.
def get_mode(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        mode = getattr(nx, 'mode', "Unknown")
        return str(mode)
    else:
        return ""
# Time/date stamp in ISO8601 format, UTC. 
# May have a fractional part of up to .001sec precision. 
# May be absent if the mode is not 2D or 3D.
def get_time(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        time = getattr(nx, 'time', "Unknown")
        return str(time)
    else:
        return ""

# MSL Altitude in meters. 
# The geoid used is rarely specified and is often inaccurate. 
# See the comments below on geoidSep. altMSL is altHAE minus geoidSep.
def get_altMSL(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        altMSL = getattr(nx, 'altMSL', "Unknown")
        return str(altMSL)
    else:
        return ""

# Current datum. Hopefully WGS84.
def get_datum(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        datum = getattr(nx, 'datum', "Unknown")
        return str(datum)
    else:
        return ""

# Longitude error estimate in meters. Certainty unknown.
def get_epx(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        epx = getattr(nx, 'epx', "Unknown")
        return str(epx)
    else:
        return ""
# Latitude error estimate in meters. Certainty unknown.
def get_epy(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        epy = getattr(nx, 'epy', "Unknown")
        return str(epy)
    else:
        return ""

# Estimated vertical error in meters. Certainty unknown.
def get_epv(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        epv = getattr(nx, 'epv', "Unknown")
        return str(epv)
    else:
        return ""

# Latitude in degrees: +/- signifies North/South.
def get_lat(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        lat = getattr(nx, 'lat', "Unknown")
        return str(lat)
    else:
        return ""

# Longitude in degrees: +/- signifies East/West.
def get_lon(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        lon = getattr(nx, 'lon', "Unknown")
        return str(lon)
    else:
        return ""

# Speed over ground, meters per second.
def get_speed(gps):
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        speed = getattr(nx, 'speed', "Unknown")
        return str(speed)
    else:
        return ""

# SKY REPORT --------------------

# Horizontal dilution of precision, a dimensionless factor which should 
# be multiplied by a base UERE to get a circular error estimate.
def get_hdop(gps):
    nx = gpsd.next()
    if nx['class'] == 'SKY':
        hdop = getattr(nx, 'hdop', "Unknown")
        return str(hdop)
    else:
        return ""

# Vertical (altitude) dilution of precision, a dimensionless factor 
# which should be multiplied by a base UERE to get an error estimate.
def get_vdop(gps):
    nx = gpsd.next()
    if nx['class'] == 'SKY':
        vdop = getattr(nx, 'vdop', "Unknown")
        return str(vdop)
    else:
        return ""

# Number of satellite objects in "satellites" array.
def get_nSat(gps):
    nx = gpsd.next()
    if nx['class'] == 'SKY':
        nSat = getattr(nx, 'nSat', "Unknown")
        return str(nSat)
    else:
        return ""

# Number of satellites used in navigation solution.
def get_uSat(gps):
    nx = gpsd.next()
    if nx['class'] == 'SKY':
        uSat = getattr(nx, 'uSat', "Unknown")
        return str(uSat)
    else:
        return ""

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
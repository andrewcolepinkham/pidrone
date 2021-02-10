import bme280
import library_gps
import time
from datetime import datetime
import csv
from gps import *
(chip_id, chip_version) = bme280.readBME280ID()
rows = []
count = 0
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

# Init!
for i in range(10):
  status = library_gps.get_status(gpsd)
  mode = library_gps.get_mode(gpsd)
  gps_time = library_gps.get_time(gpsd)
  altMSL = library_gps.get_altMSL(gpsd)
  datum = library_gps.get_datum(gpsd)
  epx = library_gps.get_epx(gpsd)
  epy = library_gps.get_epy(gpsd)
  epv = library_gps.get_epv(gpsd)
  hdop = library_gps.get_hdop(gpsd) 
  vdop = library_gps.get_vdop(gpsd) 
  nSat = library_gps.get_nSat(gpsd)
  uSat = library_gps.get_uSat(gpsd)
  lat = library_gps.get_lat(gpsd)
  lon = library_gps.get_lon(gpsd)
  rows.append([
                  i, 
                  temperature, 
                  pressure, 
                  humidity, 
                  lat, 
                  lon, 
                  status,
                  mode,
                  gps_time,
                  altMSL,
                  datum,
                  epx,
                  epy,
                  epv,
                  speed, 
                  hdop,
                  vdop,
                  nSat,
                  uSat,
                  tm
                ])



# Main data collection loop
while count < 1000:
  tm = datetime.now().time() #Current Time
  temperature,pressure,humidity = bme280.readBME280All() # Data from TPH sensor

  # GPS Data from TPV responce
  # status = library_gps.get_status(gpsd)
  # mode = library_gps.get_mode(gpsd)
  # gps_time = library_gps.get_time(gpsd)
  # altMSL = library_gps.get_altMSL(gpsd)
  # datum = library_gps.get_datum(gpsd)
  # epx = library_gps.get_epx(gpsd)
  # epy = library_gps.get_epy(gpsd)
  # epv = library_gps.get_epv(gpsd)
  lat = library_gps.get_lat(gpsd)
  lon = library_gps.get_lon(gpsd)
  # speed = library_gps.get_speed(gpsd)

  # GPS Data from SKY responce
  # hdop = library_gps.get_hdop(gpsd) 
  # vdop = library_gps.get_vdop(gpsd) 
  # nSat = library_gps.get_nSat(gpsd)
  # uSat = library_gps.get_uSat(gpsd)

  print "Temperature : ", temperature, "C"
  print "Pressure : ", pressure, "hPa"
  print "Humidity : ", humidity, "%"
  print "Latitude : ", lat, "deg"
  print "Longitude : ", lon, "deg"
  # print "status : ", status
  print("------------------------------")
  print("\n")
  rows.append([
                count, 
                temperature, 
                pressure, 
                humidity, 
                lat, 
                lon, 
                # status,
                # mode,
                # gps_time,
                # altMSL,
                # datum,
                # epx,
                # epy,
                # epv,
                # speed, 
                # hdop,
                # vdop,
                # nSat,
                # uSat,
                tm
              ])
  count+=1
  time.sleep(1)

filename = "multisensor_readings.csv"
fields = [
          'ID', 
          'Temperature (degC)', 
          'Pressure (Pa)', 
          'Humidity (%)', 
          'Latitude (deg)', 
          'Longitude (deg)', 
          'Status',
          'Mode',
          'GPS Time',
          'AltMSL',
          'Datum',
          'EPX',
          'EPY',
          'EPV',
          'Speed',
          'Hdop',
          'Vdop',
          'nSat',
          'uSat',
          'Time']
# writing to csv file
with open(filename, 'a') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
    
    print("done")

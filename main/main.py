import bme280
import library_gps
import time
from datetime import datetime
import csv
from gps import *
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
(chip_id, chip_version) = bme280.readBME280ID()
rows = []
count = 0
while count < 50:
  tm = datetime.now().time() # time object
  temperature,pressure,humidity = bme280.readBME280All()
  gps_data = library_gps.getPositionData(gpsd)

  longitude = None
  latitude = None
  if gps_data != None:
    longitude = gps_data[0]
    latitude = gps_data[1]
  print "Temperature : ", temperature, "C"
  print "Pressure : ", pressure, "hPa"
  print "Humidity : ", humidity, "%"
  print "Latitude : ", latitude, "deg"
  print "Longitude : ", longitude, "deg"
  print("------------------------------")
  print("\n")
  rows.append([count, temperature, pressure, humidity, latitude, longitude, chip_id, chip_version, tm])
  count+=1
  time.sleep(1)

filename = "multisensor_readings.csv"
fields = ['ID', 'Temperature (degC)', 'Pressure (Pa)', 'Humidity (%)', 'Latitude (deg)', 'Latitude (deg)', 'BME180 Chip ID', 'BME180 Chip VERSION', 'Time']
# writing to csv file
with open(filename, 'a') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
    
    print("done")

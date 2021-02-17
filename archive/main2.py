import bme280
import library_gps
import time
from datetime import datetime
import csv
from gps import *

seconds = 60
backup_name = "backup.csv"
output_name = "multisensor_readings.csv"

backup_rows = []
rows = []
count = 0
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
start_time = time.time()

with open(backup_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["BACKUP-SESSION START WALK AROUND 2/15 5:30pm"])

with open(output_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["DATA START WALK AROUND 2/15 5:30pm"])
      
# Main data collection loop
while True:
  current_time = time.time()
  elapsed_time = current_time - start_time
  tm = datetime.now().time() #Current Time
  temperature,pressure,humidity = bme280.readBME280All() # Data from TPH sensor
  lat = library_gps.get_lat(gpsd)
  lon = library_gps.get_lon(gpsd)
  data = library_gps.get_gps_report(gpsd)
  # print "Temperature : ", temperature, "C"
  # print "Pressure : ", pressure, "hPa"
  # print "Humidity : ", humidity, "%"
  # print "Latitude : ", lat, "deg"
  # print "Longitude : ", lon, "deg"
  print "Data: ", str(data)
  print("------------------------------")
  print("\n")
  if elapsed_time > seconds:
    print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
    break
  backup_rows.append([
    count, 
    temperature, 
    pressure, 
    humidity, 
    data,
    tm
    ])
  rows.append([
    count, 
    temperature, 
    pressure, 
    humidity, 
    data, 
    tm
  ])
  if count % 20 == 0:
    with open(backup_name, 'a') as csvfile:
      # creating a csv writer object
      csvwriter = csv.writer(csvfile)
      # writing the fields
      csvwriter.writerow(["BACKUP-SESSION----------------------------------------------BACKUP-SESSION", "count: ", count])
      # writing the data rows
      csvwriter.writerows(rows)
      csvwriter.writerow(["BACKUP-SESSION----------------------------------------------BACKUP-SESSION", "count: ", count])
  count+=1

print("Now building data...")
fields = [
  'ID', 
  'Temperature (degC)', 
  'Pressure (Pa)', 
  'Humidity (%)', 
  'Latitude (deg)', 
  'Longitude (deg)', 
  'Mode',
  'GPS Time',
  'Alt',
  'EPX',
  'EPY',
  'EPV',
  'Speed',
  'Hdop',
  'Vdop',
  'Time'
]
# build the data objects to be pretty
output_rows = []
for row in rows:
  count = row[0]
  temp = row[1]
  pres = row[2]
  hum = row[3]
  tm = row[5] 
  lat = getattr(row[4],'lat', None)
  lon = getattr(row[4],'lon', None)
  mode = getattr(row[4],'mode', None)
  gps_time = getattr(row[4],'time', None)
  alt = getattr(row[4],'alt', None)
  epx = getattr(row[4],'epx', None)
  epy = getattr(row[4],'epy', None)
  epv = getattr(row[4],'epv', None)
  speed = getattr(row[4],'speed', None)
  hdop = getattr(row[4],'hdop', None)
  vdop = getattr(row[4],'vdop', None)
  output_rows.append([
    count,
    temp,
    pres,
    hum,
    lat,
    lon,
    mode,
    gps_time,
    alt,
    epx,
    epy,
    epv,
    speed,
    hdop,
    vdop,
    tm
  ])
# writing to csv file
with open(output_name, 'a') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(output_rows)
    
    print("done")

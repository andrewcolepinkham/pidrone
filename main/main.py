import bme280
import time
from datetime import datetime
import csv
from gps import *

seconds = 100
backup_name = "quicker_backup.csv"
output_tpv_name = "quicker_tpv.csv"
output_sky_name = "quicker_sky.csv"

rows = []
count = 0
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
start_time = time.time()

with open(output_tpv_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["Quicker TPV Data Test"])

with open(output_sky_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["Quicker SKY Data Test"])
      
# Main data collection loop
while True:
  current_time = time.time()
  elapsed_time = current_time - start_time
  tm = datetime.now().time() #Current Time
  temperature,pressure,humidity = bme280.readBME280All() # Data from TPH sensor
  data = gpsd.next()
  print "Data: ", str(data)
  print("------------------------------")
  print("\n")

  rows.append([
    count, 
    temperature, 
    pressure, 
    humidity, 
    data, 
    tm
  ])
  if count % 20 == 0 or elapsed_time > seconds:
    with open(backup_name, 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(["Quicker Backup Test"])
      csvwriter.writerow(["BACKUP-SESSION", "count: ", count])
      csvwriter.writerows(rows)
      csvwriter.writerow(["BACKUP-SESSION", "count: ", count])
  if elapsed_time > seconds:
    print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
    break
  count+=1

print("Now building data...")
fields_tpv = ['ID', 'Temperature (degC)', 'Pressure (Pa)', 'Humidity (%)', 
  'Latitude (deg)', 'Longitude (deg)', 'Mode','GPS Time','Alt','EPX',
  'EPY','EPV','Speed','Time'
]
fields_sky = ['ID', 'Temperature (degC)', 'Pressure (Pa)', 'Humidity (%)', 
  'Hdop','Vdop','Time'
]

# build the data objects to be pretty
output_tpv = []
output_sky = []
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
  if lat != None and lon != None:
    output_tpv.append([count,temp,pres,hum,lat,
      lon,mode,gps_time,alt,epx,epy,epv,speed,tm
    ])
  elif hdop != None and vdop != None:
    output_sky.append([count, temp, pres, hum,hdop, vdop, tm])

with open(output_tpv_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(fields_tpv)
  csvwriter.writerows(output_tpv)

with open(output_sky_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(fields_sky)
  csvwriter.writerows(output_sky)
print("done")

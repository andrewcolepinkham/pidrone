#bring in libraries
import bme280
import time
from datetime import datetime
import csv
from gps import *

#Define the length of data collection and output file names
seconds = 60
backup_name = "backup.csv"
output_tpv_name = "tpv.csv"
output_sky_name = "sky.csv"

rows = [] # our main data matrix
count = 0 # the ID of each line of data
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) #gps tool
start_time = time.time() # start time
broke = False # boolean to check if user has stopped data collection manually
termination_msg = "Data collection was manually terminated with Ctr+C"

#initalize first row of TPV data file
with open(output_tpv_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["TPV Data"])

#initalize first row of SKY data file
with open(output_sky_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["SKY Data"])

try:     
  # Main data collection loop
  while True:
    current_time = time.time() # keep track of time for each epoch
    elapsed_time = current_time - start_time
    tm = datetime.now().time() #Current Time
    temperature,pressure,humidity = bme280.readBME280All() # Data from TPH sensor
    data = gpsd.next() # data from the gps unit
    print ("Data: ", str(data))
    print("------------------------------")
    print("\n")
    # append to the data matrix in a naive quick way
    rows.append([
      count, 
      temperature, 
      pressure, 
      humidity, 
      data, 
      tm
    ])
    #save a quick version to the backfile just in case we dont reach the final step
    with open(backup_name, 'w') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(["Backup Data"])
      csvwriter.writerow(["BACKUP-SESSION", "count: ", count])
      csvwriter.writerows(rows)
      csvwriter.writerow(["BACKUP-SESSION", "count: ", count])
    #break the loop if we finish the seconds
    if elapsed_time > seconds:
      print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
      break
    count+=1
except KeyboardInterrupt:
  # user stopped collection so write to the backup file
  print(termination_msg)
  with open(backup_name, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Backup Data"])
    csvwriter.writerow(["BACKUP-SESSION", "count: ", count])
    csvwriter.writerows(rows)
    csvwriter.writerow(["BACKUP-SESSION", "count: ", count])
    csvwriter.writerow([termination_msg])
  broke = True

#build the output data matrix with correct headers
print("Now building data...")
fields_tpv = ['ID', 'Temperature (degC)', 'Pressure (Pa)', 'Humidity (%)', 
  'Latitude (deg)', 'Longitude (deg)', 'Mode','GPS Time','Alt','EPX',
  'EPY','EPV','Speed','Time'
]
fields_sky = ['ID', 'Temperature (degC)', 'Pressure (Pa)', 'Humidity (%)', 
  'Hdop','Vdop','Time'
]

# build the data objects and make them look pretty
output_tpv = []
output_sky = []
for row in rows:
  count = row[0]
  temp = row[1]
  pres = row[2]
  hum = row[3]
  tm = row[5] 
  #gps data is all stored in row[4], so we must get each param manually using getattr() function
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
  # sometimes we dont get a lat, long, hdop, or vdop, so catch those cases
  if lat != None and lon != None:
    output_tpv.append([count,temp,pres,hum,lat,
      lon,mode,gps_time,alt,epx,epy,epv,speed,tm
    ])
  elif hdop != None and vdop != None:
    output_sky.append([count, temp, pres, hum,hdop, vdop, tm])

#write to output files
with open(output_tpv_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(fields_tpv)
  csvwriter.writerows(output_tpv)
  if broke:
    csvwriter.writerow([termination_msg])

with open(output_sky_name, 'a') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(fields_sky)
  csvwriter.writerows(output_sky)
  if broke:
    csvwriter.writerow([termination_msg])
print("done")

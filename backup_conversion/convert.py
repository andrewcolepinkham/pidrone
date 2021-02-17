import csv
import json
import re
from python_dict_wrapper import wrap, unwrap

input_csv_name = "backup2.csv"
      
raw_rows = []
with open(input_csv_name) as csvfile:
    reader = csv.reader(csvfile) # change contents to floats
    for row in reader: # each row is a list
      if row[0] != 'BACKUP-SESSION----------------------------------------------BACKUP-SESSION':
        raw_rows.append(row)
print(raw_rows[1])
output_rows = []
for row in raw_rows:
  count = row[0]
  temp = row[1]
  pres = row[2]
  hum = row[3]
  tm = row[5] 
  s = unwrap(row[4])
  # s = s.split(None, 1)[1]
  # s = s[0:len(s)-1]
  # s = s.replace("'", "\"")
  # s = s.replace(" u", " ")
  # s = s.replace("u\"pps", "\"pps")
  # s = s.replace("False", "\"False\"")
  # s = s.replace("True", "\"True\"")
  # s = s.replace("u\"epx", "\"epx")
  # s = s.replace("u\"gdop", "\"gdop")
  # s = s.replace("[", "\"[")
  # s = s.replace("]", "]\"")
  # s = s.replace("dictwrapper: ", "")
  # s = s.replace("<", "")
  # s = s.replace(">", "")
  # s = re.sub('[.*?]', '', s)
  print(s)
  before_lat, lat, after_lat = row[4].partition('lat\': ')
  lat = after_lat.split(", ", 1)[0]
  before_lon, lon, after_lon = row[4].partition('lon\': ')
  lon = after_lon.split(", ", 1)[0]

  before_mode, mode, after_mode = row[4].partition('mode\': ')
  mode = after_mode.split(", ", 1)[0]

  before_time, time, after_time = row[4].partition('time\': ')
  gps_time = after_time.split(", ", 1)[0]
  
  before_alt, alt, after_alt = row[4].partition('alt\': ')
  alt = after_alt.split(", ", 1)[0]

  before_epx, epx, after_epx = row[4].partition('epx\': ')
  epx = after_epx.split(", ", 1)[0]

  before_epy, epy, after_epy = row[4].partition('epy\': ')
  epy = after_epy.split(", ", 1)[0]

  before_epv, epv, after_epv = row[4].partition('epv\': ')
  epv = after_epv.split(", ", 1)[0]

  before_speed, speed, after_speed = row[4].partition('speed\': ')
  speed = after_speed.split(", ", 1)[0]

  before_hdop, hdop, after_hdop = row[4].partition('hdop\': ')
  hdop = after_hdop.split(", ", 1)[0]

  before_vdop, vdop, after_vdop = row[4].partition('vdop\': ')
  vdop = after_vdop.split(", ", 1)[0]

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

# print(output_rows)

output_csv_name = "cleaned_data.csv"    
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
# writing to csv file
with open(output_csv_name, 'w') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(["DATA START WALK AROUND 2/15 5:30pm"])
  csvwriter.writerow(fields)
  csvwriter.writerows(output_rows)
  print("done")

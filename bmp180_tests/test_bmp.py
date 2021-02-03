import bmpsensor
import time
from datetime import datetime
import csv
rows = []
count = 0
while count < 1000:
    temp, pressure, altitude = bmpsensor.readBmp180()
    tm = datetime.now().time() # time object
    # print("Temperature is ", temp)  # degC
    # print("Pressure is ", pressure)  # Pressure in Pa
    # print("Altitude is ", altitude)  # Altitude in meters
    # print("\n")
    # print(tm)
    rows.append([temp, pressure, altitude, tm, count])
    count+=1
    time.sleep(.01)

filename = "bmp180_readings.csv"
fields = ['Temperature (degC)', 'Pressure (Pa)', 'Altitude (m)', 'Time']
# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
    
    print("done")

import serial
import mysql.connector
from datetime import date,datetime


if __name__ == '__main__':
  # if no Arduino connected, open port exception

  # establish serial on Raspbian
  ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

  # establish serial on Windows, check device manager or IDE for port number
  #ser = serial.Serial('COM4', 9600, timeout=1)

  ser.flush()
  
  #cursor pointed to local database on Daniel's computer, original one from Pi
  #cnx = mysql.connector.connect(host='localhost',database='vitals',user='drvega',password='AAPLcherry324')
  
  #cursor pointed to aws. Tested on Jason's local machine
  cnx = mysql.connector.connect(host='ec2-18-117-8-215.us-east-2.compute.amazonaws.com', database='vitals', user='recreate_energy', password='algae')
  
  cursor = cnx.cursor()
  
  while True:
    if ser.in_waiting > 0:
      line = ser.readline().decode('utf-8').rstrip()
      data = line.split(',')
      
      try:
        add_data = "INSERT INTO vitals(temp,ph,ADCRaw,ADCVolt,DOX,sub_date) VALUES(%s,%s,%s,%s,%s,%s)"
        data = (data[0],data[1],data[2],data[3],data[4],datetime.now())
        cursor.execute(add_data,data)
        cnx.commit()
        print(data[0]+str(" C")+str(" , ")+data[1]+str(" pH")+str(" , ")+data[2]+str(" ADC Raw")+str(" , ")+data[3]+str(" ADC Voltage")+str(" , ")+data[4]+str(" DO"))
      except IndexError:
        pass

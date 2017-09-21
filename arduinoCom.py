import serial
import array
import time

class Arduino:

  def __init__(self):
    print("Arduino object created")
  #Initialize the serial communication with the device mentioned
  def startCom(self, device):
    try:
      self.ser = serial.Serial(device ,9600, timeout=6)
      print("Waiting")
      time.sleep(5)
      return 1
    except:
      print("Arduino device not available!")
      return 0

  def closeCom(self):
    try:
      self.ser.close()
      print("serial port closed")
    except:
      print("Failed to close serial port")

  #function to set value on Arduino
  def set_value(self,lin_vel,ang_vel):
    try:
      self.ser.flushInput()
      self.ser.write("setValue "+str(lin_vel)+","+str(ang_vel)+'\n')
      y =  self.ser.readline()
      return y
    except:
      print("move_robot: Failed to write to arduino \n")

  #function to get value from Arduino
  def get_value(self,sub_cmd):
    try:
      self.ser.flushInput()
      self.ser.write("get.value :"+sub_cmd+'\n')
      x = self.ser.readline()
      return x
    except:
      print("get_value: Faild to read from arduino \n")
      return 0

  #Handskae to check that serial device we are communicating is Arduino
  def sayHello(self):
    try:
      self.ser.flushInput()
      self.ser.write("Hi_Arduino\n")
      pi = self.ser.readline().rstrip()
      print pi
      if pi == 'Hi_Raspberry':
        return 1
      else:
        self.closeCom()
        return 0
    except:
      print("sayHello: Failed to write and read from arduino")
      return 0
  #Connect to available serial devices and check
  def connect(self):
    if self.startCom('/dev/ttyACM0') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    elif self.startCom('/dev/ttyACM1') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    elif self.startCom('/dev/ttyACM2') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    elif self.startCom('/dev/ttyACM3') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    else:
      print("Couldn't connect to Arduino!!!")
      return 0

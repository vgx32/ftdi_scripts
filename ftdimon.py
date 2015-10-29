import serial
import array
import sys
import threading
import time
import binascii

def setupSerial(interface='/dev/ttyUSB0'):
  con = serial.Serial(interface, 19200)
  return con

# assume data is a byte array
def writeData(con, data):
  # print "tx:" + data.tostring()
  con.write(data)

def runDebugLog(con):
  debugThread = threading.Thread(target=debugPrints, args=(con,))
  debugThread.daemon = True
  debugThread.start()

def debugPrints(con):
  while True:
    readData(con)

def readData(con):
  # con.timeout
  data = con.readline()
  if(len(data) > 0):
    if ord(data[0]) == 0:
      sys.stdout.write("RX({0}):{1}\n".format(len(data), binascii.hexlify(data[:-1])))
    else:
      sys.stdout.write("RX({0}):{1}".format(len(data), str(data)))

  return data

def getDataFromArgs():
  data = array.array('B', [0x55, 0x56, 0x57])
  if len(sys.argv) > 1:
    dataString = sys.argv[1]
    # dataHex = dataString.decode("hex")
    dataHex = dataString
    data = array.array('B', dataHex)
  return data

def main():
  con = None
  if len(sys.argv) > 1:
    con = setupSerial('/dev/ttyUSB' + str(sys.argv[1]))
  else:
    con = setupSerial()
  
  print con
  runDebugLog(con)
  data = getDataFromArgs()
  while(True):
    time.sleep(2)
    # writeData(con, data)
  

if __name__ == "__main__":
  main()

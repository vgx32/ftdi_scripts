import serial
import array
import sys
import threading
import time
import binascii

def setupSerial():
  con = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
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
    print
  return data

def main():
  con = setupSerial()
  print con
  data = getDataFromArgs()
  
  print("writing data " + str(data))
  writeData(con, data)
  response = readData(con)
  numAttempts = 0

  while(len(response) == 0 and numAttempts < 4):
    print("no response, retrying")
    writeData(con, data)
    response = readData(con)
    
    numAttempts += 1

    time.sleep(1)
    # writeData(con, data)
  if len(response) == 0:
    print "failed to get a response from MCU"

if __name__ == "__main__":
  main()

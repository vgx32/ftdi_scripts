import sys
from ftdilib import *

def main():
  con = setupSerial(timeout=1)
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

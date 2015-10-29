import sys
from ftdilib import *



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

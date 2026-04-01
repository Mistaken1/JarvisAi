#Manual override commands here
#Add new functions in order to call them in main.py
#_________________________ IMPORTS _____________________
import sys
import time
import voice

functions = {
  "Override Command One": shutdown(),
}

def shutdown():
  time.sleep(1)
  voice.speak("Shutting down")
  sys.exit()
  
  

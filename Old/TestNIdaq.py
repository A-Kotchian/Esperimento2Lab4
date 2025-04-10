#!python

import nidaqmx
import time
import sys


if len(sys.argv)<2 :
	print("At least 1 argument needed - number of measurement")
	print("Optional arguments:")
	print("                    2) Number of  samples per channel")
	print("                    3) Waiting time")
	sys.exit(0)

nloops=int(sys.argv[1])
try: 
	samples=int(sys.argv[2])
except:
	samples=1
try: 
	waitT=float(sys.argv[3])
except:
	waitT=1
f=open("test.csv","w")
task=nidaqmx.Task()
ch1=task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
for i in range(nloops):
        risultato=task.read(number_of_samples_per_channel=samples)
        print(risultato)
        media=0
        for item in risultato:
                media+=item/len(risultato)
        f.write("%s " % media)
        f.write("\n")
        time.sleep(waitT)
f.close()


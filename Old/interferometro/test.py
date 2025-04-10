#!python


import nidaqmx
import time
import sys
import csv 


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
	
with open("test.csv","w") as f:
        with nidaqmx.Task() as task:     
                ch1=task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
        #print(ch1.ai_term_cfg)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai1",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai2",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai3",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai4",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai5",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai6",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	#task.ai_channels.add_ai_voltage_chan("Dev1/ai7",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
                for i in range(nloops):
                        risultato=task.read(number_of_samples_per_channel=samples)
                        print(risultato)

                for item in risultato:
                        for x in samples:
                                f.write("%s" % item)
                        time.sleep(waitT)



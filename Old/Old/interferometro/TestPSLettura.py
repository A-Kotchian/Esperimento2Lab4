#!python

import nidaqmx
import time
import sys
import pyvisa

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

rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::9::INSTR')
inst.query("*RST")
f=open("test.csv","w")
with nidaqmx.Task() as task:
        ch1=task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
        print(ch1.ai_term_cfg)
        inst.write("OUTP ON")
        for i in range(nloops):
                inst.write(("VOLT %d" % (10+i/10)))
                risultato=task.read(number_of_samples_per_channel=samples)
                print(risultato)
                for item in risultato:
                        f.write("%s " % item)
                f.write("\n")
                time.sleep(waitT)
inst.query("*RST")
f.close()


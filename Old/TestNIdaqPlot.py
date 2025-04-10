#!python
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%Y-%B-%d_%H-%M-%S")

if len(sys.argv)<2 :
    print("At leat 1 argument needed - number of measurement")
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

datax=[]
datay=[]	


plt.ion()
fig = plt.figure()


axes = plt.gca()
axes.set_autoscaley_on(True)
axes.set_autoscalex_on(True)
linee = axes.plot(datax, datay, 'ro-', label='ch0',linewidth=1)
plt.legend()
plt.title("Plot")
plt.ylabel("voltage (V)")
plt.xlabel("time (s)")

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
    for i in range(nloops):
        mes = task.read(number_of_samples_per_channel=samples)
        print(mes)
        mean = 0.
        for samp in mes:
            mean += samp/samples
        print(mean)
        datax.append(i*waitT)
        datay.append(mean)
        linee[0].set_xdata(datax)
        linee[0].set_ydata(datay)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(waitT)

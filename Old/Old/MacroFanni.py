#!python
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
from datetime import datetime
import pyvisa
import os

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB0::18::INSTR')
inst.write(":OUTP:STAT 1")


now = datetime.now()

current_time = now.strftime("%Y%m%d_%Hh%Mm%Ss")

if len(sys.argv)<2 :
    print("At least 1 argument needed - number of measurement")
    print("Optional arguments:")
    print("                    2) Number of samples per channel")
    print("                    3) Waiting time")
    print("                    4) Voltage increment for measure")
    sys.exit(0)

nloops=int(sys.argv[1])
samples=int(sys.argv[2])
waitT=float(sys.argv[3])
V_INCREMENT=float(sys.argv[4])
#if abs(V_INCREMENT)*abs(nloops)>140:
    #raise ValueError

datax=[]
datay=[]	


plt.ion()
fig = plt.figure()


axes = plt.gca()
axes.set_autoscaley_on(True)
axes.set_autoscalex_on(True)
linee = axes.plot(datax, datay, 'ro-', label='ch0',linewidth=1)
plt.legend()
plt.title("Intensità luminosa")

plt.ylabel("signal(V)")
if V_INCREMENT == 0.:
    plt.xlabel("time(s)")
else:
    plt.xlabel("supplì(V)")

with nidaqmx.Task() as task, open(os.path.join("data","{}_{}V_from{}Vto{}V.txt".format(current_time,V_INCREMENT,0,V_INCREMENT*nloops)), "a") as output_file:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
    inst.write("SOUR:VOLT {}".format(V_INCREMENT))
    for i in range(nloops):
        #inst.write("SOUR:VOLT {}".format(i*V_INCREMENT))
        
        read=inst.query(':READ? "defbuffer1", DATE, SOUR, READ') #legge i valori erogati dallo strumento (da fare per aggiornare il display)
        mes = task.read(number_of_samples_per_channel=samples)
        mean = 0.
        for samp in mes:
            output_file.write(str(samp)+""+read+"\n")
            mean += samp/samples
        print(mean)
        if V_INCREMENT == 0.:
            datax.append(i*waitT)
        else:
            datax.append(i*V_INCREMENT)
        datay.append(mean)
        linee[0].set_xdata(datax)
        linee[0].set_ydata(datay)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(waitT)
  

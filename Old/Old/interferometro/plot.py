#!python
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
import pyvisa

def Average(lst):
    return sum(lst) / len(lst)


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
datay0=[]	
#datay1=[]	
dd0=[0.]
#dd1=[0.]
#print("here")
axes = plt.gca()
axes.set_autoscaley_on(True)
axes.set_autoscalex_on(True)
h0, = axes.plot(datax, datay0, 'ro-', label='ch0',linewidth=1)
#h1, = axes.plot(datax, datay1,'b^-',label='ch1',linewidth=1)
plt.legend()
plt.title("Interferometro")
plt.ylabel("Intensità")
plt.xlabel("Numero Misure")
#print("there")
rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::9::INSTR')
inst.query("*RST")
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
    inst.write("OUTP ON")
    for i in range(nloops):
        inst.write(("VOLT %.1f" % (0+float(i)/2.)))
        mes=task.read(number_of_samples_per_channel=samples)
        print(mes)
        dd0[0]=0.
        for dd in mes:
                dd0[0]+=dd/len(mes)

 #       print(dd0)
        datax.append(i)
        datay0.extend(dd0)
        h0.set_xdata(datax)
        h0.set_ydata(datay0)
        axes.relim()
        axes.autoscale_view()
        plt.draw()
        plt.pause(1e-17)
        time.sleep(waitT)
inst.query("*RST")
plt.show()


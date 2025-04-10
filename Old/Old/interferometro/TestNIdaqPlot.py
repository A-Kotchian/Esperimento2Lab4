#!python
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys

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
plt.title("Beautiful Plot")
plt.ylabel("Something else (cm)")
plt.xlabel("Something (um)")
#print("there")
with nidaqmx.Task() as task:
	task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#	task.ai_channels.add_ai_voltage_chan("Dev1/ai1",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
	for i in range(nloops):
		mes=task.read(number_of_samples_per_channel=samples)
		print(mes)
		dd0[0]=0.
		for dd in mes:
                        dd0[0]+=dd/len(mes)
#		dd1[0]=0.
#		for dd in mes[1]:
#                        dd1[0]+=dd/len(mes[1])
		print(dd0)
#		print(dd1)
		datax.append(i)
		datay0.extend(dd0)
#		datay1.extend(dd1)
		h0.set_xdata(datax)
		h0.set_ydata(datay0)
#		h1.set_xdata(datax)
#		h1.set_ydata(datay1)
		axes.relim()
		axes.autoscale_view()
		plt.draw()
		plt.pause(1e-17)
		time.sleep(waitT)

plt.show()


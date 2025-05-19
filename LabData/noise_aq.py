#!python
import matplotlib.pyplot as plt
import numpy as np
import pyvisa
import time
import nidaqmx
import sys
import csv 
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%Y-%B-%d_%H-%M-%S")

if len(sys.argv)<4 :
    print("3 arguments needed:")
    print("                    1) Number of measurements")
    print("                    2) Number of  samples per channel")
    print("                    3) Acquisition Time")
    sys.exit(0)



freq = 10000                                #frequenza di campionamento S/[s]
value = 10.0                                #tensione iniziale [V]
N_data = int(sys.argv[1])                   #numero di dati da prendere
data = []                                   #array dove vengono raccolti i dati       
tempo = float(sys.argv[3])                  #durata misurazione[s]
samples=int(sys.argv[2])                    #numero di sample da prendere
waitT=tempo-float(samples)/float(freq)-tempo/100 #tempo da aspettare[s]


N_triang=3                                  #numero triangoli

step = 90*(N_triang*2)/N_data               #salto di Volt[V]
salita = (N_triang*2)

#Condizioni
if N_data % 2 == 1:
    print("Put even number of mesurementsssss")
    sys.exit(0)

if tempo-float(samples)/float(freq)< tempo/2:
    print("Too many samples per measurement")
    sys.exit(0)

#Comunicazione con DAQ System
rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::9::INSTR')    #creazione e lettura generatore


#Reset sistema
inst.write("CURR 0")
inst.write("VOLT 0")
inst.write(":OUTP:STAT 0")
inst.write("*RST")
inst.write("*RST")



inst.write("VOLT 0")        #stato iniziale [V]
inst.write("CURR 1E-3")     #corrente [A]
inst.write(":OUTP:STAT 1")  #accende il generatore


datax=[]        #tempo [s]
datay=[]	#Corrente [boh]


colonne=["V ","A_mean"]




print("SCAPPAA CHE STA MISURANDO VIA VIA\n")
for j in range(10):
    print("Rimasti: ", 10-j, "s\n")
    time.sleep(1)

tensioni = np.array( [5, 15, 25, 35, 45, 55, 65, 75, 85, 95] )

for tensione in tensioni:
	inst.write(("VOLT %d" % (float(tensione))))
	with open("noise_{0}V_360_20_0.5.csv".format(tensione),"w") as f:
    		f.write(",".join(colonne))
    		with nidaqmx.Task() as task:
        		task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)


       		#multi-triangolare  
        		for i in range(N_data):
                		a=0 
                		time.sleep(tempo/100)
                		try:
                    			a=float(inst.query('MEAS:VOLT?'))
                		except:
                    			inst.query('MEAS:VOLT?')
                    			a=float(inst.query('MEAS:VOLT?'))
                		data.append(a)
                		#f.write("%f \n" % a)                   
                
                		mes = task.read(number_of_samples_per_channel=samples)
                		mean = 0.
                		for samp in mes:
                    			mean += samp/samples
                		print(mean)
                		datax.append(i*waitT)
                		datay.append(mean)
                		f.write("\n{0}, {1}".format(a ,mean))
                		time.sleep(waitT)

                

	#print(data, "  ", type(data[0]))

	"""x = np.linspace(0,len(data)-1, N_data)
	print(x)
	plt.plot(x, data)
	plt.xlabel("Iteration")
	plt.ylabel("Tensione [V]")
	plt.title("Tensione erogata al piezoelettrico")
	plt.show()

	plt.plot(datax, datay)
	plt.xlabel("Tempo[s]")
	plt.ylabel("Corrente [boh]")
	plt.title("Segnale in uscita dal fotodiodo")
	plt.show()"""

#Reset sistema
inst.write("CURR 0")
inst.write("VOLT 0")
inst.write(":OUTP:STAT 0")
inst.write("*RST")
inst.write("*RST")

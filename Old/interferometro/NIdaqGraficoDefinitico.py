import matplotlib.pyplot as plt
import pyvisa                               #libreria generica per gestire strumenti
import nidaqmx
import time
import csv
import sys
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%Y-%B-%d_%H-%M-%S")

rm = pyvisa.ResourceManager()
ugo=rm.open_resource('GPIB0::18::INSTR')
ugo.write(":OUTP:STAT 1")                   #accendo lo strumento (ugo)
print(ugo.query(":OUTP:STAT?"))             #chiedo se è acceso o spento (la memoria fa cilecca)
azzero=int(0)
ugo.write("SOUR:VOLT %f" %azzero)           #imposto tensione a zero (a vuoto)
ugo.write(':SENS:FUNC "CURR"')              #corrente aggiunta come secondo valore da leggere
#ugo.write("SOUR:VOLT:ILIM 0.5")            #comando proibito:limite corrente (100uA)
tensione=float(input("Inserisci tensione iniziale: "))
passo=float(input("Inserisci intervallo fra le tensioni: "))
tmax=float(input("Inserisci tensione massima: "))
attesa=float(input("Inserisci intervallo temporale: "))
campioni=int(input("Numero di campioni per ogni misura: "))
npunti=int((tmax-tensione)/passo)
datax=[]
datay=[]	

plt.ion()
fig = plt.figure()

axes = plt.gca()
axes.set_autoscaley_on(True)
axes.set_autoscalex_on(True)
linee = axes.plot(datax, datay, 'ro-', label='ch0',linewidth=1)
plt.legend()
plt.title("Grafico")
plt.ylabel("Tensione uscita (V)")
plt.xlabel("Tensione ingresso (V)")

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
    f=open('test.csv',"w")    

    for t in range(npunti+1):
        ugo.write("SOUR:VOLT %f" % (tensione+t*passo))                   #imposto tensione
        time.sleep(attesa)
        outputS=ugo.query(':READ? "defbuffer1", DATE, SOUR, READ')
        print(outputS) #leggo e aggiorno schermo
        TensionePulita= float(outputS.split(",")[1])
        #tensione=float(input("Imposta nuova tensione: "))          #nuova tensione che immetto
        #ugo.write("SOUR:VOLT:ILIM <a>")

        mis = task.read(number_of_samples_per_channel=campioni)
        media = 0
        for camp in mis:
            media += camp/campioni
        print(media)
#       datax.append(t*attesa)
        datax.append(TensionePulita)
        datay.append(media)
        linee[0].set_xdata(datax)
        linee[0].set_ydata(datay)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        print("%s \n\n" %TensionePulita)
        f.write("%s " %(TensionePulita))
        f.write("%s " %media)
        f.write("\n")

    f.close()

#plt.show()

ugo.write("SOUR:VOLT %f" %azzero)                    #imposto tensione a 0
print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ')) #leggo e aggiorno schermo
time.sleep(30)                                       #tempo di scarico
print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ')) #leggo e aggiorno schermo
ugo.write(":OUTP:STAT 0")                   #spento lo strumento (ugo)
print(ugo.query(":OUTP:STAT?"))             #chiedo se è acceso o spento (la memoria fa cilecca)


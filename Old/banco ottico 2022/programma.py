#!python
#NOTA BENE: quando si usa una funzione di una libreria, la sintassi è: nomelibreria.nomefunzione(parametri se ci sono, separati da una virgola)
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
import pyvisa
import time
rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::18::INSTR')

#la libreria sys è una libreria di sistema; i termini sys.argv[] è la lista degli argomenti definiti all'avvio del programma sulla stessa riga di comando

if len(sys.argv)<2 :
        print("At least 2 argument needed - number of measurement and file output name")
        print("Optional arguments:")
        print("                    3) Number of  samples per channel")
        print("                    4) Waiting time")
        sys.exit(0)

#gli diamo 4 parametri: 1: nome del programma; 2: numero di valori del potenziale(loops); 3: nome del file in cui vengono salvati i dati; 4: numero di misure per ogni valore del potenziale; 5: tempo d'attesa.

nloops=int(sys.argv[1])
outname=sys.argv[2]
try: 
	samples=int(sys.argv[3])
except:
	samples=1
try: 
	waitT=float(sys.argv[4])
except:
	waitT=0.2

#il numero di valori di V e il nome del file vanno inseriti sempre, altrimenti da errore; gli altri due parametri sono facoltyativi e se non vengono inseriti prende un valore di default scritto sopra

#       ****** inizio comandi per grafico******	
datax=[]
datay=[]	

plt.ion()
fig = plt.figure()

axes = plt.gca()
axes.set_autoscaley_on(True)    #questa funzione inserisce nel grafico i valori dell'asse y (x la riga successiva); se si setta su false i valori non compaiono
axes.set_autoscalex_on(True)
linee = axes.plot(datax, datay, 'ro-', label='ch0',linewidth=1)
plt.legend()
plt.title("Plot")
plt.xlabel("voltage (V)")
plt.ylabel("intensity (arb. un.)")

#       ****** fine comandi per grafico******

f=open(outname,"w") #crei nuovo file, in sola scrittura 
task=nidaqmx.Task()
ch1=task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE) #questo serve per l'ADC (analog digital converter) e ai0 è il canale in cui entra il segnale analogico 
inst.write(":OUTP:STAT 1") 
for i in range(nloops):
        voltaggio=0.5+0.5*i #cambialo in 0,5
        inst.write(("SOUR:VOLT %f" % voltaggio ))
        time.sleep(0.5)
        data=inst.query(':READ? "defbuffer1", DATE, SOUR, READ')
        print(data)
        risultato=task.read(number_of_samples_per_channel=samples)
        media=0
        for item in risultato:
                media+=item/len(risultato)
        print(media)
        f.write("%s " % voltaggio )     #scrive sul file i dati 
        f.write("%s " % media)
        f.write("\n")   #questo equivale all'andare a capo
        datax.append(voltaggio)
        datay.append(media)
        linee[0].set_xdata(datax)
        linee[0].set_ydata(datay)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(waitT)

task.close()    #questo serve 
inst.write("SOUR:VOLT 0")       #questo resetta i parametri del generatore 
inst.write(":OUTP:STAT 0")
f.close()

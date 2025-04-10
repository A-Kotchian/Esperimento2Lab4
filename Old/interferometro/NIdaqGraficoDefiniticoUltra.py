import matplotlib.pyplot as plt
import pyvisa                   #libreria generica per gestire strumenti
import nidaqmx
import time
import csv
import sys
from datetime import datetime


if len(sys.argv)<2 :
    print("Serve almeno un argomento: intervallo in tensione fra le misure")
    print("Argomenti opzionali:")
    print("                    2) Tempo di attesa")
    print("                    3) Numero di campioni per ogni misura")
    print("                    4) Tensione iniziale")
    print("                    5) Tensione finale")
    print("Inserire '0' per attivare la modalità di prova manuale!")
    sys.exit(0)

adesso = datetime.now()

current_time = adesso.strftime("%Y-%B-%d_%H-%M-%S")

rm = pyvisa.ResourceManager()
ugo=rm.open_resource('GPIB0::18::INSTR')
ugo.write(":OUTP:STAT 1")                   #accendo lo strumento ("ugo")
print(ugo.query(":OUTP:STAT?"))             #chiedo subito se è acceso o spento come prova (la mia memoria fa cilecca)
azzero=int(0)                               #non ci pensare troppo: serve perché pyvisa ha esigenze strane sull'azzeramento della tensione, pare
ugo.write("SOUR:VOLT %f" %azzero)           #impos	to tensione a zero per precauzione (a vuoto)
ugo.write(':SENS:FUNC "CURR"')              #corrente aggiunta come secondo valore da leggere
#ugo.write("SOUR:VOLT:ILIM 0.5")            #comando "proibito", dà problemi: limite max corrente (forse 100µA si può mettere)


passo=float(sys.argv[1])         #assegna il valore dell'intervallo ("[0]" è da ignorare, c'è solo il nome del comando)
if (passo==0.0):    #succede solo se viene attivata la modalità manuale: solo per comodità ignora pure le prossime 3 righe
    print("Modalità manuale: inserisci un valore superiore a 150 per uscire")
    tensione=azzero             #inizializzo a 0V per sicurezza
    while(tensione<=150.0):     #questa soglia serve anche a proteggere il piezoelettrico
        ugo.write("SOUR:VOLT %f" %tensione)             #immetto tensione scelta
        print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ'))   #leggo valori generatore e aggiorno schermo
        tensione=float(input("Imposta nuova tensione: "))   #scelgo nuova tensione da immettere manualmente
    else:               # perché anche gli 'while' hanno un 'else', volendo
        sys.exit(0)     #esco dalla modalità manuale: ricomincio il programma
try: 
    attesa=float(sys.argv[2])    #assegna, se viene scelto, il tempo di attesa
except:
    attesa=1                     #(vedi sopra) altrimenti è assegnato a 1s
try:
    Ncampioni=int(sys.argv[3])  #assegna, se viene scelto, il numero di campionamenti per misura
except:
    Ncampioni=1                 #(vedi sopra) altrimenti è assegnato a 1
try: 
    tmin=float(sys.argv[4])     #assegna, se viene scelta, la tensione iniziale
except:
    tmin=20                     #(vedi sopra) altrimenti è assegnata a 20
try: 
    tmax=float(sys.argv[5])     #assegna, se viene scelta, la tensione iniziale
except:
    tmax=100                     #(vedi sopra) altrimenti è assegnata a 100

npunti=int((tmax-tmin)/passo)   #calcolo il numero di punti che ci servirà valutare (valore di fondo escluso), presi i nostri parametri (potrei anche scrivere direttamente "npunti=((tmax-tmin)//passo)", credo)
datax=[]                                    #inizializzo le liste (vuote) dei dati sugli assi
datay=[]	

plt.ion()                                   #tutta preparazione del grafico quaggiù
fig = plt.figure()

axes = plt.gca()
axes.set_autoscaley_on(True)                
axes.set_autoscalex_on(True)
linee = axes.plot(datax, datay, 'ro-', label='ch0',linewidth=1) #parametri vari linea: 'ro-' è stile/colore
plt.legend()                                                    #inserisce legenda (non che ci serva, ci basta un canale)
plt.title("Grafico")
plt.ylabel("Tensione (V)")
plt.xlabel("Tempo (s)")

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
    f=open('test.csv',"w")    

    for t in range(npunti+1):               #aggiungo un indice per includere il valore di fondo
        ugo.write("SOUR:VOLT %f" % (tmin+t*passo))                  #imposto tensione più alta passo passo
        print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ'))   #leggo valori generatore e aggiorno schermo

        lettura = task.read(number_of_samples_per_channel=Ncampioni)
        media = 0
        for campione in lettura:
            media += campione/Ncampioni
        print(media)
        datax.append(t*attesa)
        datay.append(media)
        linee[0].set_xdata(datax)
        linee[0].set_ydata(datay)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        TensionePulita=float(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ').split(",")[1]) #prendo valore generatore, separo ora, V ed I e prendo solo V ("[1]")
        print("%s \n\n" %TensionePulita)    #faccio un po' di spazio, altrimenti visivamente su schermo è ambiguo
        f.write("%s " %(TensionePulita))    #scrivo valore tensione generatore su calc
        f.write("%s " %media)               #scrivo tensione sensore sulla cella a fianco
        f.write("\n")                       #mando a capo
        time.sleep(attesa)      

    f.close()

ugo.write("SOUR:VOLT %f" %azzero)                    #imposto tensione a 0 con il solito metodo ridondante
time.sleep(10)                                       #tempo di scarico per sicurezza
print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ')) #leggo e aggiorno schermo
ugo.write(":OUTP:STAT 0")                   #spengo lo strumento (ugo)
print(ugo.query(":OUTP:STAT?"))             #chiedo se è acceso o spento (la mia memoria fa ancora cilecca)

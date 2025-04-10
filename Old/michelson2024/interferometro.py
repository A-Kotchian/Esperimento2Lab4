#!python

import pyvisa
import time
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
from datetime import datetime
import pandas as pd
import numpy as np

time.sleep(10)
now = datetime.now()

current_time = now.strftime("%Y-%B-%d_%H-%M-%S")

rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::18::INSTR')

inst.write(':SENS:FUNC "CURR"')
inst.write(":OUTP:STAT 1")


if len(sys.argv)<2 :
    print("Scivi almeno un parametro (passo del volt)")
    print("Parametri opzionali:")
    print("                    2) Numero di campioni per canale")
    print("                    3) Tempo che aspetto")
    print("                    4) Numero prova")
    print("                    5) guadagno")
    sys.exit(0)

passo =float(sys.argv[1])
try: 
    nCampioni =int(sys.argv[2])
except:
    nCampioni=1
try: 
    tAttesa =float(sys.argv[3])
except:
    tAttesa =1

nElementiArray = int(125/passo)
print(nElementiArray)

voltaggio = np.zeros(nElementiArray)
for i in range(nElementiArray):
    voltaggio[i] = i*passo
print(voltaggio)

mediaArray =[]# np.zeros(nElementiArray)
voltaggioEffettivo = [] #np.zeros(nElementiArray)
mediaErr = np.empty(0)
numeroProva = str(sys.argv[4])
guadagno = str(sys.argv[5])

plt.ion()
fig = plt.figure()
axes = plt.gca()
axes.set_autoscaley_on(True)
axes.set_autoscalex_on(True)
linee = axes.plot(voltaggioEffettivo, mediaArray, 'ro-', label='ch0',linewidth=1)
    
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)

    for i in range(len(voltaggio)):
        inst.write(("SOUR:VOLT %f" % (voltaggio[i])))
        time.sleep(tAttesa)
        dataAlimentatore=inst.query(':READ? "defbuffer1", DATE, SOUR, READ')
        print(dataAlimentatore)
        mes = task.read(number_of_samples_per_channel=nCampioni)
        mean = 0.
        mediaErr = np.append(mediaErr, np.std(mes))
        for samp in mes:
            mean += samp/nCampioni
        print('media= ', mean)
        #mediaArray[i] = mean
        mediaArray.append(mean)
        x = dataAlimentatore.split(",")
        voltaggioEffettivo.append(float(x[1]))
        #voltaggioEffettivo[i] = x[1]
        linee[0].set_xdata(voltaggioEffettivo)
        linee[0].set_ydata(mediaArray)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.savefig('grafico'+ str(passo)+ 'Prova' + numeroProva + 'Guadagno' + guadagno + '.png')


        

inst.write("SOUR:VOLT 0")
time.sleep(10)
inst.query(':READ? "defbuffer1", DATE, SOUR, READ')
inst.write(":OUTP:STAT 0")


tabella = pd.DataFrame()
tabella['voltaggioEffettivo'] = voltaggioEffettivo
tabella['media'] = mediaArray
tabella['erroreMedia'] = mediaErr
print(tabella)
nome = 'michelsonPasso'+ str(passo)+ 'Prova' + numeroProva + 'Guadagno' + guadagno + '.csv'

tabella.to_csv(nome, index=False)



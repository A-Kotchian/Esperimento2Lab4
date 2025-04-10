
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
from datetime import datetime
import pyvisa
import numpy as np

# Parsing degli argomenti della linea di comando
if len(sys.argv) < 2:
    print("Necessario almeno 1 argomento: numero di misurazioni (nloops)")
    print("Argomenti opzionali:")
    print("  2) Numero di campioni per canale (samples)")
    print("  3) Tempo di attesa tra le misurazioni (waitT)")
    sys.exit(1)

nloops = int(sys.argv[1])
try:
    samples = int(sys.argv[2])
except:
    samples = 1
try:
    waitT = float(sys.argv[3])
except:
    waitT = 1

# Inizializzazione pyvisa
rm = pyvisa.ResourceManager()
try:
    inst = rm.open_resource('GPIB0::9::INSTR')  # Sostituisci con l'indirizzo corretto
    print("Connessione al generatore di tensione stabilita.")
except pyvisa.VisaIOError as e:
    print(f"Errore di connessione al generatore: {e}")
    sys.exit(1)

# Funzione per impostare la tensione
def imposta_tensione(tensione):
    inst.write(f"VOLT {tensione}")
    stato_output = int(inst.query("OUTP:STAT?"))
    if stato_output == 0 and tensione > 0:
        inst.write("OUTP:STAT 1")
        print("Output acceso.")
    elif stato_output == 1 and tensione == 0:
        inst.write("OUTP:STAT 0")
        print("Output spento.")
    tensione_erogata = float(inst.query('MEAS:VOLT?'))
    print(f"Tensione impostata: {tensione} V, Tensione misurata: {tensione_erogata} V")

datax = []
datay = []

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(datax, datay, 'ro-', label='ch0', linewidth=1)
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Tensione (V)")
ax.set_title("Misurazioni con variazione di tensione")
ax.legend()
ax.grid(True)

with nidaqmx.Task() as task:
    try:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)  # Sostituisci con il tuo canale DAQ
        for i in range(nloops):
            # Calcola la tensione da impostare (lineare tra 0V e 100V)
            tensione_da_impostare = (100.0 * i) / (nloops - 1) if nloops > 1 else 0.0
            if tensione_da_impostare > 100:
                tensione_da_impostare = 100

            # Imposta la tensione sul generatore
            imposta_tensione(tensione_da_impostare)

            # Attendi un po' dopo aver impostato la tensione
            time.sleep(0.5)  # Regola questo valore se necessario

            # Misura la tensione con il DAQ
            mes = task.read(number_of_samples_per_channel=samples)
            mean = np.mean(mes)
            print(f"Misurazione {i+1}: Tensione impostata = {tensione_da_impostare:.2f} V, Tensione misurata = {mean:.2f} V")

            current_time_sec = time.time()
            datax.append(current_time_sec)
            datay.append(mean)

            line.set_data(datax, datay)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()

            time.sleep(waitT)

    except nidaqmx.DaqmxError as e:
        print(f"Errore DAQmx: {e}")
    except Exception as e:
        print(f"Errore generico: {e}")

    finally:
        # Riporta la tensione a 0 e resetta lo strumento
        imposta_tensione(0)
        inst.write("*RST")
        print("Tensione riportata a 0 e strumento resettato.")

        if 'inst' in locals() and inst is not None:
            inst.close()
            print("Connessione allo strumento chiusa.")
        rm.close()
        print("Resource Manager chiuso.")

plt.ioff()
plt.show()
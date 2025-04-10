import pyvisa                               #libreria generica per gestire srumenti
import time

rm = pyvisa.ResourceManager()
ugo=rm.open_resource('GPIB0::18::INSTR')
ugo.write(":OUTP:STAT 1")                   #accendo lo strumento (ugo)
print(ugo.query(":OUTP:STAT?"))             #chiedo se è acceso o spento (la memoria fa cilecca)
ugo.write("SOUR:VOLT 0")                   #imposto tensione
ugo.write(':SENS:FUNC "CURR"')              #corrente aggiunta come secondo valore da leggere
#ugo.write("SOUR:VOLT:ILIM 0.5")            #comando proibito:limite corrente (100uA)
tensione=float(input("Inserisci tensione iniziale: "))
passo=float(input("Inserisci intervallo fra le tensioni: "))
tmax=float(input("Inserisci tensione massima: "))
attesa=float(input("Inserisci intervallo temporale: "))
npunti=int((tmax-tensione)/passo)
for t in range(npunti+1):
    ugo.write("SOUR:VOLT %f" % (tensione+t*passo))                   #imposto tensione
    print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ')) #leggo e aggiorno schermo
    #tensione=float(input("Imposta nuova tensione: "))          #nuova tensione che immetto
    time.sleep(attesa)
    #ugo.write("SOUR:VOLT:ILIM <a>")
azzero=int(0)
ugo.write("SOUR:VOLT %f" %azzero)                    #imposto tensione a 0
time.sleep(10)              #tempo di scarico
print(ugo.query(':READ? "defbuffer1", DATE, SOUR, READ')) #leggo e aggiorno schermo
ugo.write(":OUTP:STAT 0")                   #spento lo strumento (ugo)
print(ugo.query(":OUTP:STAT?"))             #chiedo se è acceso o spento (la memoria fa cilecca)

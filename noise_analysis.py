import numpy as np
import matplotlib.pyplot as plt
import math
import scipy as sc
from scipy import constants, fft
import pandas as pd



#lettura csv e creazione array

tensione = input("Select the tension: ")

data = pd.read_csv('noise_{0}V_360_20_0.5.csv'.format(tensione))

v = data['V ']

print(len(v))
tempo = np.arange(0, 180, 0.5)

a = data['A_mean']

a = a.to_numpy()
samplerate = 1/(tempo[1]-tempo[0])

plt.figure(figsize = (18,9))
plt.title("Tensione di alimentazione in funzione del tempo")
plt.plot(tempo,v)
plt.xlabel("t [s]")
plt.ylabel("V [V]")
plt.show()

plt.figure(figsize = (20,10))
plt.title("Ampiezza media in funzione del tempo")
plt.plot(tempo,a)
plt.xlabel("t [s]")
plt.ylabel("A_mean [u.a.]")
plt.show()

"""fft_1  = fft.rfft(a[:100])
fftfreqs_1  = fft.rfftfreq(len(a[:100]), 1.0/samplerate) 
potenze_1 = fft_1.real ** 2 + fft_1.imag ** 2

print(fftfreqs_1)
#plt.plot(fftfreqs_1[1:len(fft_1)], potenze_1[1:len(fft_1)] , color='lightsteelblue')
#plt.show()


data_sig = pd.read_csv('rampa_200_10_0.5.csv')

v = data_sig['V']




a_sig = data_sig['A_mean']

a_sig = a_sig.to_numpy()
v = v.to_numpy()

numeri = np.linspace(0,199,200)


mask = numeri %2 == 0


a_sig = a_sig[mask]
v = v[mask]


samplerate = 1/(v[1]-v[0])


#plt.plot(v,a_sig)
#plt.show()



fft_1_sig  = fft.rfft(a_sig)
fftfreqs_1_sig  = fft.rfftfreq(len(a_sig), 1.0/samplerate) 
potenze_1_sig = fft_1_sig.real ** 2 + fft_1_sig.imag ** 2

plt.plot(fftfreqs_1_sig[1:len(fft_1_sig)], potenze_1_sig[1:len(fft_1_sig)] , color='magenta')
plt.show()
print(fftfreqs_1_sig)


max_ampl = np.max(potenze_1_sig[1:len(fft_1_sig)])

print(max_ampl)
print(potenze_1_sig[1:len(fft_1_sig)])
mask_1 = potenze_1_sig[1:len(fft_1_sig)]== max_ampl

print(mask_1)
freq_1 = fftfreqs_1_sig[1:len(fft_1_sig)][mask_1]

max_freq = np.max(freq_1)

print(max_freq)

plt.plot(v, 0.48-0.03*np.cos(v*2*np.pi*max_freq) , color='lightsteelblue')
plt.plot(v,a_sig)
plt.show()"""
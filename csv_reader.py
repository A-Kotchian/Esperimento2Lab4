import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import constants
from scipy.fft import fft, fftfreq, rfft, rfftfreq, ifft

file_path = "rumore.csv"
data = pd.read_csv(file_path)
V=data['A_mean'].values

V=V[1:]
# Plot the values
t=np.linspace(0,len(V)/2,len(V))
# plt.plot(t,V)
# plt.title("Rumore")
# plt.xlabel("Tempo")
# plt.ylabel("V") 
# plt.show()


samplerate = 1024
fft_V = fft(V)
n = len(fft_V)
freq_dx = fftfreq(n,1/samplerate)
module_dx = pow(np.abs(fft(V)),2) 


plt.plot(freq_dx[1:len(module_dx)], module_dx[1:len(module_dx)], "g--")
plt.title("Fourier Rumore")
plt.xlabel("Frequenza")
plt.ylabel("Magnitudo")
plt.show()

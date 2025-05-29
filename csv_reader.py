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

print(len(V))

V_dx = V[50:(int(len(V)/2))]
V_sx = V[(int(len(V)/2+30)):]

V_dx_mean = np.sum(V_dx)/len(V_dx)
V_sx_mean = np.sum(V_sx)/len(V_sx)

scarti_dx = V_dx - V_dx_mean
scarti_sx = V_sx - V_sx_mean

mean_s_dx = np.sum(np.abs(scarti_dx))/len(scarti_dx)
mean_s_sx = np.sum(np.abs(scarti_sx))/len(scarti_sx)
print(mean_s_dx, mean_s_sx)

plt.hist(V, 200, [0.465, 0.51])
plt.show()


plt.hist(scarti_dx, 15, [-0.025,0.025])
plt.show()

plt.hist(scarti_sx, 15, [-0.025,0.025])
plt.show()

# Plot the values
t=np.linspace(0,len(V),len(V))
plt.plot(t,V, color = 'teal')
plt.hlines(V_dx_mean, t[0], t[len(t)-1])
plt.hlines(V_sx_mean, t[0], t[len(t)-1])
plt.vlines(int(len(V)/2-10), np.min(V), np.max(V))
plt.vlines(int(len(V)/2+30), np.min(V), np.max(V))
plt.title("Rumore")
plt.xlabel("Tempo [s]")
plt.ylabel("Tensione [V]") 
plt.show()


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


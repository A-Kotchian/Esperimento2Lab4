import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

L_off = pd.read_csv("L_off.csv")
R_off = pd.read_csv("R_off.csv")
C_off = pd.read_csv("C_off.csv")
RC_off = pd.read_csv("RC_off.csv")
LC_off = pd.read_csv("LC_off.csv")
C_on = pd.read_csv("C_on.csv")


L_off_V = L_off['A_mean'].values[1:]
R_off_V = R_off['A_mean'].values[1:]
C_off_V = C_off['A_mean'].values[1:]
RC_off_V = RC_off['A_mean'].values[1:]
LC_off_V = LC_off['A_mean'].values[1:]
C_on_V = C_on['A_mean'].values[1:]

t=np.linspace(0,len(L_off_V)/2,len(L_off_V))

fig, axs = plt.subplots(2,3, sharey = True)
axs[0,0].plot(t, L_off_V, color = "#238155", linewidth = 2)
axs[0,0].set_title('L off')
axs[0,1].plot(t, R_off_V, color = "#238155", linewidth = 2)
axs[0,1].set_title('R off')
axs[0,2].plot(t, C_off_V, color = "#238155", linewidth = 2)
axs[0,2].set_title('C off')
axs[1,0].plot(t, RC_off_V, color = "#238155", linewidth = 2)
axs[1,0].set_title('L on')
axs[1,1].plot(t, LC_off_V, color = "#238155", linewidth = 2)
axs[1,1].set_title('R on')
axs[1,2].plot(t, C_on_V, color = "#238155", linewidth = 2)
axs[1,2].set_title('C on')
axs[1,0].set_xlabel('Tempo [s]')
axs[1,1].set_xlabel('Tempo [s]')
axs[1,1].set_xlabel('Tempo [s]')
axs[0,0].set_ylabel('Voltaggio [V]')
axs[1,0].set_ylabel('Voltaggio [V]')
plt.show()

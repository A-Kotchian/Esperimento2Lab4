import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as st

def funzione(x, A, w, phi, z):
    return A * np.sin(x*w + phi) + z

def chi2(oss, att, ossErr):
    chiArr = np.zeros(len(oss))
    return ((att-oss)/ ossErr)**2


    

    
        

nomeFile = 'fotodiodoProva7Guadagno60.csv'
dati = pd.read_csv(nomeFile)
vEff = dati['voltaggioEffettivo']
mediaArr = dati['media']
mediaErr = dati['erroreMedia']

mediaGiusto = np.empty([])
for i in range(len(mediaArr)):
    mediaGiusto = np.append(mediaGiusto, mediaArr[i])
    '''if mediaArr[i]< 4.5:
        mediaGiusto = np.append(mediaGiusto, mediaArr[i])'''

mediaGiusto = mediaGiusto[2:]
plt.plot(mediaGiusto, '-o')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 3')
plt.show()

devStd = np.std(mediaGiusto)
print('deviazione standard = ', devStd)

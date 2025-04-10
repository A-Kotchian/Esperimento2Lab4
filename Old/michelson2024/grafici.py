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


    

    
        

nomeFile = 'michelsonPasso0.2Prova5Guadagno60.csv'
dati = pd.read_csv(nomeFile)
vEff = dati['voltaggioEffettivo']
mediaArr = dati['media']
mediaErr = dati['erroreMedia']

offset= 0.001
noise = 0.0008

vEffErr = np.zeros(len(vEff))
for i in range(len(vEffErr)):
    if i<20:
        vEffErr[i] = vEff[i] * 0.00015 + 0.0002
    elif i < 200:
        vEffErr[i] = vEff[i] * 0.0002 + 0.0003
    else:
        vEffErr[i] = vEff[i] * 0.00015 + 0.0024
        
    

mediaErrTot = np.sqrt(mediaErr**2 + offset**2 + noise**2+vEffErr**2)


arrayVEff = np.array([vEff[100:125], vEff[125:150], vEff[150:175], vEff[175:200], vEff[200:225], vEff[225:250], vEff[250:275], vEff[275:300], vEff[300:325], vEff[325:350], vEff[350:375]])
arrayMedia = np.array([mediaArr[100:125], mediaArr[125:150], mediaArr[150:175], mediaArr[175:200], mediaArr[200:225], mediaArr[225:250], mediaArr[250:275], mediaArr[275:300], mediaArr[300:325], mediaArr[325:350], mediaArr[350:375]])
arrayMediaErr = np.array([mediaErr[100:125], mediaErr[125:150], mediaErr[150:175], mediaErr[175:200], mediaErr[200:225], mediaErr[225:250], mediaErr[250:275], mediaErr[275:300], mediaErr[300:325], mediaErr[325:350], mediaErr[350:375]])

'''
vEff2 = vEff[250:375]
mediaArr2 = mediaArr[250:375]
mediaErr2 = mediaErr[250:375]
'''

vEff2 = vEff[100:375]
mediaArr2 = mediaArr[100:375]
mediaErr2 = mediaErr[100:375]

plt.plot(vEff, mediaArr, '-o')
plt.plot(arrayVEff[0], arrayMedia[0], '-o')
plt.plot(arrayVEff[1], arrayMedia[1], '-o')
plt.plot(arrayVEff[2], arrayMedia[2], '-o')
plt.plot(arrayVEff[3], arrayMedia[3], '-o')
plt.plot(arrayVEff[4], arrayMedia[4], '-o')
plt.plot(arrayVEff[5], arrayMedia[5], '-o')
plt.plot(arrayVEff[6], arrayMedia[6], '-o')
plt.plot(arrayVEff[7], arrayMedia[7], '-o')
plt.plot(arrayVEff[8], arrayMedia[8], '-o')
plt.plot(arrayVEff[9], arrayMedia[9], '-o')
plt.plot(arrayVEff[10], arrayMedia[10], '-o')
plt.title('Intervallo dati selezionato')
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.show()



'''    
plt.plot(vEff, mediaArr, '-o')
plt.plot(vEff2, mediaArr2, '-o')
plt.title('Intervallo dati selezionato')
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.show()
'''


pstart = np.array([-1.742841123322082, 1.2931801726049132,  -4.618687242338679, 2.6429589769737354])
#pstart = np.array([4, 1.2,  -4.618687242338679, 2.6429589769737354])

arrayPar = np.ones([11,4])
arrayParErr = np.ones([11,4])
arrayMediaFit = np.ones([11, len(arrayVEff[0])])
arrayChi = np.ones([11])

for i in range(len(arrayVEff)):
    parametri, cov = optimize.curve_fit(funzione, arrayVEff[i], arrayMedia[i], p0=[pstart], sigma = arrayMediaErr[i])
    errParametri = np.sqrt(np.diag(cov))
    arrayPar[i] = parametri
    arrayParErr[i] = errParametri
    arrayMediaFit[i] = funzione(arrayVEff[i], parametri[0], parametri[1], parametri[2], parametri[3])
    chiArr = chi2(arrayMedia[i], arrayMediaFit[i], arrayMediaErr[i])
    chi = np.sum(chiArr)/(len(arrayMedia[i]) -4)
    arrayChi[i] = chi



plt.errorbar(vEff2, mediaArr2, yerr= mediaErr2, fmt ='-o', alpha = 0.5, label = 'dati', color = 'black')

for i in range(len(arrayVEff)):
    plt.plot(arrayVEff[i], arrayMediaFit[i], '-o', label= 'fit', alpha = 0.8)
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.title('Confronto dati e fit')
plt.legend()
plt.grid()
plt.show()

A = np.ones([11])
AErr = np.ones([11])
w = np.ones([11])
wErr = np.ones([11])
phi = np.ones([11])
phiErr = np.ones([11])
z = np.ones([11])
zErr = np.ones([11])

for i in range(11):
    A[i] = arrayPar[i][0]
    AErr[i] = arrayParErr[i][0]
    w[i] = arrayPar[i][1]
    wErr[i] = arrayParErr[i][1]
    phi[i] = arrayPar[i][2]
    phiErr[i] = arrayParErr[i][2]
    z[i] = arrayPar[i][3]
    zErr[i] = arrayParErr[i][3]
   

tabella = pd.DataFrame()
tabella.index = ['20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65', '65-70', '70-75']
tabella['A'] = A
tabella['AErr'] = AErr
tabella['w'] = w
tabella['wErr'] = wErr
tabella['phi'] = phi
tabella['phiErr'] = phiErr
tabella['z'] = z
tabella['zErr'] = zErr
tabella['chi2'] = arrayChi
print(tabella)
tabella.to_csv('parametriFit.csv', index=True)

x = ['20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65', '65-70', '70-75']
plt.errorbar(x, w, yerr= wErr)
plt.show()

'''  
parametri, cov = optimize.curve_fit(funzione, vEff2, mediaArr2, p0=[pstart], sigma = mediaErr2)
errParametri = np.sqrt(np.diag(cov))
print('parametri ottimali trovati: \n', 'A: ', parametri[0],' ± ', errParametri[0], '\n w: ', parametri[1],' ± ', errParametri[1], '\n phi: ',parametri[2],' ± ', errParametri[2], '\n z: ',parametri[3],' ± ', errParametri[3])



mediaFit = funzione(vEff2, parametri[0], parametri[1], parametri[2], parametri[3])
#plt.plot(vEff2, mediaArr2, '-o')
plt.plot(vEff2, mediaFit, '-o', label= 'fit', alpha = 0.8)

plt.errorbar(vEff2, mediaArr2, yerr= mediaErr2, fmt ='-o', alpha = 0.8, label = 'dati')
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.title('Confronto dati e fit')
plt.legend()
plt.grid()
plt.show()


chiArr = chi2(mediaArr2, mediaFit, mediaErr2)
chi = np.sum(chiArr)/(len(mediaArr2) -4)
print('chi2 = ', chi)


'''

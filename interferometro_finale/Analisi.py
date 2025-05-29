import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import optimize
from scipy import constants
import scipy.odr as odr


#Dati e variabili
file_path = "L_off.csv"
data = pd.read_csv(file_path)

V_o=data['A_mean'].values
V_o_err=data['A_err'].values
V_i=data['V'].values


V_out=V_o[1:]
V_in=V_i[1:]
V_out_err=V_o_err[1:]


t=np.linspace(0,len(V_out)/2,len(V_out))

# mask = [i%2 == 0 for i in range(0,len(V_in))]
# V_in = V_in[mask]

plt.plot(t, V_in, color = "indianred", linewidth = 2)
plt.title('Tensione erogata ai piezoelettrici')
plt.xlabel("Tempo [s]")
plt.ylabel("Tensione [V]")
plt.show()

V_in_salita=V_in[:int(len(V_in)/2)]
V_in_salita_err=np.full(len(V_in_salita),0.01)

V_in_discesa=V_in[int(len(V_in)/2):]
V_in_discesa_err=np.full(len(V_in_discesa),0.01)

V_out_salita=V_out[:int(len(V_out)/2)]
V_out_salita_err=V_out_err[:int(len(V_out)/2)]
#V_out_salita_err=np.full(len(V_out_salita),0.001)

V_out_discesa=V_out[int(len(V_out)/2):]
V_out_discesa_err=V_out_err[int(len(V_out)/2):]




# Plot salita
plt.errorbar(V_in_salita,V_out_salita,xerr=V_in_salita_err,yerr=V_out_salita_err,color="mediumseagreen")
plt.title("Segnale in uscita dal fotodiodo, rampa in salita")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.legend(loc="best")
plt.show()


# Plot discesa
plt.errorbar(V_in_discesa,V_out_discesa,xerr=V_in_discesa_err,yerr=V_out_discesa_err,color="mediumseagreen")
plt.title("Segnale in uscita dal fotodiodo, rampa in discesa")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.show()


def test_func(p,x):
    a,b,c,d=p
    """ 
    f(x) = c*sin(a*x+b)+d

    """
    return c*np.sin(a*x+b)+d


# Fit in salita
pstart = [ 0.68669015, -2.00904276, -1.0864331,  1.73886837]

fit_sim = odr.Model(test_func)
data_sim = odr.RealData( V_in_salita, V_out_salita, sx=V_in_salita_err, sy=V_out_salita_err)
odrr_sim   = odr.ODR(data_sim, fit_sim,beta0=pstart)
fit_out_sim   = odrr_sim.run()
fit_out_sim.pprint()



xtest = np.linspace(10, 100,400)
ytest = test_func(fit_out_sim.beta, xtest)
plt.plot(xtest,ytest , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_salita,V_out_salita,xerr=V_in_salita_err,yerr=V_out_salita_err, fmt=".--",label="Dati",linewidth= 1,color = "#786394")
plt.legend()
plt.title("Fit rampa in salita")
plt.xlabel("Tensione di alimentazione [V]")
plt.xlim(0,110)
plt.ylim(0,3.5)
plt.ylabel("Tensione in uscita [V] ") 
plt.legend(loc="upper right")
plt.show()

# Fit in discesa
pstart_2 = [0.6, 0.1, 1.2,  1.9]
fit_sim= odr.Model(test_func)
data_sim_2 = odr.RealData( V_in_discesa, V_out_discesa, sx=V_in_discesa_err, sy=V_out_discesa_err)
odrr_sim_2  = odr.ODR(data_sim_2, fit_sim, beta0=pstart_2)
fit_out_sim_2  = odrr_sim_2.run()
fit_out_sim_2.pprint()
xtest_2 = np.linspace(10, 100,400)
ytest_2 = test_func(fit_out_sim_2.beta, xtest_2)
plt.plot(xtest_2,ytest_2 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_discesa,V_out_discesa,xerr=V_in_discesa_err,yerr=V_out_discesa_err, fmt=".--",label="Dati",linewidth= 1,color = "#7D5FA5")
plt.title("Fit rampa in discesa")
plt.xlabel("Tensione di alimentazione [V]")
plt.xlim(0,110)
plt.ylim(0,3.5)
plt.ylabel("Tensione in uscita [V] ") 
plt.legend(loc="upper right")
plt.show()


#Fit a pezzi 

#salita
V_in_salita_1=V_in_salita[:int(len(V_in_salita)/3)]
V_in_salita_err_1=V_in_salita_err[:int(len(V_in_salita)/3)]

V_in_salita_2=V_in_salita[int(len(V_in_salita)/3):2*int(len(V_in_salita)/3)]
V_in_salita_err_2=V_in_salita_err[int(len(V_in_salita)/3):2*int(len(V_in_salita)/3)]

V_in_salita_3=V_in_salita[2*int(len(V_in_salita)/3):]
V_in_salita_err_3=V_in_salita_err[2*int(len(V_in_salita)/3):]


V_out_salita_1=V_out_salita[:int(len(V_out_salita)/3)]
V_out_salita_err_1=V_out_salita_err[:int(len(V_out_salita)/3)]

V_out_salita_2=V_out_salita[int(len(V_out_salita)/3):2*int(len(V_in_salita)/3)]
V_out_salita_err_2=V_out_salita_err[int(len(V_out_salita)/3):2*int(len(V_in_salita)/3)]

V_out_salita_3=V_out_salita[2*int(len(V_out_salita)/3):]
V_out_salita_err_3=V_out_salita_err[2*int(len(V_out_salita)/3):]

#discesa
V_in_discesa_1=V_in_discesa[:int(len(V_in_discesa)/3)]
V_in_discesa_err_1=V_in_discesa_err[:int(len(V_in_discesa)/3)]

V_in_discesa_2=V_in_discesa[int(len(V_in_discesa)/3):2*int(len(V_in_discesa)/3)]
V_in_discesa_err_2=V_in_discesa_err[int(len(V_in_discesa)/3):2*int(len(V_in_discesa)/3)]

V_in_discesa_3=V_in_discesa[2*int(len(V_in_discesa)/3):]
V_in_discesa_err_3=V_in_discesa_err[2*int(len(V_in_discesa)/3):]


V_out_discesa_1=V_out_discesa[:int(len(V_out_discesa)/3)]
V_out_discesa_err_1=V_out_discesa_err[:int(len(V_out_discesa)/3)]

V_out_discesa_2=V_out_discesa[int(len(V_out_discesa)/3):2*int(len(V_in_discesa)/3)]
V_out_discesa_err_2=V_out_discesa_err[int(len(V_out_discesa)/3):2*int(len(V_in_discesa)/3)]

V_out_discesa_3=V_out_discesa[2*int(len(V_out_discesa)/3):]
V_out_discesa_err_3=V_out_discesa_err[2*int(len(V_out_discesa)/3):]

"""
#Salita, pezzo 1
pstart_3 = [ 0.64568908, -0.93407884, -1.10235022,  1.75455202]
fit_sim= odr.Model(test_func)
data_sim_3 = odr.RealData( V_in_salita_1, V_out_salita_1, sx=V_in_salita_err_1, sy=V_out_salita_err_1)
odrr_sim_3  = odr.ODR(data_sim_3, fit_sim, beta0=pstart_3)
fit_out_sim_3  = odrr_sim_3.run()
fit_out_sim_3.pprint()
xtest_3 = np.linspace(10, 41,400)
ytest_3= test_func(fit_out_sim_3.beta, xtest_3)
plt.plot(xtest_3,ytest_3 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_salita_1,V_out_salita_1,xerr=V_in_salita_err_1,yerr=V_out_salita_err_1,fmt=".--",label="Dati",linewidth= 1,color = "#786394")
plt.legend()
plt.title("Fit rampa in salita, prima parte")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 

plt.show()

#Salita, pezzo 2
pstart_4 = [0.669, -0.93407884, -1.5,  1.75455202]
fit_sim= odr.Model(test_func)
data_sim_4 = odr.RealData( V_in_salita_2, V_out_salita_2, sx=V_in_salita_err_2, sy=V_out_salita_err_2)
odrr_sim_4  = odr.ODR(data_sim_4, fit_sim, beta0=pstart_4)
fit_out_sim_4  = odrr_sim_4.run()
fit_out_sim_4.pprint()
xtest_4 = np.linspace(41, 70,400)
ytest_4= test_func(fit_out_sim_4.beta, xtest_4)
plt.plot(xtest_4,ytest_4 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_salita_2,V_out_salita_2,xerr=V_in_salita_err_2,yerr=V_out_salita_err_2,fmt=".--",label="Dati",linewidth= 1,color = "#786394")
plt.legend()
plt.title("Fit rampa in salita, seconda parte")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.show()


#Salita, pezzo 3
pstart_5 = [0.65317303, -5.35783906, -1.03548394,  1.7980214]
fit_sim= odr.Model(test_func)
data_sim_5 = odr.RealData( V_in_salita_3, V_out_salita_3, sx=V_in_salita_err_3, sy=V_out_salita_err_3)
odrr_sim_5  = odr.ODR(data_sim_5, fit_sim, beta0=pstart_5)
fit_out_sim_5  = odrr_sim_5.run()
fit_out_sim_5.pprint()
xtest_5 = np.linspace(70, 100,400)
ytest_5= test_func(fit_out_sim_5.beta, xtest_5)
plt.plot(xtest_5,ytest_5 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_salita_3,V_out_salita_3,xerr=V_in_salita_err_3,yerr=V_out_salita_err_3,fmt=".--",label="Dati",linewidth= 1,color = "#786394")
plt.legend()
plt.title("Fit rampa in salita, terza parte")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.show()

"""


#Discesa, pezzo 1
pstart_6 = [0.485, -5.35783906, -1.03548394,  1.7980214]
fit_sim= odr.Model(test_func)
data_sim_6 = odr.RealData( V_in_discesa_1, V_out_discesa_1, sx=V_in_discesa_err_1, sy=V_out_discesa_err_1)
odrr_sim_6  = odr.ODR(data_sim_6, fit_sim, beta0=pstart_6)
fit_out_sim_6  = odrr_sim_6.run()
fit_out_sim_6.pprint()
xtest_6 = np.linspace(70, 100,400)
ytest_6= test_func(fit_out_sim_6.beta, xtest_6)
plt.plot(xtest_6,ytest_6 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_discesa_1,V_out_discesa_1,xerr=V_in_discesa_err_1,yerr=V_out_discesa_err_1, fmt=".--",label="Dati",linewidth= 1,color = "#786394")
plt.legend()
plt.title("Fit rampa in discesa, prima parte")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.show()

#Discesa, pezzo 2
pstart_7 = [0.65, -5.35783906, -1.03548394,  1.7980214]
fit_sim= odr.Model(test_func)
data_sim_7 = odr.RealData( V_in_discesa_2, V_out_discesa_2, sx=V_in_discesa_err_2, sy=V_out_discesa_err_2)
odrr_sim_7  = odr.ODR(data_sim_7, fit_sim, beta0=pstart_7)
fit_out_sim_7  = odrr_sim_7.run()
fit_out_sim_7.pprint()
xtest_7 = np.linspace(41, 70,400)
ytest_7= test_func(fit_out_sim_7.beta, xtest_7)
plt.plot(xtest_7,ytest_7 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_discesa_2,V_out_discesa_2,xerr=V_in_discesa_err_2,yerr=V_out_discesa_err_2, fmt=".--",label="Dati",linewidth= 1,color = "#786394")
plt.legend()
plt.title("Fit rampa in discesa, seconda parte")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.show()

#Discesa, pezzo 3
pstart_8 = [0.76106066, -9.78349498, -1.12666546,  1.83672274]
fit_sim= odr.Model(test_func)
data_sim_8 = odr.RealData( V_in_discesa_3, V_out_discesa_3, sx=V_in_discesa_err_3, sy=V_out_discesa_err_3)
odrr_sim_8  = odr.ODR(data_sim_8, fit_sim, beta0=pstart_8)
fit_out_sim_8  = odrr_sim_8.run()
fit_out_sim_8.pprint()
xtest_8 = np.linspace(10, 41,400)
ytest_8= test_func(fit_out_sim_8.beta, xtest_8)
plt.plot(xtest_8,ytest_8 , label ="Fit", color="#6acc8c",linewidth= 1.6)
plt.errorbar(V_in_discesa_3,V_out_discesa_3,xerr=V_in_discesa_err_3,yerr=V_out_discesa_err_3, fmt=".--",label="Dati",linewidth= 1,color = "#786394")

plt.legend()
plt.title("Fit rampa in discesa, terza parte")
plt.xlabel("Tensione di alimentazione [V]")
plt.ylabel("Tensione in uscita [V] ") 
plt.show()


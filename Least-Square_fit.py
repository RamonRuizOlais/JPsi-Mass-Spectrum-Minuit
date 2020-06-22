import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit 

def model(x, norm, mean, sigma, c0, c1): #Definimos la función para el ajuste de datos
 linear = c0 + c1*(x-xmin)/(xmax-xmin)
 gaussian = norm*xbinwidth/(2.*np.pi)**0.5/sigma * \
 np.exp(-0.5*((x-mean)/sigma)**2)
 return gaussian + linear

def fcn(norm, mean, sigma, c0, c1): #Definimos la función núcleo
 expt = model(vx, norm, mean, sigma, c0, c1)
 delta = (vy-expt)/vyerr
 return (delta[vy>0.]**2).sum()

evt = np.load('dimuon.npy') #Se cargan los datos a trabajar (seleccionar "dimuon.npy" o "clean_data.npy")
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje Y y bordes de X
vx = 0.5*(edges[1:]+edges[:-1]) #Eje X
vyerr = vy**0.5 #Varianza estándar de Poisson


m = Minuit(fcn, norm=6000., mean=3.09, sigma=0.04, c0=200., c1=0.)
m.migrad() #Se busca el mínimo
m.minos() #Calculamos errores asimétricos
m.print_param() #Imprimimos el resumen de parámetros

plt.plot([xmin,xmax],[0.,0.],c='black',lw=2)
plt.errorbar(vx, vy, yerr = vyerr, fmt = '.')
cx = np.linspace(xmin,xmax,500)
cy = model(cx,m.values['norm'],m.values['mean'],
 m.values['sigma'],m.values['c0'],m.values['c1'])
cy_bkg = model(cx,0.,m.values['mean'],
 m.values['sigma'],m.values['c0'],m.values['c1'])
plt.plot(cx, cy, c='red',lw=2)
plt.plot(cx, cy_bkg, c='red',lw=2,ls='--')
plt.xlabel('GeV')
plt.ylabel('Eventos/0.02GeV')

plt.grid()
plt.show()
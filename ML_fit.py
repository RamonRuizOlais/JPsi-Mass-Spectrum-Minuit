import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit

def model(x, norm, mean, sigma, c1): #Definimos la función de verosimilitud
 linear = (1. + c1*x)/((xmax-xmin) + c1*(xmax**2-xmin**2)/2.) #Función para el background
 gaussian = 1./(2.*np.pi)**0.5/sigma * \
 np.exp(-0.5*((x-mean)/sigma)**2) #Función de distribucion para los datos
 fs = norm/len(evt)
 return fs*gaussian + (1.-fs)*linear

def fcn(norm, mean, sigma, c1): #Se le asigna una verosimilitud a cada evento
 L = model(evt, norm, mean, sigma, c1)
 if np.any(L<=0.): return 1E100
 return -2.*np.log(L).sum()

evt = np.load('dimuon.npy') #Cargamos los datos a trabajar
evt = evt[abs(evt-3.1)<0.5] #Definimos la cantidad de eventos
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje y y bordes de x
vx = 0.5*(edges[1:]+edges[:-1]) #Eje x
vyerr = vy**0.5 #Varianza estándar de Poisson

m = Minuit(fcn, norm=6000., mean=3.09, sigma=0.04, c1=0.)
m.migrad() #Se busca el mínimo
m.minos() #Calculamos errores asimétricos
m.print_param() #Imprimimos el resumen de parámetros

fig = plt.figure(figsize=(6,6), dpi=80)
plt.plot([xmin,xmax],[0.,0.],c='black',lw=2)
plt.errorbar(vx, vy, yerr = vyerr, fmt = '.')
cx = np.linspace(xmin,xmax,500)
cy = model(cx,m.values['norm'],m.values['mean'],m.values['sigma'], #Normalizamos la función de verosimilitud a 1
m.values['c1'])*xbinwidth*len(evt)                 #multiplicamos el número de eventos por el ancho de los bin
cy_bkg = model(cx,0.,m.values['mean'],m.values['sigma'],
m.values['c1'])*xbinwidth*(len(evt)-m.values['norm'])
plt.plot(cx, cy, c='red',lw=2)
plt.plot(cx, cy_bkg, c='red',lw=2,ls='--') 
plt.xlabel('GeV')
plt.ylabel('Eventos/0.02GeV')
plt.grid()
plt.show()

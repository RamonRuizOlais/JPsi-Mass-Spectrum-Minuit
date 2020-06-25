# Espectro-de-masa-de-JPsi-Minuit

La partícula J/Psi es un mesón de sabor neutro que consta de un quark encanto y un anti-quark encanto, particularmente famosa por conllevar varias confirmaciones teóricas importantes en su descubrimiento, entre ellas la existencia de un cuarto quark "encanto" y la idea de que los quarks vienen por pares, posteriormente gracias a esta partícula también se confirma la "libertad asintótica" que dice que la fuerza entre los quarks es mayor conforme su distancia aumenta, una característica muy particular de los quarks.
Con los siguientes códigos vamos a calcular el espectro de masa de esta partícula a través de tres métodos estadísticos y el módulo Minuit. A continuación dejo una pequeña guía con notas sobre como cargar y utilizar bibliotecas y las correspondientes diferencias según cada método, se escribirá en el orden en que se acoplan los códigos.

# Bibliotecas
Vamos a necesitar cargar numpy, iminuit y matplotlib. Las tres bibliotecas se pueden instalar a través de pip.

Numpy:
<pre><code>
pip install numpy
</code></pre>

Matplotlib:
<pre><code>
python -m pip install -U matplotlib
</code></pre>

iminuit:
<pre><code>
pip install iminuit
</code></pre>

Una vez instalados pueden ser fácilmente llamados de la siguiente forma:
<pre><code>
import numpy as np
from iminuit import Minuit
import matplotlib.pyplot as plt
</code></pre>
Nota: Para este trabajo solo necesitamos la función Minuit de la biblioteca iminuit, por eso solo se llamó a esta.

# Función modelo y función núcleo
La función modelo y núcleo sufriran pequeñas modificaciones según sea el caso del método estadístico con el que vayamos a trabajar.

Mínimos cuadrados:

<pre><code>
def model(x, norm, mean, sigma, c0, c1): #Definimos la función para el ajuste de datos
 linear = c0 + c1*(x-xmin)/(xmax-xmin)
 gaussian = norm*xbinwidth/(2.*np.pi)**0.5/sigma * \
 np.exp(-0.5*((x-mean)/sigma)**2)
 return gaussian + linear

def fcn(norm, mean, sigma, c0, c1): #Definimos la función núcleo
 expt = model(vx, norm, mean, sigma, c0, c1)
 delta = (vy-expt)/vyerr
 return (delta[vy>0.]**2).sum()
</code></pre>

Máxima verosimilitud:

<pre><code>
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
</code></pre>

Máxima verosimilitud extendida:

<pre><code>
def model(x, ns, nb, mean, sigma, c1): #Definimos la función de verosimilitud
 linear = (1. + c1*x)/((xmax-xmin) + c1*(xmax**2-xmin**2)/2.) #Función del background
 gaussian = 1./(2.*np.pi)**0.5/sigma * np.exp(-0.5*((x-mean)/sigma)**2) #Función de distribución
 return ns*gaussian + nb*linear  #La versión actualizada Li

def fcn(ns, nb, mean, sigma, c1): #Se le asigna una verosimilitud a cada evento
 L = model(evt, ns, nb, mean, sigma, c1)
 if np.any(L<=0.): return 1E100
 return 2.*(ns+nb)-2.*np.log(L).sum()
</code></pre>

# Selección de datos
Para realizar un ajuste primero necesitamos obtener datos, los datos utilizados para este proyecto fueron obtenidos de un experimento que consistió en una colisión protón-protón en 2010. De aquí se obtuvieron los sets de datos "dimuon.npy" y "clean_data.npy". Es importante colocar los datos en la ubicación que abras con tu IDLE (en caso de que uses uno) y que los cargues a tu programa para poder trabajarlos. Respecto al ajuste, es importante aclarar de nuevo que hay pequeñas modificaciones según cada método.

Mínimos cuadrados:
Podemos trabajar con cualquier set de datos.

<pre><code>
evt = np.load('dimuon.npy') #Se cargan los datos a trabajar (seleccionar "dimuon.npy" o "clean_data.npy")
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje Y y bordes de X
vx = 0.5*(edges[1:]+edges[:-1]) #Eje X
vyerr = vy**0.5 #Varianza estándar de Poisson
</code></pre>

Máxima verosimilitud y su versión extendida:
Aquí la única distinción entre un método y otro son los datos a trabajar, el método de máxima verosimilitud solo puede trabajar el conjunto de datos "dimuon.npy", sin embargo su versión extendida puede trabajar con cualquiera de los dos, aunque se agregó específicamente para trabajar "clean_data.npy".

<pre><code>
evt = np.load('dimuon.npy') #Cargamos los datos a trabajar (Seleccionar según el método)
evt = evt[abs(evt-3.1)<0.5] #Definimos la cantidad de eventos
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje y y bordes de x
vx = 0.5*(edges[1:]+edges[:-1]) #Eje x
vyerr = vy**0.5 #Varianza estándar de Poisson
</code></pre>

# Minuit
Minuit es una herramienta computacional en formato de módulo para Python 3, originalmente escrita en FORTRAN, que se utiliza para encontrar el mínimo de funciones multivariables y hacer análisis de la forma de la función alrededor de este punto, está intencionada para el análisis estadístico y cálculo de valores de parámetros.
Según sea el caso de cada método estadístico hay que ser unos pequeños cambios

Mínimos cuadrados:

<pre><code>
m = Minuit(fcn, norm=6000., mean=3.09, sigma=0.04, c0=200., c1=0.)
m.migrad() #Se busca el mínimo
m.minos() #Calculamos errores asimétricos
m.print_param() #Imprimimos el resumen de parámetros
</code></pre>

Máxima verosimilitud:

<pre><code>
m = Minuit(fcn, norm=6000., mean=3.09, sigma=0.04, c0=200., c1=0.)
m.migrad() #Se busca el mínimo
m.minos() #Calculamos errores asimétricos
m.print_param() #Imprimimos el resumen de parámetros
</code></pre>

Máxima verosimilitud extendida:

<pre><code> 
 m = Minuit(fcn, ns=6000., nb=14000., mean=3.09, sigma=0.04, c1=0.)
 m.migrad() #Se busca el mínimo
 m.minos() #Calculamos errores asimétricos
 m.print_param() #Imprimimos el resumen de parámetros
 </code></pre>

# Gráfica del ajuste
No olvidemos que hay que graficar los ajustes que realizamos, de nuevo para cada método habrá una ligera modificación.

Mínimos cuadrados:

<pre><code>
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
</code></pre>

Máxima verosimilitud:

<pre><code>
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
</code></pre>

Máxima verosimilitud extendida:

<pre><code>
fig = plt.figure(figsize=(6,6), dpi=80)
plt.plot([xmin,xmax],[0.,0.],c='black',lw=2)
plt.errorbar(vx, vy, yerr = vyerr, fmt = '.')
cx = np.linspace(xmin,xmax,500)
cy = model(cx,m.values['ns'],m.values['nb'],m.values['mean'], #Normalizamos la función de verosimilitud a 1
 m.values['sigma'],m.values['c1'])*xbinwidth    #multiplicamos el número de eventos por el ancho de los bin
cy_bkg = model(cx,0.,m.values['nb'],m.values['mean'],
 m.values['sigma'],m.values['c1'])*xbinwidth
plt.plot(cx, cy, c='red',lw=2)
plt.plot(cx, cy_bkg, c='red',lw=2,ls='--')
plt.xlabel('GeV')
plt.ylabel('Eventos/0.02GeV')
plt.grid()
plt.show()
</code></pre>

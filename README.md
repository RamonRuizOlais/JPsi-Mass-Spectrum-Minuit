# Espectro-de-masa-de-JPsi-Minuit

La partícula J/Psi es un mesón de sabor neutro que consta de un quark encanto y un anti-quark encanto, particularmente famosa por conllevar varias confirmaciones teóricas importantes en su descubrimiento, entre ellas la existencia de un cuarto quark "encanto" y la idea de que los quarks vienen por pares, posteriormente gracias a esta partícula también se confirma la "libertad asintótica" que dice que la fuerza entre los quarks es mayor conforme su distancia aumenta, una característica muy particular de los quarks.
Con los siguientes códigos vamos a calcular el espectro de masa de esta partícula a través de tres métodos estadísticos y el módulo Minuit.

# Minuit
Puede ser instalado a través de pip
<pre><code>
pip install iminuit
</code></pre>

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
 from iminuit import Minuit
 m = Minuit(fcn, ns=6000., nb=14000., mean=3.09, sigma=0.04, c1=0.)
 m.migrad() #Se busca el mínimo
 m.minos() #Calculamos errores asimétricos
 m.print_param() #Imprimimos el resumen de parámetros
</code></pre>

# Selección de datos
Para realizar un ajuste primero necesitamos obtener datos, los datos utilizados para este proyecto fueron obtenidos de un experimento que consistió en una colisión protón-protón en 2010. De aquí se obtuvieron los sets de datos "dimuon.npy" y "clean_data.npy". Es importante colocar los datos en la ubicación que abras con tu IDLE (en caso de que uses uno) y que los cargues a tu programa para poder trabajarlos. Respecto al ajuste, es importante aclarar de nuevo que hay pequeñas modificaciones según cada método.

Mínimos cuadrados:
Podemos trabajar con cualquier set de datos.

<pre><code>
import numpy as np
evt = np.load('dimuon.npy') #Se cargan los datos a trabajar (seleccionar "dimuon.npy" o "clean_data.npy")
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje Y y bordes de X
vx = 0.5*(edges[1:]+edges[:-1]) #Eje X
vyerr = vy**0.5 #Varianza estándar de Poisson
</code></pre>

Máxima verosimilitud y su versión extendida:
Aquí la única distinción entre un método y otro son los datos a trabajar, el método de máxima verosimilitud solo puede trabajar el conjunto de datos "dimuon.npy", sin embargo su versión extendida puede trabajar con cualquiera de los dos, aunque se agregó específicamente para trabajar "clean_data.npy".

<pre><code>
import numpy as np
evt = np.load('dimuon.npy') #Cargamos los datos a trabajar (Seleccionar según el método)
evt = evt[abs(evt-3.1)<0.5] #Definimos la cantidad de eventos
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje y y bordes de x
vx = 0.5*(edges[1:]+edges[:-1]) #Eje x
vyerr = vy**0.5 #Varianza estándar de Poisson
</code></pre>


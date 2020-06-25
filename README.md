# Espectro-de-masa-de-JPsi-Minuit

La partícula J/Psi es un mesón de sabor neutro que consta de un quark encanto y un anti-quark encanto, particularmente famosa por conllevar varias confirmaciones teóricas importantes en su descubrimiento, entre ellas la existencia de un cuarto quark "encanto" y la idea de que los quarks vienen por pares, posteriormente gracias a esta partícula también se confirma la "libertad asintótica" que dice que la fuerza entre los quarks es mayor conforme su distancia aumenta, una característica muy particular de los quarks.
Con los siguientes códigos vamos a calcular el espectro de masa de esta partícula a través de tres métodos estadísticos y el módulo Minuit.

# Minuit
Puede ser instalado a través de pip
<pre><code>
pip install iminuit
</code></pre>

Minuit es una herramienta computacional en formato de módulo para Python 3, originalmente escrita en FORTRAN, que se utiliza para encontrar el mínimo de funciones multivariables y hacer análisis de la forma de la función alrededor de este punto, está intencionada para el análisis estadístico y cálculo de valores de parámetros.

<pre><code> 
 from iminuit import Minuit
 m = Minuit(fcn, ns=6000., nb=14000., mean=3.09, sigma=0.04, c1=0.)
 m.migrad() #Se busca el mínimo
 m.minos() #Calculamos errores asimétricos
 m.print_param() #Imprimimos el resumen de parámetros
</code></pre>

# Selección de datos y datos para el ajuste
Para realizar un ajuste primero necesitamos obtener datos, los datos utilizados para este proyecto fueron obtenidos de un experimento que consistió en una colisión protón-protón en 2010. De aquí se obtuvieron los sets de datos "dimuon.npy" y "clean_data.npy". Es importante colocar los datos en la ubicación que abras con tu IDLE (en caso de que uses uno) y que los cargues a tu programa para poder trabajarlos.
<pre><code>
evt = np.load('dimuon.npy') #Se cargan los datos a trabajar (seleccionar "dimuon.npy" o "clean_data.npy")
xmin, xmax, xbinwidth = 2.6, 3.6, 0.01 #Mantenemos los eventos entre 2.6 y 3.6
vy,edges = np.histogram(evt, bins=100, range=(xmin,xmax)) #Eje Y y bordes de X
vx = 0.5*(edges[1:]+edges[:-1]) #Eje X
vyerr = vy**0.5 #Varianza estándar de Poisson
</code></pre>  


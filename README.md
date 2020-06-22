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
  


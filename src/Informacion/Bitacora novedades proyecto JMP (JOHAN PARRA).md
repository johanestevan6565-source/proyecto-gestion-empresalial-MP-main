25/12/25 23:58



-se hizo funcionar los archivos Json del menu de clientes para sobrescribir y redactar los datos propuestos.

-agregue el archivo "main".

-cambios hechos en functions\_clientes.py

 	-se uso un nuevo comando "import = os" ¨.path" ".dirname" "(\_\_file\_\_)"

 	-se cambio la ruta usada en la(s) líneas 6, 13. Añadiéndole "encoding = -8" además de cambiar la ruta de "datos" por "datos\_clientes"

 	-se creo una nueva variable "BASE\_DIR" y "datos\_clientes"

-cambios hechos en menu\_clientes.py

 	-se cambio los textos

 	print("\\n menu \\n")

    	print("1. Agregar cliente")

    	print("2. Listado de clientes")

    	print("3. volver al menu principal")

 	de las líneas 3,4 y 5 a las líneas 7,8,9 y 10. se realizo este cambio para mantener las opciones dentro del bucle "while true" por motivos de practicidad y visualización general en la consola.





26/12/25 22:15



\- se agrego el modulo "menu\_productos.py"

\- se agrego la función "functions\_productos"

\- se implemento la lógica relacionada a cada modulo

**nota importante** \[en el modulo "functions\_productos" se implemento el cambio a la función "obtener\_productos\_flexible" la cual esta bien implementada pero no se ha encontrado ni anexado algun uso real,recordatorio para anexarla a futuras revisiones, esto se hizo para que el usuario pueda buscar tanto por ID "PID" como por nombre del producto (con relacion a este modulo) pero no se ha podido anexar a ninguna funcion util]





26/12/25 23:38



-se soluciono y se aplico la nota anterior, ya se le dio uso real a la implementación

-se añadió una nueva función llamada "normaliar\_texto" su implementación se usara para facilitar la búsqueda por nombre al usuarion sin que se vea afectada la base de datos, se implemento como un completento de la función "obtener\_productos\_flexibles"



nota \[hay observaciones en 3 aspectos. 1. se duplica de manera inconsistente la información en el submodulo ("#5 cambiar precio de producto" / liena 53:85 / menu\_productos) encontrar la liena que da ese fallo de datos, 2. no se ha posido solucionar la falla de "poder editar productos tanto con nombre como por ID (PID)" atención a esto antes de continuar 3. hacer los respectivos cambios en el submodulo ("2. editar producto" / linea 22:40 / menu\_productos)]



nota \[probar los demás modulos y posibles variables que pueda desarrollar el cliente antes de continuar, una vez que este en funcionamiento de lo básico, proseguir a continuar con el modulo de "registro de ventas por cliente"]



nota \[al terminar el modulo "menu\_productos" crear un commit y subirlo a github]





27/12/25 22:02

-se ha corregido el fallo visual y lógico dispuesto en la nota anterior, el código funciona de manera esperada, en los modulos "editar precio" y "editar nombre", el error lógico que producia el fallo de la búsqueda de datos es un if en mala posición, dado como valido todas las entradas sin verificar si es true o false, asi que nunca se comparaba los resultados, segundo error lógico, nunca se comparaba directamente la entrada del usuario con la base de datos, produciendo nuevamente el error de "ID no encontrada" tercer fallo lógico: se hacia una doble búsqueda, tanto en el modulo de funciones, como en el modulo de menu, por ende si en uno daba error, en el otro generaba los mismos resultados, además de ser rebundante e inecesario el uso de 2 búsquedas en el mismo modulo

-se añadió la opción de "eliminar producto" funciona con normalidad.





28/12/25 22:11

-se ha encontrado un error en el modulo de "agregar producto" no se han integrado variables de fallo

nota\[verificar al detalle todas las variables de fallo en todos los submodulos de "menu\_productos" para evitar fallos a futuro





28/12/25 23:14



-se han corregido todos lo errores lógicos de las subfunciones del modulo "menu\_productos"

-se han añadido funciones de variables en el submodulo "#agregar producto" del modulo "menu\_productos" para simplificar el uso de código innecesario y que sea mas legible

-se añadió las siguientes funciones en el modulo "functions\_productos":

 	-#función de pedir nombre del producto \[21:39]

 	-#función de pedir precio del producto \[43:63]

nota: añadir simplificaciones a todos los demás submodulos para asi, con este cambio ayudar a legibilidad del código y por ende la sustentabilidad mas a futuro de este mismo



28/12/25 13:35



-se han implementado optimizaciones del código de el modulo "menu\_productos"

-se han añadido nuevas funciones a "functions\_productos" el cual es "#reactivar productos" \[198:204] el cual su función es reactivar los productos "eliminados" haciendo asi que cualquier fallo del usurario sea reversible, asi evitar fallos por perditda de datos o búsquedas erróneas por ID



nota: solucionar los fallos producidos por los nuevos cambios en el modulo de "#listar productos" arreglar ya que esta con los valores de (true/false) y en los valores de la función implícita son valores (activo/inactivo) revisar modulo por modulo para evitar fallos



nota: terminar de optimizar modulos y probar variables



nota: al terminar las nuevas revisiones, guardar el progrso en commit y posteriormente subirlo a github



07/01/26 23:05



feliz año nuevo



-se han corregido varios bugs de lógica que al intentar salir del submenu de productos, salía directamente al menu principal

-se corrigio los errores lógicos de la verificación de los estados de los productos, ahora su estado se ve afectado por los parámetros "activo=none" y de ahi derivan sus estados de "true" como "activo" y "false" como "inactivo"

-se ha implementado una nueva función llamada:

 	-#función de seleccionar producto \[215:232]

-se ha optimizado la totalidad de los modulos

 	-"menu\_prodcutos.py"

 	-"functions\_productos.py"

se han subido los cambios





08/01/26 00:23



-se ha optimizado el código usado en los modulos relacionados con {clientes}

-se ha reorganizado gran parte de las funciones de {clientes}

-se han implementado algunos cambios lógicos y de UX al modulo de "menu\_clientes" para facilitar su legibilidad y manutención a futuro



05/02/26 20:56

-se han ordenado todas las carpetas del proyecto

nota: el orden de momento es temporal, en un futuro organizar mejor los archivos, aparte recordar cambiar también la ubicación de búsqueda en los archivos con la terminación functions

-se han agregado los siguientes archivos en la carpeta modulos

 	-"inventarios" (carpeta principal)

 	-"Data"

 	-"Functions"

 	-"Menu\_debug"

-se han añadido lógica base para el funcionamiento del modulo inventarios con las siguientes funciones

 	-comprobar archivos existentes "fecha por mes"

 	-registrar evento según corresponda (año/mes/dia/hora) en la carpeta correspondiente



08/02/26 

-se ha completado el modulo de inventarios

nota: probar en un menú debug para saber que todo el código funciona a la perfeccion

nota: anexar función #calcular\_stock\_producto \[109/122] al modulo de ventas para que asi se pueda verificar el stock de los productos y de esta forma se pueda realizar la compra

nota: pulir aun mas cosas del modulo para que asi en la revisión final este lo mas completo 


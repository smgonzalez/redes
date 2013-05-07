Ejercicio 1: 
    Averiguar la(s) dirección(es) MAC asociada(s) a una determinada dirección IP.
    Ejecutar: ./ej1 <dirección IP>
    La consulta se efectúa enviando un paquete ARP broadcast, de tipo who-has, con la dirección a consultar como dirección de destino.
    
Ejercicio 2: 
    Capturar tráfico ARP en una red. Los resultados se guardan en ./capturas/(timestamp).data
    Ejecutar: ./ej2
    Interrumpir la captura con Ctrl + C
    
Entropimetro.py:
    Módulo python.
    Entropimetro.calcularTodo(dump, start = None, end = None):
        Calcula la entropía en bits para los datos almacenados en <dump>, comenzando en start (si no fue provisto, desde el comienzo del dump) y finalizando en end (si no fue provisto, hasta el final del dump). Las líneas de dump deben ser compatibles con el formato escrito por ej2, así como también el formato de start y end.
    
    Entropimetro.contarSimbolos(dump, start= None, end = None):
        Retorna un objeto Counter, donde Counter[simbolo] = cantidad de apariciones (simbolo)
        start y end operan de la misma manera que en el caso anterior.
        
    Entropimetro.contarHosts(dump, start = None, end = None):
        Retorna un objeto Counter, donde Counter[host] = cantidad de apariciones de host en el campo ipDst del paquete ARP. Ídem start y end.
        
    Entropimetro.calcularInfoPorHost(dump):
        Dado un dump, devuelve un diccionario (host => info) donde host es cada uno de las direcciones ipDst del dump, e info representa la cantidad de información que dichas direcciones contienen.
        
    Entropimetro.entropia(counter):
        Recibe un objeto Counter[simbolo] = cantidad de apariciones (simbolo), y calcula la entropía, en bits, tomando la frecuencia relativa de cada símbolo.
        
parser.py:
    Modulo python.
    parser.readFilteredLine(f, filtro);
        Dado un objeto file: f, y una expresión booleana: filtro(l), devuelve la próxima línea del archivo a leer que satisface filtro. Además, si filtro(l) = None, se da por finalizada la lectura.
        
    parser.filtrarPorTiempo(linea, timeStart, timeEnd):
        Evalúa que el tipo de mensaje sea who-has y que el timestamp de linea se encuentre entre las cotas temporales provistas.
    
import numpy as np
import sys
from Graficacion import Graficacion

class Coloracion:

    def __init__(self):
        self.grafica = None
        self.vertices = 0
        self.aristas = 0
        
    @staticmethod
    def leer_archivo(archivo):
        """ Función que genera una instancia de Coloracion
            a partir de leer un archivo en el que describe
            una gráfica.

        Args:
            archivo (string): nombre del archivo a leer

        Returns:
            Coloracion: Instancia de la clase Coloracion con
            la gráfica descrita en el archivo
        """
        coloracion = Coloracion()
        with open(archivo, 'r') as datos:
            for linea in datos:
                cadena = linea.strip().split()
                if cadena[0] == 'c':
                    continue
                elif cadena[0] == 'p':
                    n = int(cadena[2])
                    coloracion.vertices = n
                    coloracion.aristas = int(cadena[3])
                    coloracion.grafica = [[0] * n for _ in range(n)]
                elif cadena[0] == 'e':
                    i = int(cadena[1]) - 1
                    j = int(cadena[2]) - 1
                    coloracion.grafica[i][j] = 1
                    coloracion.grafica[j][i] = 1
        return coloracion

    def funcion_evaluacion(self, colores):
        """ Función que evalúa una solución al problema
            de coloracion dependiendo de cuantas adyacencias
            entre vertices del mismo color existen y la cantidad
            de colores usados.

        Args:
            colores (array(int)): Arreglo con las asignaciones
            de color a cada vértice

        Returns:
            int: 
        """
        calificacion = 0
        for i in range(self.vertices):
            for j in range(self.vertices):
                if self.grafica[i][j] == 1 and colores[i] == colores[j]:
                    calificacion += 1
        for i in range(self.vertices):
            for j in range(len(colores)):
                if colores[j] == i+1:
                    calificacion += 1
                    break
        return calificacion
    
    def soluciones_aleatorias(self, iteraciones=10):
        """ Función para generar soluciones aleatorias

        Args:
            iteraciones (int, optional): Número de iteraciones para generar
            soluciones aleatorias. Defaults to 1000.

        Returns:
            (array(int)): Arreglo con la mejor solucion generada aleatoriamente
        """
        mejor_solucion = np.random.randint(1, self.vertices+1, self.vertices)
        for _ in range(iteraciones):
            solucion_actual = np.random.randint(1,self.vertices+1,self.vertices)
            if self.funcion_evaluacion(solucion_actual) <= self.funcion_evaluacion(mejor_solucion):
                mejor_solucion = solucion_actual
        return mejor_solucion
    
    def funcion_vecindad(self, solucion_actual):
        """ Funcion que selecciona al primer vecino "mejorado"

        Args:
            solucion_actual (array(int)): Arreglo con la solucion actual

        Returns:
            array(int): Regresa al mejor vecino encontrado
        """
        vecino = self.obtener_vecino(solucion_actual)
        while self.funcion_evaluacion(vecino) > self.funcion_evaluacion(solucion_actual):
            vecino = self.obtener_vecino(solucion_actual)
        return vecino
    
    def obtener_vecino(self, solucion_actual):
        """ Obtiene un vecino de la solucion actual

        Args:
            solucion_actual (array(int)): Arreglo con la solucion actual
            
        Returns:
            array(int): Arreglo de la solucion actual con una mutacion
        """
        nuevo_color = np.random.randint(1, self.vertices+1)
        indice = np.random.randint(0, len(solucion_actual))
        solucion_actual[indice] = nuevo_color
        return solucion_actual
    
    def busqueda_escalada(self, iteraciones=1000):
        """ Funcion para realizar una busqueda por escalada 

        Args:
            iteraciones (int, optional): Iteraciones para la busqueda por escalada. Defaults to 1000.

        Returns:
            array(int): Arreglo con la mejor solucion encontrada
        """
        mejor_solucion = np.random.randint(1, self.vertices+1, self.vertices)
        for _ in range(iteraciones):
            mejor_solucion = self.funcion_vecindad(mejor_solucion)
        return mejor_solucion
    
    def  busqueda_local_iterada(self, iteraciones=1000):
        """ Funcion para realizar una busqueda local iterada

        Args:
            iteraciones (int, optional): Iteraciones para la búsqueda local iterada. Defaults to 1000.

        Returns:
            array(int): Arreglo con la mejor solución encontrada
        """
        mejor_solucion = np.random.randint(1, self.vertices+1, self.vertices)
        for _ in range(iteraciones):
            solucion_modificada = self.perturbacion(mejor_solucion)
            mejor_solucion_local = self.funcion_vecindad(solucion_modificada)
            if self.funcion_evaluacion(mejor_solucion_local) <= self.funcion_evaluacion(mejor_solucion):
                mejor_solucion = mejor_solucion_local
        return mejor_solucion
            
    def perturbacion(self, solucion_actual):
        """Función para modificar la solución actual, toma cierto
            numero de indices de la solucion y los modifica

        Args:
            solucion_actual (array(int)): Representación de la solución
        Returns:
            array(int): Arreglo con la solución actual modificada
        """
        cantidad_indices = int(len(solucion_actual)/10) + 1
        indices = np.random.randint(len(solucion_actual), size=cantidad_indices)
        for i in indices:
            solucion_actual[i] = np.random.randint(1, len(solucion_actual)+1)
        return solucion_actual
        
        
    def genera_poblacion_inicial(self, tamanio_poblacion):
        """Genera una población inicial con un tamaño especificado

        Args:
            tamanio_poblacion (int): Tamaño de la población a generar

        Returns:
            array(array(int)): Población generada
        """
        return np.random.randint(1, self.vertices+1, size = (tamanio_poblacion, self.vertices))
    
    def seleccion_padres_torneo(self, poblacion_actual):
        """Función para seleccionar a 2 padres de la poblacion dada

        Args:
            poblacion_actual (array(array(int))): Poblacion actual

        Returns:
            tuple: Ambos padres seleccionados
        """
        padre1, padre2 = None, None
        for j in range(2):
            indices_individuos = np.random.choice(len(poblacion_actual), size=int(len(poblacion_actual)/10), replace=False)
            individuos = [poblacion_actual[i] for i in indices_individuos]
            mejor_evaluacion = float("inf")
            mejor_individuo_actual = None
            for i in individuos:
                if self.funcion_evaluacion(i) < mejor_evaluacion:
                    mejor_evaluacion = self.funcion_evaluacion(i)
                    mejor_individuo_actual = i
            if j == 0:
                padre1 = mejor_individuo_actual
            else:
                padre2 =mejor_individuo_actual
        return padre1, padre2
        
    def selecciona_mejor_individuo(self, poblacion):
        """Funcion para encontrar al mejor individuo de la poblacion actual

        Args:
            poblacion (array(array(int))): Poblacion actual

        Returns:
            array(int): Mejor individuo de la poblacion actuaL
        """
        mejor_evaluacion = float("inf")
        mejor_individuo = None
        for i in poblacion:
            evaluacion = self.funcion_evaluacion(i)
            if evaluacion < mejor_evaluacion:
                mejor_evaluacion = evaluacion
                mejor_individuo = i
        return mejor_individuo
        
    def cruza_padres(self, padre1, padre2):
        """Cruza a los padres para generar a los hijos

        Args:
            padre1 (array(int)): Primer padre
            padre2 (array(int)): Segundo padre

        Returns:
            tuple: Hijos resultantes de la cruza 
        """
        mitad = int(len(padre1)/2)
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            if i < mitad:
                hijo1.append(padre1[i])
                hijo2.append(padre2[i])
            else:
                hijo1.append(padre2[i])
                hijo2.append(padre1[i])
        return hijo1, hijo2
    
    def mutacion(self, hijo):
        """Funcion para aplicar la mutacion a un hijo

        Args:
            hijo (array(int)): Hijo que mutara
        
        Returns:
            (array(int)): hijo con o sin mutacion
        """
        if np.random.random() <= 0.1:
            indice1 = np.random.randint(0, len(hijo))
            indice2 = np.random.randint(0, len(hijo))
            aux = hijo[indice1]
            hijo[indice1] = hijo[indice2]
            hijo[indice2] = aux
        return hijo
    
    def genera_siguiente_poblacion(self, poblacion):
        """Funcion para generar la siguiente poblacion, se mantiene la mejor solucion actual

        Args:
            poblacion (array(array(int))): Poblacion actual

        Returns:
            array(array(int)): Nueva poblacion
        """
        hijos = []
        hijos.append(self.selecciona_mejor_individuo(poblacion))
        while len(hijos) < len(poblacion):
            padre1, padre2 = self.seleccion_padres_torneo(poblacion)
            hijo1, hijo2 = None, None
            if np.random.random() <= 0.7:
                hijo1, hijo2 = self.cruza_padres(padre1, padre2)
            else:
                hijo1 = padre1
                hijo2 = padre2
            hijo1 = self.mutacion(hijo1)
            hijo2 = self.mutacion(hijo2)
            hijos.append(hijo1)
            hijos.append(hijo2)
        return hijos
            
        
    def algoritmo_genetico(self, tamanio_poblacion, iteraciones=1000):
        """Funcion que ejecuta el algoritmo genetico para coloracion

        Args:
            tamanio_poblacion (int): Tamaño de la poblacion
            iteraciones (int, optional): Número de iteraciones a realizar en el algoritmo. Defaults to 1000.

        Returns:
            array(int): La mejor solución encontrada
        """
        file = open('Ejecucion.txt', 'w')
        poblacion = self.genera_poblacion_inicial(tamanio_poblacion)
        mejor_solucion = None
        for i in range(iteraciones):
            mejor_solucion = self.selecciona_mejor_individuo(poblacion)
            mejor_evaluacion = self.funcion_evaluacion(mejor_solucion)
            file.write(str(i) + " " + str(mejor_evaluacion) + "\n")
            poblacion = self.genera_siguiente_poblacion(poblacion)
        file.close()
        return mejor_solucion, mejor_evaluacion
                
    
    def realiza_busqueda(self, busqueda, iteraciones, tamanio_poblacion = 50):
        """ Función para realizar la búsqueda especificada

        Args:
            busqueda (str): Búsqueda a realizar
            iteraciones (int): Iteraciones a realizar en la búsqueda
        """
        if busqueda == "aleatoria":
            solucion_aleatoria = self.soluciones_aleatorias(iteraciones=iteraciones)
            print(f"Resultado de la busqueda aleatoria: {solucion_aleatoria}  con evaluacion de {self.funcion_evaluacion(solucion_aleatoria)}")
        elif busqueda == "escalada":
            solucion_escalada = self.busqueda_escalada(iteraciones=iteraciones)
            print(f"Resultado de la busqueda por escalada: {solucion_escalada} con evaluacion de {self.funcion_evaluacion(solucion_escalada)}")
        elif busqueda == "iterada":
            solucion_iterada = self.busqueda_local_iterada(iteraciones=iteraciones)
            print(f"Resultado de la busqueda local iterada: {solucion_iterada} con evaluacion de {self.funcion_evaluacion(solucion_iterada)}")
        elif busqueda == "genetica":
            solucion_genetica, evaluacion = self.algoritmo_genetico(tamanio_poblacion, iteraciones)
            print(f"Resultado del algoritmo genetico con tamaño de poblacion: {tamanio_poblacion}, iteraciones: {iteraciones} \n Mejor individuo encontrado {solucion_genetica} con usa evaluación de: {evaluacion}")
            Graficacion.grafica_txt("Ejecucion.txt", "Coloracion", iteraciones)
        else:
            print("Para seleccionar una busqueda debe escribir aleatoria o escalada")

if __name__ == "__main__":
    """Main donde se procesará el archivo ingresado y realizará la búsqueda especificada
    """
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Uso: python Coloracion.py <nombre_archivo> <busqueda> <iteraciones>")
    else:
        nombre_archivo = sys.argv[1]
        busqueda = sys.argv[2]
        coloracion = Coloracion.leer_archivo(nombre_archivo)
        #print(f"Representacion de la gráfica: \n {coloracion.grafica}")
        if len(sys.argv) == 4:
            coloracion.realiza_busqueda(busqueda, int(sys.argv[3]))
        elif len(sys.argv) == 5:
            coloracion.realiza_busqueda(busqueda, int(sys.argv[3]), int(sys.argv[4]))
        else:
            coloracion.realiza_busqueda(busqueda, 1000)
        
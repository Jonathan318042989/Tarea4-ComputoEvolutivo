import numpy as np
import sys

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
        
        
            
    
    def realiza_busqueda(self, busqueda, iteraciones):
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
        else:
            print("Para seleccionar una busqueda debe escribir aleatoria o escalada")
    
if __name__ == "__main__":
    """Main donde se procesará el archivo ingresado y realizará la búsqueda especificada
    """
    if len(sys.argv) < 3:
        print("Uso: python Coloracion.py <nombre_archivo> <busqueda>")
    else:
        nombre_archivo = sys.argv[1]
        busqueda = sys.argv[2]
        coloracion = Coloracion.leer_archivo(nombre_archivo)
        #print(f"Representacion de la gráfica: \n {coloracion.grafica}")
        if len(sys.argv) == 4:
            coloracion.realiza_busqueda(busqueda, int(sys.argv[3]))
        else:
            coloracion.realiza_busqueda(busqueda, 1000)
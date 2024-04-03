import math
import numpy as np

class Funciones:
    
    global dominio_sphere_rastrigin
    dominio_sphere_rastrigin = (-5.12, 5.12)
    global dominio_ackley
    dominio_ackley = (-30, 30)
    global dominio_griewank
    dominio_griewank = (-600, 600)
    global dominio_rosenbrock
    dominio_rosenbrock = (-2.048, 2.048)
    
    @staticmethod
    def rosenbrock(valores):
        """Método que implementa la función Rosenbrock

        Args:
            valores (list(float)): lista de valores con los que se evaluará la función

        Returns:
            float: resultado de evaluar la función
        """
        suma = 0
        for i in range(len(valores) - 1):
            term1 = 100 * (valores[i + 1] - valores[i] ** 2) ** 2
            term2 = (valores[i] - 1) ** 2
            suma += term1 + term2
        return suma
    
    @staticmethod
    def sphere(valores):
        """Método que implementa la función Sphere

        Args:
            valores (list(float)): lista de valores con los que se evaluará la función
        Returns:
            float: resultado de evaluar la función
        """
        suma = 0
        for i in range(len(valores)):
            suma += valores[i] ** 2
        return suma

    @staticmethod
    def rastrigin(valores):
        """Método que implementa la función Rastrigin

        Args:
            valores (list(float)): lista de valores con los que se evaluará la función
        Returns:
            float: resultado de evaluar la función
        """
        suma = 10 * len(valores)
        for i in range(len(valores)):
            suma += valores[i] ** 2
            suma -= 10 * math.cos(2 * math.pi * valores[i])
        return suma
    
    @staticmethod
    def ackley(valores):
        """Método que implementa la función Ackley

        Args:
            valores (list(float)): lista de valores con los que se evaluará la función
        Returns:
            float: resultado de evaluar la función
        """
        suma1 = 0
        suma2 = 0 
        for i in range(len(valores)):
            suma1 += valores[i]**2
        for i in range(len(valores)):
            suma2 += math.cos(2 * math.pi * valores[i])
        resultado = 20 + math.e - 20*np.exp(-0.2*(math.sqrt(suma1/len(valores)))) - np.exp(suma2/len(valores))
        return resultado
    
    @staticmethod
    def griewank(valores):
        """Método que implementa la función Griewank

        Args:
            valores (list(float)): lista de valores con los que se evaluará la función
        Returns:
            float: resultado de evaluar la función
        """
        suma = 0
        for i in range(len(valores)):
            suma += (valores[i]**2)/4000
        multi = 1
        for i in range(len(valores)):
            if i != 0:
                multi *= math.cos(valores[i]/math.sqrt(i))
        resultado = 1 + suma - multi
        return resultado
import random
import math
import numpy as np
import matplotlib.pyplot as plt

class Funciones:
    
    @staticmethod
    def rosenbrock(valores):
        suma = 0
        for i in range(len(valores) - 1):
            term1 = 100 * (valores[i + 1] - valores[i] ** 2) ** 2
            term2 = (valores[i] - 1) ** 2
            suma += term1 + term2
        return suma
    
    @staticmethod
    def sphere(valores):
        suma = 0
        for i in range(len(valores)):
            suma += valores[i] ** 2
        return suma

    @staticmethod
    def rastrigin(valores):
        suma = 10 * len(valores)
        for i in range(len(valores)):
            suma += valores[i] ** 2
            suma -= 10 * math.cos(2 * math.pi * valores[i])
        return suma
    
    @staticmethod
    def ackley(valores):
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
        suma = 0
        for i in range(len(valores)):
            suma += (valores[i]**2)/4000
        multi = 1
        for i in range(len(valores)):
            if i != 0:
                multi *= math.cos(valores[i]/math.sqrt(i))
        resultado = 1 + suma - multi
        return resultado

class AlgoritmoGenetico:
    
    def __init__(self, funcion_objetivo, longitud_cromosoma, dominio, tamano_poblacion=100, num_generaciones=100, prob_mutacion=0.1, elitismo=True):
        self.funcion_objetivo = funcion_objetivo
        self.longitud_cromosoma = longitud_cromosoma
        self.dominio = dominio
        self.tamano_poblacion = tamano_poblacion
        self.num_generaciones = num_generaciones
        self.prob_mutacion = prob_mutacion
        self.elitismo = elitismo
    
    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.tamano_poblacion):
            cromosoma = ''.join(random.choice('01') for _ in range(self.longitud_cromosoma))
            poblacion.append(cromosoma)
        return poblacion
    
    def evaluar_poblacion(self, poblacion):
        evaluaciones = []
        for cromosoma in poblacion:
            valores = self.decodificar_cromosoma(cromosoma)
            evaluacion = self.funcion_objetivo(valores)
            evaluaciones.append((cromosoma, evaluacion))
        return evaluaciones
    
    def seleccionar_padres(self, evaluaciones):
        total_fitness = sum(1 / evaluacion[1] for evaluacion in evaluaciones)
        padres_seleccionados = []
        while len(padres_seleccionados) < 2:
            punto = random.uniform(0, total_fitness)
            acumulado = 0
            for cromosoma, evaluacion in evaluaciones:
                acumulado += 1 / evaluacion
                if acumulado > punto:
                    padres_seleccionados.append(cromosoma)
                    break
        return padres_seleccionados
    
    def cruzar_padres(self, padre1, padre2):
        punto_cruza = random.randint(1, self.longitud_cromosoma - 1)
        hijo1 = padre1[:punto_cruza] + padre2[punto_cruza:]
        hijo2 = padre2[:punto_cruza] + padre1[punto_cruza:]
        return hijo1, hijo2
    
    def mutar(self, cromosoma):
        cromosoma_mutado = ''
        for bit in cromosoma:
            if random.random() < self.prob_mutacion:
                cromosoma_mutado += '1' if bit == '0' else '0'
            else:
                cromosoma_mutado += bit
        return cromosoma_mutado
    
    def reemplazar_generacional(self, poblacion, evaluaciones):
        nueva_generacion = []
        if self.elitismo:
            mejor_cromosoma = min(evaluaciones, key=lambda x: x[1])[0]
            nueva_generacion.append(mejor_cromosoma)
        while len(nueva_generacion) < self.tamano_poblacion:
            padres = self.seleccionar_padres(evaluaciones)
            hijo1, hijo2 = self.cruzar_padres(padres[0], padres[1])
            hijo1_mutado = self.mutar(hijo1)
            hijo2_mutado = self.mutar(hijo2)
            nueva_generacion.extend([hijo1_mutado, hijo2_mutado])
        return nueva_generacion
    
    def decodificar_cromosoma(self, cromosoma):
        longitud_seccion = len(cromosoma) // len(self.dominio)
        valores = []
        for i in range(0, len(cromosoma), longitud_seccion):
            seccion = cromosoma[i:i+longitud_seccion]
            valor_decimal = int(seccion, 2)
            valor_real = self.dominio[0] + (valor_decimal / (2**longitud_seccion - 1)) * (self.dominio[1] - self.dominio[0])
            valores.append(valor_real)
        return valores
    
    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        mejor_aptitud_por_generacion = []
        for _ in range(self.num_generaciones):
            evaluaciones = self.evaluar_poblacion(poblacion)
            mejor_aptitud = min(evaluaciones, key=lambda x: x[1])[1]
            mejor_aptitud_por_generacion.append(mejor_aptitud)
            poblacion = self.reemplazar_generacional(poblacion, evaluaciones)
        return mejor_aptitud_por_generacion

def graficar_evolucion(funcion_objetivo, longitud_cromosoma, dominio, titulo):
    ag = AlgoritmoGenetico(funcion_objetivo, longitud_cromosoma, dominio)
    mejor_aptitud_por_generacion = ag.ejecutar()
    plt.plot(mejor_aptitud_por_generacion)
    plt.title(titulo)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Aptitud")
    plt.show()

def ejecutar_experimentos(funciones, num_ejecuciones=30):
    resultados = {}
    for nombre_funcion, funcion in funciones.items():
        resultados[nombre_funcion] = {"mejor": float('inf'), "peor": float('-inf'), "promedio": 0}
        for _ in range(num_ejecuciones):
            ag = AlgoritmoGenetico(funcion, 10, (-5.12, 5.12))
            mejor_aptitud = min(ag.ejecutar())
            resultados[nombre_funcion]["mejor"] = min(resultados[nombre_funcion]["mejor"], mejor_aptitud)
            resultados[nombre_funcion]["peor"] = max(resultados[nombre_funcion]["peor"], mejor_aptitud)
            resultados[nombre_funcion]["promedio"] += mejor_aptitud
        resultados[nombre_funcion]["promedio"] /= num_ejecuciones
    return resultados

# Definir las funciones de prueba
funciones = {
    "sphere": Funciones.sphere,
    "rastrigin": Funciones.rastrigin,
    "ackley": Funciones.ackley,
    "griewank": Funciones.griewank,
    "rosenbrock": Funciones.rosenbrock
}

# Ejecutar el algoritmo genético múltiples veces y mostrar resultados estadísticos
resultados = ejecutar_experimentos(funciones)
print("\nResultados estadísticos:")
print("{:<10} {:<10} {:<10} {:<10}".format("Función", "Mejor", "Peor", "Promedio"))
for nombre_funcion, res in resultados.items():
    print("{:<10} {:<10.2f} {:<10.2f} {:<10.2f}".format(nombre_funcion, res["mejor"], res["peor"], res["promedio"]))


for nombre_funcion, funcion in funciones.items():
    titulo = f"Evolución de {nombre_funcion}"
    graficar_evolucion(funcion, 10, (-5.12, 5.12), titulo)

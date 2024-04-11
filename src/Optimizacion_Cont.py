import random
import math
import numpy as np
import matplotlib.pyplot as plt
from Funciones import *
from Codificacion import Codificacion

class AlgoritmoGenetico:
    
    def __init__(self, nombre_funcion, longitud_cromosoma, tamano_poblacion=100, num_generaciones=100, prob_mutacion=0.1, elitismo=True):
        self.nombre_funcion = nombre_funcion
        self.funcion_objetivo = funciones[nombre_funcion]
        self.longitud_cromosoma = longitud_cromosoma
        self.dominio = self.obtener_dominio(nombre_funcion)
        self.tamano_poblacion = tamano_poblacion
        self.num_generaciones = num_generaciones
        self.prob_mutacion = prob_mutacion
        self.elitismo = elitismo
        
    
    def obtener_dominio(self, nombre_funcion):
        if nombre_funcion in ["sphere", "rastrigin"]:
            return dominio_sphere_rastrigin
        elif nombre_funcion == "ackley":
            return dominio_ackley
        elif nombre_funcion == "griewank":
            return dominio_griewank
        elif nombre_funcion == "rosenbrock":
            return dominio_rosenbrock
        else:
            raise ValueError("Función no reconocida")

    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.tamano_poblacion):
            cromosoma = ''.join(random.choice('01') for _ in range(self.longitud_cromosoma))
            poblacion.append(cromosoma)
        return poblacion
    
    def evaluar_poblacion(self, poblacion):
        evaluaciones = []
        for cromosoma in poblacion:
            valores = Codificacion.decodifica_vector(cromosoma, self.longitud_cromosoma, *self.dominio)
            evaluacion = self.funcion_objetivo(valores)
            evaluaciones.append((cromosoma, evaluacion))
        return evaluaciones
    
    def seleccionar_padres(self, evaluaciones):
        total_fitness = sum(1 / evaluacion[1] if evaluacion[1] != 0 else 1 for evaluacion in evaluaciones)
        padres_seleccionados = []
        while len(padres_seleccionados) < 2:
            punto = random.uniform(0, total_fitness)
            acumulado = 0
            for cromosoma, evaluacion in evaluaciones:
                acumulado += 1 / evaluacion if evaluacion != 0 else 1
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
    
    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        mejor_aptitud_por_generacion = []
        for _ in range(self.num_generaciones):
            evaluaciones = self.evaluar_poblacion(poblacion)
            mejor_aptitud = min(evaluaciones, key=lambda x: x[1])[1]
            mejor_aptitud_por_generacion.append(mejor_aptitud)
            poblacion = self.reemplazar_generacional(poblacion, evaluaciones)
        return mejor_aptitud_por_generacion

def graficar_evolucion(funcion_objetivo, longitud_cromosoma, titulo):
    ag = AlgoritmoGenetico(funcion_objetivo, longitud_cromosoma)
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
            ag = AlgoritmoGenetico(nombre_funcion, 10)
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
    graficar_evolucion(nombre_funcion, 10, titulo)

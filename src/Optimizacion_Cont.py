import random
import numpy as np
import matplotlib.pyplot as plt
from Funciones import Funciones

class AlgoritmoGenetico:
    
    def __init__(self, funcion_objetivo, dominio, tamano_poblacion=100, num_generaciones=100, prob_mutacion=0.1, num_puntos_cruza=2, elitismo=True):
        self.funcion_objetivo = funcion_objetivo
        self.dominio = dominio
        self.tamano_poblacion = tamano_poblacion
        self.num_generaciones = num_generaciones
        self.prob_mutacion = prob_mutacion
        self.num_puntos_cruza = num_puntos_cruza
        self.elitismo = elitismo

    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.tamano_poblacion):
            solucion = [random.uniform(self.dominio[0], self.dominio[1]) for _ in range(len(self.dominio))]
            poblacion.append(solucion)
        return poblacion

    def evaluar_poblacion(self, poblacion):
        evaluaciones = []
        for individuo in poblacion:
            evaluacion = self.funcion_objetivo(individuo)
            evaluaciones.append((individuo, evaluacion))
        return evaluaciones

    def seleccionar_padres(self, evaluaciones):
        total_fitness = sum(1 / evaluacion[1] for evaluacion in evaluaciones)
        padres_seleccionados = []
        while len(padres_seleccionados) < 2:
            punto = random.uniform(0, total_fitness)
            acumulado = 0
            for individuo, evaluacion in evaluaciones:
                acumulado += 1 / evaluacion
                if acumulado > punto:
                    padres_seleccionados.append(individuo)
                    break
        return padres_seleccionados

    def cruzar_padres(self, padre1, padre2):
        puntos_cruza = sorted(random.sample(range(len(padre1)), self.num_puntos_cruza))
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            if i in puntos_cruza:
                hijo1.append(padre2[i])
                hijo2.append(padre1[i])
            else:
                hijo1.append(padre1[i])
                hijo2.append(padre2[i])
        return hijo1, hijo2

    def mutar(self, individuo):
        for i in range(len(individuo)):
            if random.random() < self.prob_mutacion:
                individuo[i] = random.uniform(self.dominio[0], self.dominio[1])
        return individuo

    def reemplazar_generacional(self, poblacion, evaluaciones):
        nueva_generacion = []
        if self.elitismo:
            mejor_solucion = min(evaluaciones, key=lambda x: x[1])[0]
            nueva_generacion.append(mejor_solucion)
        while len(nueva_generacion) < self.tamano_poblacion:
            padres = self.seleccionar_padres(evaluaciones)
            hijos = self.cruzar_padres(padres[0], padres[1])
            hijo1_mutado = self.mutar(hijos[0])
            hijo2_mutado = self.mutar(hijos[1])
            nueva_generacion.extend([hijo1_mutado, hijo2_mutado])
        return nueva_generacion

    def encuentra_peor(self, evaluaciones, peor):
        peor_candidato = max(evaluaciones, key=lambda x: x[1])[1]
        if peor_candidato > peor:
            return peor_candidato
        else:
            return peor 

    def calcula_promedio(self, evaluaciones, promedio_actual):
        suma = 0
        for i in range(len(evaluaciones)):
            suma += evaluaciones[i][1]
        suma /= len(evaluaciones)    
        promedio_actual += suma
        return promedio_actual/2

    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        mejor_aptitud_por_generacion = []
        peor = 0
        promedio = 0
        mejor = float("inf")
        for _ in range(self.num_generaciones):
            evaluaciones = self.evaluar_poblacion(poblacion)
            mejor_aptitud = min(evaluaciones, key=lambda x: x[1])[1]
            if mejor > mejor_aptitud:
                mejor = mejor_aptitud
            peor = self.encuentra_peor(evaluaciones, peor)
            promedio += self.calcula_promedio(evaluaciones, promedio)
            mejor_aptitud_por_generacion.append(mejor_aptitud)
            poblacion = self.reemplazar_generacional(poblacion, evaluaciones)
        return poblacion, mejor_aptitud_por_generacion, mejor, peor, promedio

def graficar_evolucion(funcion_objetivo, dominio, titulo):
    ag = AlgoritmoGenetico(funcion_objetivo, dominio)
    _, mejor_aptitud_por_generacion, mejor,  peor, promedio = ag.ejecutar()
    plt.plot(mejor_aptitud_por_generacion)
    plt.title(titulo)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Aptitud")
    plt.show()
    return mejor_aptitud_por_generacion, mejor,  peor, promedio

def ejecutar_experimentos(funciones, dominios, num_ejecuciones=30):
    resultados = {}
    for nombre_funcion, funcion in funciones.items():
        resultados[nombre_funcion] = {"mejor": float('inf'), "peor": float('-inf'), "promedio": 0}
        promedios = []
        for _ in range(num_ejecuciones):
            ag = AlgoritmoGenetico(funcion, dominios[nombre_funcion])
            _, mejor_aptitud_por_generacion = ag.ejecutar()
            mejor_aptitud = min(mejor_aptitud_por_generacion)
            resultados[nombre_funcion]["mejor"] = min(resultados[nombre_funcion]["mejor"], mejor_aptitud)
            resultados[nombre_funcion]["peor"] = max(resultados[nombre_funcion]["peor"], mejor_aptitud)
            promedios.append(mejor_aptitud)
        resultados[nombre_funcion]["promedio"] = sum(promedios) / num_ejecuciones
    return resultados


dominios = {
    "sphere": (-5.12, 5.12),
    "rastrigin": (-5.12, 5.12),
    "ackley": (-30, 30),
    "griewank": (-600, 600),
    "rosenbrock": (-2.048, 2.048)
}


funciones = {
    "sphere": Funciones.sphere,
    "rastrigin": Funciones.rastrigin,
    "ackley": Funciones.ackley,
    "griewank": Funciones.griewank,
    "rosenbrock": Funciones.rosenbrock
}


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python Optimizacion_Cont.py <funcion>")
        sys.exit(1)

    funcion_seleccionada = sys.argv[1]

    if funcion_seleccionada not in funciones:
        print("La función seleccionada no está disponible.")
        sys.exit(1)

    funcion_objetivo = funciones[funcion_seleccionada]
    dominio = dominios[funcion_seleccionada]

    titulo = f"Evolución de Aptitud para {funcion_seleccionada}"
    mejor_aptitud_por_generacion, mejor, peor, promedio = graficar_evolucion(funcion_objetivo, dominio, titulo)
    print(f"Función {funcion_seleccionada}. Mejor: {mejor}. Peor: {peor}. Promedio: {promedio}")
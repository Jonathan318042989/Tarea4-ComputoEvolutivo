import math
import numpy as np
import random
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
    
    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        mejor_aptitud_por_generacion = []
        for _ in range(self.num_generaciones):
            evaluaciones = self.evaluar_poblacion(poblacion)
            mejor_aptitud = min(evaluaciones, key=lambda x: x[1])[1]
            mejor_aptitud_por_generacion.append(mejor_aptitud)
            poblacion = self.reemplazar_generacional(poblacion, evaluaciones)
        return mejor_aptitud_por_generacion

def graficar_evolucion(funcion_objetivo, dominio, titulo):
    ag = AlgoritmoGenetico(funcion_objetivo, dominio)
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
            ag = AlgoritmoGenetico(funcion, dominios[nombre_funcion])
            mejor_aptitud = min(ag.ejecutar())
            resultados[nombre_funcion]["mejor"] = min(resultados[nombre_funcion]["mejor"], mejor_aptitud)
            resultados[nombre_funcion]["peor"] = max(resultados[nombre_funcion]["peor"], mejor_aptitud)
            resultados[nombre_funcion]["promedio"] += mejor_aptitud
        resultados[nombre_funcion]["promedio"] /= num_ejecuciones
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


for nombre_funcion, funcion in funciones.items():
    titulo = f"Evolución de Aptitud para {nombre_funcion}"
    graficar_evolucion(funcion, dominios[nombre_funcion], titulo)

resultados = ejecutar_experimentos(funciones)
print("\nResultados estadísticos:")
print("{:<10} {:<10} {:<10} {:<10}".format("Función", "Mejor", "Peor", "Promedio"))
for nombre_funcion, res in resultados.items():
    print("{:<10} {:<10.2f} {:<10.2f} {:<10.2f}".format(nombre_funcion, res["mejor"], res["peor"], res["promedio"]))

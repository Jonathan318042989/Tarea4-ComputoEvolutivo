import matplotlib.pyplot as plt 

class Graficacion:
    @staticmethod
    def grafica_txt(nombre_archivo, titulo, iteraciones):
        x = []
        y = []
        for linea in open(nombre_archivo, 'r'):
            lineas = [i for i in linea.split()]
            if int(lineas[0])%int(iteraciones/20) == 0 or int(lineas[0]) == iteraciones-1:
                x.append(lineas[0])
                y.append(int(lineas[1]))
        plt.title(titulo)
        plt.xlabel("Iteraciones")
        plt.ylabel("Evaluacion")
        plt.yticks(y)
        plt.plot(x,y,marker ='o', c = 'g')
        plt.show()
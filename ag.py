import random
import string

CADENA_A_BUSCAR = 'CAMILO'

class ADN:
    def __init__(self, generador, fitness, f_reproduccion, f_mutacion, porcentaje_mutacion):
        self.generador = generador
        self.fitness = fitness
        self.f_reproduccion = f_reproduccion
        self.f_mutacion = f_mutacion
        self.porcentaje_mutacion = porcentaje_mutacion
        
        self.genes = "" #aca tengo una nueva cadena
        self.fitness_result = 0

    def generar(self, longitud):
        self.genes = self.generador(longitud)

    def calcular_fitness(self):
        self.fitness_result = self.fitness(self.genes) #le paso la nueva cadena
        return self.fitness_result  #retorna el fitness de la especie (cantidad de coincidencias)

    def reproducir(self, pareja):
        genes_hijo = self.f_reproduccion(self, pareja)
        especie_hijo = ADN(self.generador, self.fitness, self.f_reproduccion, self.f_mutacion, self.porcentaje_mutacion)
        especie_hijo.genes = genes_hijo #a la nueva especie le asignamos la nueva cadena
        return especie_hijo

    def mutar(self):
        if random.random() < self.porcentaje_mutacion:
            self.genes = self.f_mutacion(self.genes) #se altera el valor de genes por las mutacion

    def __str__(self):
        return " ".join(self.genes)

class Poblacion:
    def __init__(self, cant_poblacion, generador, fitness, f_reproduccion, f_mutacion, porcentaje_mutacion):
        self.cant_poblacion = cant_poblacion
        self.generador = generador
        self.fitness = fitness
        self.f_reproduccion = f_reproduccion
        self.f_mutacion = f_mutacion
        self.porcentaje_mutacion = porcentaje_mutacion

        self.poblacion = [] #arreglo de especies
        self.fitness_total = 0
        self.fitness_results = []

        for i in range(1, cant_poblacion):
            especie = ADN(self.generador, self.fitness, self.f_reproduccion, self.f_mutacion, self.porcentaje_mutacion)
            especie.generar(len(CADENA_A_BUSCAR))
            self.poblacion.append(especie)
            fitness_especie = especie.calcular_fitness()
            self.fitness_total = self.fitness_total + fitness_especie #acumula los fitness de toda la poblacion
            self.fitness_results.append(fitness_especie) #arreglo de fitness por cada especie

    def seleccion(self): # Conservamos los cromosomas (especies) con mejor performance para luego convertirse en padres
        self.lista_reproduccion = []
        for i in range (0, len(self.poblacion)):
            porcentaje_especie = float(self.fitness_results[i])/self.fitness_total #la relacion de la cant de coincidencias de la especie con la  de todas las especies
            n = int(porcentaje_especie*len(self.poblacion))
            for j in range(0,n):
                self.lista_reproduccion.append(self.poblacion[i]) # le anaido a la lista j veces la especie

    def reproduccion(self): #Ejecutamos crossover para seleccionar simulitudes comunes entre padres y usarlas para crear hijos
        self.poblacion = []
        self.fitness_results = []
        self.fitness_total = 0

        for i in range(0, self.cant_poblacion):
            pareja_a = self.lista_reproduccion[random.randint(0,len(self.lista_reproduccion)-1)]
            pareja_b = self.lista_reproduccion[random.randint(0,len(self.lista_reproduccion)-1)]

            hijo = pareja_a.reproducir(pareja_b) #retorna la nueva especie incluida su nueva cadena
            self.poblacion.append(hijo)
            fitness_especie = hijo.calcular_fitness()
            self.fitness_total = self.fitness_total + fitness_especie
            self.fitness_results.append(fitness_especie)

    def mutar(self):
        for e in self.poblacion:
            e.mutar()

    def promedio_fitness(self):
        return float(self.fitness_total)/len(self.fitness_results)

    def imprimir(self):
        for especie in self.poblacion:
            print("{} {}".format(especie, especie.calcular_fitness()))

def generador(max): #max: longitud de CADENA_A_BUSCAR, retorna cadena nueva aleatoria con misma longitud de CADENA_A_BUSCAR
    cadena = ""
    for i in range(max):
        cadena = cadena + random.choice(string.ascii_uppercase)
    return cadena    

def fitness(cadena): #recibe la nueva cadena, is a candidate solution to the problem as input and produces as output
    cont = 0
    for i in range(0, len(cadena)):
        if cadena[i] == CADENA_A_BUSCAR[i]:
            cont = cont + 1
    return cont

def f_reproduccion(pareja1, pareja2): #crossover entre padres, one-point crossover
    k = random.randint(0, len(pareja1.genes))
    parte_izq = pareja1.genes[0:k]
    parte_der = pareja2.genes[k:]
    return parte_izq + parte_der #retornamos la nueva cadena

def f_mutacion(genes): #recibe los genes que tiene actualmente
    lista = list(genes)
    pos = random.randint(0, len(lista) - 1)
    lista[pos] = random.choice(string.ascii_uppercase)
    return "".join(lista) #retorna los genes mutados (cambio de valor en algun alelo)

def main():
    poblacion = 100
    max_iteraciones = 5000
    porcentaje_mutacion = 0.01
    inst_poblacion = Poblacion(poblacion, generador, fitness, f_reproduccion, f_mutacion, porcentaje_mutacion)
    for i in range(0, max_iteraciones):
        inst_poblacion.imprimir()
        print("({})==========================".format(i))
        inst_poblacion.seleccion()
        inst_poblacion.reproduccion()
        print("Promedio fitness: {}".format(inst_poblacion.promedio_fitness()))
        inst_poblacion.mutar()

if __name__ == '__main__':
    main()
from src.Individual import Individual
from src.settings import *

def elitism(population, news):
    """Ordenar segun fitness y eliminar a los peores reemplazandolos por los hijos creados.

    Args:
        population: Poblacion que va a conservar a los mejores
        news: Hijos creados que se agregaran a la poblacion (population)
    """
    population = sorted(population, key=orderByFitness, reverse=True)
    population = population[:(len(population)-len(news))]
    population.extend(news)
    return population


def orderByFitness(x):
    return x.fitness


def orderByMemoryFitness(x):
    return x.fitnessMemory


def makeUsableList(inputList=None):
    """Recibir una lista con todos los elementos de la entrada, retornar una lista con solo los elementos relevantes.
    Esto depende mucho de la entrada y su formato, de momento se trabaja igual como se hacia en CyES, quedando abierto a cambios una vez que se sepa como van a llegar los datos que nos van a entregar

    Args:
        inputList: Lista completa (def = None)

    Returns:
        usableList: Lista con solo los elementos relevantes
    """
    usableList = []
    usableList.append(inputList[7])
    usableList.append(inputList[8])
    usableList.append(inputList[9])

    for i in range(11, 19):
        usableList.append(inputList[i])

    for i in range(25, 54):
        usableList.append(inputList[i])

    return usableList


def parsePacket(file=None):
    """Interpretar 1 linea del archivo de entrada, retornar el resultado.

    Args:
        file: Archivo a leer (def = None)

    Returns:
        p: Paquete procesado, en forma de string
    """
    p = []
    line = file.readline()
    # for elem in line.split():
    #    p.append(int(elem))
    #p = ''.join(map(str, makeUsableList(p)))
    p = line
    return p


def crossIndividuals2(parent1={}, parent2={}):
    """Hacer 2 hijos a partir de los genes de los padres y retornarlos.

    Args:
        parent1: Genes del padre 1 para crear un hijo (def = None)
        parent2: Genes del padre 2 para crear un hijo (def = None)

    Returns:
        h1: Hijo generado
    """
    d1 = {}
    c = 0
    for i in parent1.keys():
        lista = []
        for j in range(len(parent1.get(i))):
            probability = ((parent1.get(i))[j][1]+(parent2.get(i))[j][1])/2
            lista.append([parent1.get(i)[j][0], probability])
        d1[i] = lista
    global INDIVIDUAL_COUNT
    INDIVIDUAL_COUNT = INDIVIDUAL_COUNT + 1
    return Individual(INDIVIDUAL_COUNT-1, d1, 0, 0)


def crossIndividuals(parent1={}, parent2={}):
    """Hacer 2 hijos a partir de los genes de los padres y retornarlos.

    Args:
        parent1: Genes del padre 1 para crear un hijo (def = None)
        parent2: Genes del padre 2 para crear un hijo (def = None)

    Returns:
        h1, h2: Los 2 hijos
    """
    d1 = {}
    d2 = {}
    c = 0
    for i in parent1.keys():
        if c % 2 == 0:
            d1[i] = parent1[i]
            d2[i] = parent2[i]
        else:
            d1[i] = parent2[i]
            d2[i] = parent1[i]
        print(str(type(parent1.get(i)))+" " +
              str(len(parent1.get(i)))+" " + str(parent1.get(i)[0][1]))
        c = c + 1
    global INDIVIDUAL_COUNT
    INDIVIDUAL_COUNT = INDIVIDUAL_COUNT + 2
    return Individual(INDIVIDUAL_COUNT-1, d1, 0, 0), Individual(INDIVIDUAL_COUNT, d2, 0, 0)


def evaluatePop(pop=None):
    """Obtener una evaluación de la población del modelo "model".

    Args:
        model: El modelo a evaluar (def = None)

    Returns:
        totalFitness: La suma de las fitness de toda la población.
    """

    if GRAPH == "promedio":
        totalFitness = 0
        for i in pop.individuals:
            totalFitness = totalFitness + i.fitness
        totalFitness = totalFitness/len(pop.individuals)

    elif GRAPH == "elite":
        totalFitness = 0
        for i in range(int(len(pop.individuals)*PERCENTAGE_ELITISM)):
            #print(f"ind{i}: ", pop.individuals[i].fitness)
            totalFitness = totalFitness + pop.individuals[i].fitness
        totalFitness = totalFitness / \
            int(len(pop.individuals)*PERCENTAGE_ELITISM)

    else:
        totalFitness = -1
        if(pop.memory != None):
            totalFitness = pop.memory.fitness

    return totalFitness


def attack(listFitness, models=None):
    """Evaluar posible ataque".

    Args:
        listFitness: lista del fitness historico

    Returns:
        booleano que determina si está en ataque
    """
    if models == None:
        if len(listFitness) > 11:
            for i in range(len(listFitness)-10, len(listFitness)):
                porcentaje = 1-(listFitness[-1]/listFitness[i])
                if porcentaje >= FITNESS_CHAGE_ATTACK:
                    return True

        if bool(listFitness) and listFitness[-1] <= 5:
            return True
    else:
        for i in models:
            if i.repose:
                if i.fitnessHistory[-1] >= listFitness[-1]:
                    return True
    return False

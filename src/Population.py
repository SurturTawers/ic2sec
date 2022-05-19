import random
import copy
from Individual import Individual
from utils import *

class Population:
    def __init__(self, individuals=[], modelType="normal"):
        self.individuals = individuals
        self.memory = None
        self.type = modelType
        self.alertLevel = 0
        self.repose = False
        self.timeActive = 0
        self.fitnessHistory = []

    def __repr__(self):
        repr = f"""
ind #: {len(self.individuals)}
memory:
{self.memory}
type: {self.type}
alertLevel: {self.alertLevel}
repose: {self.repose}
timeActive: {self.timeActive}
fitnessHistory: {self.fitnessHistory}
        """
        return repr

    def initializePop(self, num=100):
        """Generar población inicial.

        Args:
            num: Tamaño de la población (def = 100)
        """
        for i in range(num):
            gene = {
                "*": [["*", 1]]
            }
            self.individuals.append(Individual(i, gene, 0, 0))

    def feedPop(self, packet=None, lastPacket=None):
        """Alimentar a la poblacion de este modelo.

        Args:
            packet: El paquete con que se va a alimentar (def = None)
            lastPacket: Paquete anteriormente recibido
        """
        for i in self.individuals:
            i.eatPacket(packet, lastPacket)
        if(self.memory != None):
            self.memory.eatPacket(packet, lastPacket)

    def memoryUpdate(self):
        """Darle un punto de fitnessMemory a los individuos de la poblacion con mayor fitness despues de un ciclo.
        """
        maxFitness = self.individuals[0]
        i = 0
        while self.individuals[i] == maxFitness and len(self.individuals) < i:
            self.individuals[i].fitnessMemory+1
            i+1

    def memoryChange(self):
        """Cambiar la memoria de la poblacion, eligiendo al con mayor fitnessMemory
        """
        sorted(self.individuals, key=orderByMemoryFitness, reverse=True)
        self.memory = copy.deepcopy(self.individuals[0])
        for i in self.individuals:
            i.fitnessMemory = 0

    def selectParents(self, num=2):
        """Seleccionar num padres (usando torneo) y retornarlos como lista.

        Returns:
            p: Lista de padres
        """
        p = []
        for i in range(num):
            p.append(self.torneoSelect(2))

        return p

    def torneoSelect(self, size=2):
        """ Seleccionar mejor opcion, retornandola. Si ambos son iguales, se retorna uno al azar.

        Returns:
            o1 o o2: Mejor opcion.
        """
        #popCopy = copy.deepcopy(self.population)
        # random.shuffle(popCopy)
        #participants = popCopy[0:size]
        #participants.sort(key = orderByFitness, reverse = True)
        # return participants[0]

        popIDs = []
        for i in range(size):
            popIDs.append(1)
        for i in range(len(self.individuals) - size):
            popIDs.append(0)

        random.shuffle(popIDs)
        participants = [i for i, j in zip(self.individuals, popIDs) if j]
        participants.sort(key=orderByFitness, reverse=True)
        return copy.deepcopy(participants[0])

        #o1 = random.choice(self.population)
        #o2 = random.choice(self.population)
        # if o1.fitness > o2.fitness:
        #    return o1
        # elif o1.fitness < o2.fitness:
        #    return o2
        # else:
        #    return random.choice([o1,o2])

    def checkDictionaryUpdate(self, packetList):
        """Revisar si hay algun paquete nuevo que agregar a su matriz de markov
        """
        commonPackets = list(
            dict(filter(lambda p: int(p[1]) >= PACKETS_UMBRAL, packetList.items())).keys())
        for i in commonPackets:
            for j in self.individuals:
                if(i not in j.genes):
                    j.updateGenesWithPacket(i)

    def evaporate(self, amount=1):
        """Evaporar la cantidad de feromona/señal.

        Args:
            amount: Cantidad de feromona/señal a evaporar
        """
        self.alertLevel = max(self.alertLevel - amount, 0)

    def addFeromone(self, amount=1):
        """Agregar la cantidad de feromona/señal.

        Args:
            amount: Cantidad de feromona/señal a agregar
        """
        self.alertLevel = self.alertLevel + amount


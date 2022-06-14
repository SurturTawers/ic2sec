import random
from src.settings import *

class Individual:
    # El diccionario "genes" tiene la forma:
    # {
    #   packetID: [[packetID, probability], ..., [packetID, probability]],
    #   .
    #   .
    #   .
    #   packetID: [[packetID, probability], ..., [packetID, probability]]
    # }
    # packetID es el string resultante del hash (o lo que sea que se vaya a usar) de identificación de cada tipo de paquete
    def __init__(self, i=-1, g={}, e=0, f=0, fM=0):
        self.id = i
        self.genes = g
        self.energy = e
        self.fitness = f
        self.fitnessMemory = fM

    def __repr__(self):
        g = ""
        for i in self.genes:
            g = g + str(i) + ": " + str(self.genes[i]) + "\n"
        return f"""
ID: {str(self.id)}
Genes: {g}
Energy: {str(self.energy)}
Fitness: {str(self.fitness)}
"""

    def eatPacket(self, packet=None, packetAnt=None):
        """Alimentar a individuo con packet.

        Args:
            packet: El paquete parseado para alimentar a la población (def = None)
            packetAnt: El paquete parseado anteriormente (def = None)
        """
        # print(packetAnt)
        if(packetAnt == None or packetAnt not in self.genes.keys()):
            packetAnt = "*"
        fMarkov = self.genes[packetAnt]
        packets = self.choosePackets(fMarkov)
        if packet in packets or (packet not in self.genes.keys() and "*" in packets):
            self.fitness = self.fitness + 1

    def choosePackets(self, fMarkov=[]):
        """Elegir apuesta individuo.

        Args:
            fMarkov: Fila en la matriz de markov del agente, que corresponde al paquete anteriormente llegado

        Returns:
            packets: Paquetes a los cuales se le apuesta.
        """
        packets = []  # Se guardaran las mejores opciones
        #MARGEN_CHOOSE = 0.1
        max = [None, 0]
        for i in fMarkov:
            if max[1] <= i[1]:
                max = i
        packets.append(max[0])

        for i in fMarkov:
            if i[1] >= max[1]-(max[1]*MARGEN_CHOOSE) and max != i:
                packets.append(i[0])

        return packets

    def mutate2(self):
        """Mutar el individuo."""
        #mutacion = 0.05
        for i in self.genes.keys():
            rand = random.random()
            if rand <= MUTATION_RATE:
                n1 = random.randint(0, len(self.genes[i])-1)
                n2 = random.randint(0, len(self.genes[i])-1)
                temp = self.genes[i][n1][1]*0.5
                self.genes[i][n1][1] = self.genes[i][n1][1]-temp
                self.genes[i][n2][1] = self.genes[i][n2][1]+temp

    def mutate(self):
        """Mutar el individuo."""
        #mutacion = 0.05
        for i in self.genes.keys():
            rand = random.random()
            if rand <= MUTATION_RATE:
                n1 = random.randint(0, len(self.genes[i])-1)
                n2 = random.randint(0, len(self.genes[i])-1)
                temp = self.genes[i][n1][1]
                self.genes[i][n1][1] = self.genes[i][n2][1]
                self.genes[i][n2][1] = temp

    # mutacion es el porcentaje de mutacion para cada gen del individuo. Escogiendo
    # dos random se logra intercambiar las probabilidades de cada packet

    def updateGenesWithPacket(self, packet=None):
        """Actualizar los genes de los individuos para incluir el paquete 'packet', visto muchas veces.

        Args:
            packet: El paquete que se quiere agregar a los genes de la poblacion (def = None)
        """
        for i in self.genes:
            newPacketChance = round(self.genes[i][0][1] / 2, 2)
            newJchance = self.genes[i][0][1] - newPacketChance
            self.genes[i].append([packet, newPacketChance])
            self.genes[i][0][1] = newJchance
        # print(selfModel)

        self.genes[packet] = []
        geneLine = []
        m = 100
        for i in self.genes:
            val = random.randint(0, m)
            m = m - val
            geneLine.append([i, val / 100])
        geneLine[-1][1] = (val + m) / 100
        self.genes[packet] = geneLine
        #print("Post update:")
        # print(self)
        # input()

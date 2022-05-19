import copy
import time
import matplotlib.pyplot as plt

from Population import Population
from utils import *
from settings import *

TICKS = 0

class Controller():
    """
    In charge of controling and execution of the model.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.packetList = {} # Contador para tipos de paquetes, para actualizar los genes de los agentes y el comodín
        self.normal_pop = None
        self.reactive_pops = []
        self.populations = [] # Sum of normal_pop and reactive_pops.

    # def __setattr__(self, name, value):
        # """
        # Hook to update populations on change.
        # """
        # super().__setattr__(name, value)
        # if (name == 'reactive_pops' or name == "normal_pop") and self.normal_pop != None and len(self.normal_pop.individuals):
            # print(self.normal_pop)
            # print("se activo hook")
            # super().__setattr__('populations', self.reactive_pops.append(self.normal_pop))

    def check_end(self, packet):
        if(packet == ""):
            if self.verbose: print("Parece que se terminó el archivo")
            legend = []
            for i in self.populations:
                plt.plot(i.fitnessHistory)
                legend.append(i.type)
                # print(i.fitnessHistory)
            plt.title("Normalidad vs Ataque")
            plt.legend(legend)
            plt.savefig(SAVE_GRAPHS_DIR + time.ctime())
            # plt.show()
            # print(self.populations)
            # exit(0)
            return True
        return False


    def run(self):
        """
        Este es el ciclo de vida basico para el modelo, le falta la interaccion entre los 2+ modelos
        """

        print(f"INPUT_FILE is ", INPUT_FILE)
        current_file = open(INPUT_FILE, "rt")

        # Use TICKS global variable.
        global TICKS

        # Create initial pop. 
        self.normal_pop = Population()
        self.normal_pop.initializePop(INITIAL_POP_INDIVIDUAL_COUNT)
        self.normal_pop.repose = False
        self.populations.append(self.normal_pop)

        fitnessHistory = []
        lastPacket = None

        while(True):
            TICKS = TICKS + 1
            if(TICKS % 100 == 0):
                for i in self.populations:
                    if not i.repose:
                        if self.verbose: print(str(TICKS)+i.type)


            # Leemos y procesamos el siguiente paquete
            packet = parsePacket(current_file)
            if(packet in self.packetList):
                self.packetList[packet] = self.packetList[packet] + 1
            else:
                self.packetList[packet] = 1

            # Check if end of input.
            if self.check_end(packet):
                current_file.close()
                break

            for i in self.populations:
                # Alimentamos a el/los modelos
                i.feedPop(packet, lastPacket)
                if not i.repose:
                    i.timeActive = i.timeActive + 1
                # print(i.repose)
                # print(i.alertLevel)
                # print(i.timeActive)
                # Vemos si es necesario realizar cambio al modelo de ataque
                if (not i.repose) and i.alertLevel > ATTACK_THRESHOLD and i.timeActive >= 100:
                    # if ataqueModel == None:
                    if len(self.reactive_pops) == 0:
                        new_reactive_pop = Population(individuals=copy.deepcopy(
                            self.normal_pop.individuals), modelType="ataque")
                        new_reactive_pop.fitnessHistory = fitnessHistory

                        self.reactive_pops.append(new_reactive_pop)
                        self.populations.append(new_reactive_pop)

                    else:
                        for j in self.populations:
                            if j.repose:
                                j.alertLevel = 0
                                j.repose = False
                                j.timeActive = 0
                    i.repose = True
                    i.alertLevel = 0
                    i.timeActive = 0
                    if self.verbose: print("cambio")

            # Esto controla cada cuantas generaciones se realiza una cruza. (def = 1, osea en todas)
            if(not TICKS % CYCLES_TO_EVALUATE_POP):
                # print(TICKS)
                # print(selfModel)
                # input()
                for i in self.populations:
                    medianFitness = evaluatePop(i)
                    # print("Medianfitness", medianFitness)
                    # if ataqueModel == None:
                    if len(self.reactive_pops) == 0:
                        fitnessHistory.append(-1)
                    # Evaporamos la feromona de las poblaciones
                    i.evaporate(EVAPORATION_RATE)
                    i.fitnessHistory.append(medianFitness)

                for i in self.populations:
                    if not i.repose and i.timeActive >= 100:
                        # print("fitnessHistory", i.fitnessHistory)
                        if attack(i.fitnessHistory) and TICKS > CYCLES_TO_NEW_MEMORY*2:
                            if self.verbose: print("EN ATAQUE "+str(i.alertLevel) +
                                  " "+i.type+" "+str(i.timeActive))
                            i.addFeromone(ADDED_FEROMONE)

                # Realizamos la seleccion de padres
                for i in self.populations:
                    if not i.repose:
                        # print("cruza")
                        parentsSize = int(len(i.individuals)*(1-PERCENTAGE_ELITISM))*2
                        parents = i.selectParents(
                            parentsSize if parentsSize % 2 == 0 else parentsSize+1)
                        # Realizamos la cruza
                        new = []
                        for j in range(0, len(parents), 2):
                            h1 = crossIndividuals2(
                                parents[j].genes, parents[j + 1].genes)
                            #h2 = crossIndividuals2(parents[j+2].genes, parents[j + 3].genes)
                            h1.mutate2()
                            # h2.mutate()
                            new.append(h1)
                            # new.append(h2)
                        i.individuals = elitism(i.individuals, new)
                        i.memoryUpdate()
                        if((not TICKS % CYCLES_TO_NEW_MEMORY) and (TICKS != 0)):
                            i.memoryChange()
                    for j in i.individuals:
                        j.fitness = 0
                    if i.memory != None:
                        i.memory.fitness = 0

                    # Actualizamos la matriz de todos los agentes si hay un nuevo paquete que agregar a sus genes
                    i.checkDictionaryUpdate(self.packetList) # Esto lo comente ya que en el otro code, nunca llega a correr. - vcoopman

            lastPacket = packet

        # Retorna populations para que sea testeable.
        return self.populations


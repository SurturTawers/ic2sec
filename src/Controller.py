import copy
import os
from datetime import datetime
import matplotlib.pyplot as plt

from src.Population import Population
from src.utils import *
from src.settings import *

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
            # guardar plots por separado
            for i in self.populations:
                plt.plot(i.fitnessHistory)
                legend.append(i.type)
                # print(i.fitnessHistory)
            plt.title("Normalidad vs Ataque")
            plt.legend(legend)
            date = str(datetime.now())
            date = date.replace(" ", "_").replace(":", "-").replace(".", "-")
            plt.savefig(os.path.join(SAVE_GRAPHS_DIR,date))
            print(f"Plot saved in {os.path.join(SAVE_GRAPHS_DIR,date)}.png")
            #plt.show()
            #print(self.populations)
            # exit(0)
            return True
        return False

    """
    Ideas:  -poner tope de feromonas para ver cuales no se encuentran bajo "ataque" durante alguna fase
            -guardar snapshot de fitness antes de encontrarse un cambio en el tráfico (baja el fitness) y comparar la diferencia
                si disminuye la diferencia y pasa un umbral (sube el fitness): población reconoce el ataque. 
        
    """

    def run(self):
        """
        Este es el ciclo de vida basico para el modelo, le falta la interaccion entre los 2+ modelos
        """

        print(f"INPUT_FILE is ", INPUT_FILE)
        current_file = open(INPUT_FILE, "r")

        # Use TICKS global variable.
        global TICKS
        TICKS = 0

        # Create initial pop. 
        self.normal_pop = Population()
        self.normal_pop.initializePop(INITIAL_POP_INDIVIDUAL_COUNT)
        self.normal_pop.repose = False
        self.populations.append(self.normal_pop)

        fitnessHistory = []
        lastPacket = None
        lineas=0
        while(True):
            # if self.verbose: print(TICKS)
            TICKS = TICKS + 1
            if(TICKS % 100 == 0):
                for i in self.populations:
                    if not i.repose:
                        if self.verbose: print(str(TICKS)+" "+i.type)

            # Leemos y procesamos el siguiente paquete
            packet = parsePacket(current_file)
            # if self.verbose: print(packet)
            #lineas+=1
            #print("lineas: "+ str(lineas))
            if(packet in self.packetList):
                self.packetList[packet] = self.packetList[packet] + 1
            else:
                self.packetList[packet] = 1

            # Check if end of input.
            if self.check_end(packet):
                current_file.close()
                break
            """
            for i in self.populations:
                # Alimentamos a el/los modelos
                i.feedPop(packet, lastPacket)
                if not i.repose:
                    i.timeActive = i.timeActive + 1
                # print(i.repose)
                # print(i.alertLevel)
                # print(i.timeActive)

            reconocible = False
            index = -1
            # Verifica si alguno no tiene alerta
            for p in self.populations:
                index+=1
                if p.alertLevel < ATTACK_THRESHOLD:
                    reconocible = True
                    break

            if reconocible is False:
                new_reactive_pop = Population(individuals=copy.deepcopy(
                    self.normal_pop.individuals), modelType="ataque")
                new_reactive_pop.fitnessHistory = fitnessHistory

                self.reactive_pops.append(new_reactive_pop)
                self.populations.append(new_reactive_pop)
                print("Nueva población reactiva")
            else:
                #activar el index y desactivar los otros
                if self.populations[index].repose:
                    print(self.populations[index].type + " lo reconoce")
                    for j in self.populations:
                        if not j.repose:
                            j.alertLevel = 0
                            j.repose = True
                            j.timeActive = 0
                    self.populations[index].repose = False
                    self.populations[index].alertLevel = 0
                    self.populations[index].timeActive = 0
                    if self.verbose: print("cambio a: " + self.populations[index].type)
                else:
                    print(self.populations[index].type + " ya está activo")
            """
            """
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
                    #Modificar para verificar si no existe una población de ataque que reconoce este ataque
                    if len(self.reactive_pops) == 0:
                        #tipo = "ataque "+str(len(self.reactive_pops))
                        new_reactive_pop = Population(individuals=copy.deepcopy(
                            self.normal_pop.individuals), modelType="ataque")
                        new_reactive_pop.fitnessHistory = fitnessHistory

                        self.reactive_pops.append(new_reactive_pop)
                        self.populations.append(new_reactive_pop)
                        #print(len(self.reactive_pops))

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
            """
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
                    reconocible = False
                    index = -1
                    for p in self.populations:
                        index+=1
                        if p.repose:
                            #HACER ANALISIS MAS PROFUNDO DEL FITNESS PARA DECIDIR CUANDO ESTA BAJO ATAQUE O NO
                            alerta = attack(p.fitnessHistory)
                            print(str(alerta) + " " + p.type)
                            if not alerta:
                                reconocible = True
                                break

                    if reconocible is False:
                        num = "ataque " + str(len(self.reactive_pops)+1)
                        new_reactive_pop = Population(individuals=copy.deepcopy(
                            self.normal_pop.individuals), modelType=num)
                        new_reactive_pop.fitnessHistory = fitnessHistory

                        self.reactive_pops.append(new_reactive_pop)
                        self.populations.append(new_reactive_pop)
                        print("Nueva poblacion: " + num)
                        for j in self.populations:
                            if not j.repose:
                                j.alertLevel = 0
                                j.repose = True
                                j.timeActive = 0
                        self.populations[-1].repose = False
                        self.populations[-1].alertLevel = 0
                        self.populations[-1].timeActive = 0
                        if self.verbose: print("cambio a: " + self.populations[-1].type)
                    else:
                        for j in self.populations:
                            if not j.repose:
                                j.alertLevel = 0
                                j.repose = True
                                j.timeActive = 0
                        self.populations[index].repose = False
                        self.populations[index].alertLevel = 0
                        self.populations[index].timeActive = 0
                        if self.verbose: print("cambio a: " + self.populations[index].type)


            # Esto controla cada cuantas generaciones se realiza una cruza. (def = 1, osea en todas)
            if(not TICKS % CYCLES_TO_EVALUATE_POP):
                # print(TICKS)
                # print(selfModel)
                # input()
                for i in self.populations:
                    medianFitness = evaluatePop(i)
                    # print("Medianfitness "+str(i.type) , medianFitness)
                    # if ataqueModel == None:
                    if len(self.reactive_pops) == 0:
                        fitnessHistory.append(-1)
                    # Evaporamos la feromona de las poblaciones
                    i.evaporate(EVAPORATION_RATE)
                    i.fitnessHistory.append(medianFitness)

                for i in self.populations:
                    if not i.repose and i.timeActive >= 100:
                        # print("fitnessHistory", i.fitnessHistory)
                        if attack(i.fitnessHistory) and TICKS > CYCLES_TO_NEW_MEMORY * 2:
                            if self.verbose: print(i.type + " EN ATAQUE "+str(i.alertLevel) +
                                  " "+str(i.timeActive))
                            i.addFeromone(ADDED_FEROMONE)
                """
                for i in self.populations:
                    if i.timeActive >= 100:
                        # print("fitnessHistory", i.fitnessHistory)
                        if attack(i.fitnessHistory) and TICKS > CYCLES_TO_NEW_MEMORY * 2:
                            if self.verbose : print(i.type + " EN ATAQUE " + str(i.alertLevel) +
                                                   " " + str(i.timeActive))
                            if i.repose and i.alertLevel < ATTACK_THRESHOLD :i.addFeromone(ADDED_FEROMONE)
                            elif not i.repose: i.addFeromone(ADDED_FEROMONE)
                        elif not attack(i.fitnessHistory) and TICKS > CYCLES_TO_NEW_MEMORY * 2:
                            if i.repose:
                                print(i.type +" lo reconoce")
                                for j in self.populations:
                                    if not j.repose:
                                        j.alertLevel = 0
                                        j.repose = True
                                        j.timeActive = 0
                                i.repose = False
                                i.alertLevel = 0
                                i.timeActive = 0
                                if self.verbose: print("cambio a: " + i.type)
                            else:
                                print(i.type + " ya está activo")
                """

                # Realizamos la seleccion de padres
                for i in self.populations:
                    if not i.repose:
                        #GUARDAR REFERENCIA A CUAL POBLACION ESTA ACTIVA EVITANDO ITERAR POR TODA LA POBLACIÓN
                        #print("cruzando: " + i.type)
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


# OPERATIONAL SETTINGS
SAVE_GRAPHS_DIR = "graphs/"
INPUT_FILE = "data/1000_1000.txt"
#Ambos archivos dejan con fitness de individuos = 0
#fix pq se cae el programa
#INPUT_FILE = "data/udp_parsed.txt"
#INPUT_FILE = "data/normal+ataque_parsed.txt"

# EVOLUTION SETTINGS 
INDIVIDUAL_COUNT = 0  # Contador de individuos para ID
MARGEN_CHOOSE = 0.1  # Margen de choosePackets() del individuo
MUTATION_RATE = 0.05  # Porcentaje de mutacion del inviduo
INITIAL_POP_INDIVIDUAL_COUNT = 100  # Cantidad de individuos, poblacion inicial
PACKETS_UMBRAL = 100  # umbral de minimos paquetes para agregarlos a diccionario
PERCENTAGE_ELITISM = 0.4  # Porcentaje de elitismo a realizar
CYCLES_TO_NEW_MEMORY = 10  # Cantidad de ciclos para actualizar celula de memoria
CYCLES_TO_EVALUATE_POP = 10  # Cantidad de paquetes para evaluar la población
ATTACK_THRESHOLD = 30  # Cantidad de feromona para declarar un ataque
EVAPORATION_RATE = 1  # Velocidad de evaporacion de la feromona
ADDED_FEROMONE = 10  # Cantidad de feromona a agregar en cada evaluacion que indica ataque
FITNESS_CHAGE_ATTACK = 0.3  # Porcentaje de baja del fitness para detectar un ataque
GRAPH = "elite"

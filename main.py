# instalar: pip install scikit-fuzzy
import pygame
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define las variables de entrada
distancia = ctrl.Antecedent(np.arange(0, 101, 1), 'Distancia')
angulo = ctrl.Antecedent(np.arange(-90, 91, 1), 'Ángulo')

# Define las variables de salida
movimiento = ctrl.Consequent(np.arange(-1, 1.01, 0.01), 'Movimiento')

# Definir las funciones de membresía
distancia['cerca'] = fuzz.trimf(distancia.universe, [0, 20, 40])
distancia['medio'] = fuzz.trimf(distancia.universe, [30, 50, 70])
distancia['lejos'] = fuzz.trimf(distancia.universe, [60, 80, 100])

angulo['derecha'] = fuzz.trimf(angulo.universe, [-90, -45, 0])
angulo['centro'] = fuzz.trimf(angulo.universe, [-30, 0, 30])
angulo['izquierda'] = fuzz.trimf(angulo.universe, [0, 45, 90])

movimiento['izquierda'] = fuzz.trimf(movimiento.universe, [-1, -0.5, 0])
movimiento['centro'] = fuzz.trimf(movimiento.universe, [-0.2, 0, 0.2])
movimiento['derecha'] = fuzz.trimf(movimiento.universe, [0, 0.5, 1])

# Definir las reglas difusas
regla1 = ctrl.Rule(distancia['cerca'] & angulo['derecha'], movimiento['izquierda'])
regla2 = ctrl.Rule(distancia['cerca'] & angulo['centro'], movimiento['centro'])
regla3 = ctrl.Rule(distancia['cerca'] & angulo['izquierda'], movimiento['derecha'])
# Agregar más reglas según sea necesario

# Crear el sistema de control
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])

# Crear la simulación del sistema de control
robot = ctrl.ControlSystemSimulation(sistema_control)

# Simular el sistema para obtener el valor de movimiento
robot.input['Distancia'] = 30  # Asegúrate de usar la misma etiqueta
robot.input['Ángulo'] = -10  # Asegúrate de usar la misma etiqueta
robot.compute()

# Obtener la salida
movimiento_robot = robot.output['Movimiento']
print("Movimiento del robot:", movimiento_robot)

sistema_control = ctrl.ControlSystem([regla1, regla2, regla3])
robot = ctrl.ControlSystemSimulation(sistema_control)

# Inicializar Pygame
pygame.init()

# Define los colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de Fútbol")

# Coordenadas del robot y la pelota (inicialmente en el centro)
robot_x = screen_width // 2
robot_y = screen_height // 2
pelota_x = screen_width // 2
pelota_y = screen_height // 2

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcula la distancia entre el robot y la pelota
    distancia_entre_robot_y_pelota = np.sqrt((robot_x - pelota_x) ** 2 + (robot_y - pelota_y) ** 2)

    # Calcula el ángulo entre el robot y la pelota
    angulo_entre_robot_y_pelota = np.degrees(np.arctan2(pelota_y - robot_y, pelota_x - robot_x))

    # Simula el sistema de control para obtener el movimiento del robot
    robot.input['Distancia'] = distancia_entre_robot_y_pelota
    robot.input['Ángulo'] = angulo_entre_robot_y_pelota
    robot.compute()

    # Aplica el movimiento del robot
    robot_x += int(movimiento_robot * 10)  # Multiplica por un valor para ajustar la velocidad

    # Dibuja la pantalla
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [robot_x, robot_y, 20, 20])  # Dibuja el robot
    pygame.draw.circle(screen, WHITE, (pelota_x, pelota_y), 10)  # Dibuja la pelota

    pygame.display.flip()
    clock.tick(30)  # Ajusta la velocidad de actualización de la pantalla

pygame.quit()
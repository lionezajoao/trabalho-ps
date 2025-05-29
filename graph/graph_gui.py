# graph_gui.py
import pygame
import networkx as nx
import random

# Inicialização do Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pandemic (Gráfico)")
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()
FPS = 30 # Limitar a taxa de frames

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CITY_COLOR = (200, 200, 200)
CONNECTION_COLOR = (100, 100, 100)
PLAYER_COLOR = (0, 255, 0)
RESEARCH_STATION_COLOR = (0, 128, 255) # Azul mais claro

# Dicionário para mapear nomes de cidades para posições na tela (DEFINIÇÃO MANUAL)
city_positions = {
    "Atlanta": (150, 250),
    "Chicago": (150, 150),
    "Miami": (250, 300),
    "Nova York": (300, 120),
    "Dallas": (100, 350),
    "Los Angeles": (50, 400),
    "São Francisco": (50, 300),
    "Montreal": (250, 80),
    "Washington": (250, 180),
    "Londres": (450, 80),
    "Madri": (400, 180),
    "Paris": (450, 150),
    "Milão": (500, 120),
    "Roma": (550, 180),
    "Argel": (450, 250),
    "Cairo": (550, 250),
    "Istambul": (550, 120),
    "Moscou": (650, 80),
    "São Petersburgo": (600, 50),
    "Bagdá": (650, 180),
    "Teerã": (700, 120),
    "Carachi": (700, 250),
    "Mumbai": (700, 320),
    "Deli": (750, 200),
    "Calcutá": (750, 300),
    "Bangcoc": (750, 380),
    "Pequim": (750, 50),
    "Seul": (700, 50),
    "Tóquio": (700, 100),
    "Xangai": (700, 150),
    "Hong Kong": (750, 100),
    "Taipei": (700, 20),
    "Manila": (750, 150),
    "Sydney": (100, 500),
    "Jacarta": (750, 450),
    "Ho Chi Minh": (700, 400)
}

# Superfícies de texto para os nomes das cidades (renderizadas uma vez)
city_name_surfaces = {}

def get_disease_color(color):
    if color == "vermelho":
        return RED
    elif color == "azul":
        return BLUE
    elif color == "amarelo":
        return YELLOW
    elif color == "preto":
        return BLACK
    return (128, 128, 128) # Cinza para cores desconhecidas

def draw_game(screen, board, player):
    screen.fill(WHITE)

    # Desenhar conexões
    for city_name, city in board.cities.items():
        pos1 = city_positions.get(city_name)
        if pos1:
            for connection in city.connections:
                pos2 = city_positions.get(connection.name)
                if pos2:
                    pygame.draw.line(screen, CONNECTION_COLOR, pos1, pos2, 2)

    # Desenhar cidades
    for city_name, city in board.cities.items():
        pos = city_positions.get(city_name)
        if pos:
            city_color_to_draw = CITY_COLOR
            if player and city == player.location:
                city_color_to_draw = PLAYER_COLOR

            pygame.draw.circle(screen, city_color_to_draw, pos, 18)
            # Blit a superfície de texto pré-renderizada
            if city_name in city_name_surfaces:
                text_rect = city_name_surfaces[city_name].get_rect(center=pos)
                screen.blit(city_name_surfaces[city_name], text_rect)

            y_offset = 20
            for color, level in city.infection_levels.items():
                if level > 0:
                    infection_text = font.render(f"{color}: {level}", True, get_disease_color(color), WHITE)
                    screen.blit(infection_text, (pos[0] - 30, pos[1] + y_offset))
                    y_offset += 18
            if city.has_research_station:
                pygame.draw.rect(screen, RESEARCH_STATION_COLOR, (pos[0] - 12, pos[1] - 30, 24, 8))

    # Exibir informações do jogo
    info_text = font.render(f"Surtos: {board.outbreak_count}", True, BLACK)
    screen.blit(info_text, (10, 10))
    if player:
        actions_text = font.render(f"Ações: {player.actions_left}", True, BLACK)
        screen.blit(actions_text, (10, 30))

    pygame.display.flip()
    clock.tick(FPS) # Limitar a taxa de frames

def initialize_city_positions(board):
    # As posições são definidas diretamente no dicionário city_positions
    for city_name in board.cities:
        city_name_surfaces[city_name] = font.render(city_name, True, BLACK)
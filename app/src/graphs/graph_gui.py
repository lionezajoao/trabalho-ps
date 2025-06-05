import pygame

# Inicialização do Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pandemic (Gráfico)")
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 72) # Fonte maior para vitória/derrota
clock = pygame.time.Clock()
FPS = 30 # Limitar a taxa de frames

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 128) # Azul escuro
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CITY_COLOR = (200, 200, 200)
CONNECTION_COLOR = WHITE  # Conexões brancas
PLAYER_COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)] # Verde, Vermelho, Azul, Amarelo
RESEARCH_STATION_COLOR = (0, 128, 255) # Azul mais claro

# Dicionário para mapear nomes de cidades para posições na tela
city_positions = {
    # Azul (4)
    "Atlanta": (150, 250),
    "Chicago": (150, 150),
    "Nova York": (350, 100),
    "Londres": (400, 180),
    # Amarelo (4)
    "Miami": (300, 350),
    "Cidade do México": (100, 450),
    "São Paulo": (350, 480),
    "Los Angeles": (50, 350),
    # Preto (4)
    "Cairo": (550, 350),
    "Istambul": (500, 200),
    "Bagdá": (600, 480),
    "Riade": (600, 300),
    # Vermelho (4)
    "Pequim": (700,300),
    "Seul": (550, 100),
    "Tóquio": (650, 200),
    "Xangai": (700, 150)
}

# Superfícies de texto para os nomes das cidades (renderizadas uma vez)
city_name_surfaces = {}

def get_disease_color(color):
    global RED, BLUE, YELLOW, BLACK # Indica que estamos usando as variáveis globais
    if color == "vermelho":
        return RED
    elif color == "azul":
        return BLUE
    elif color == "amarelo":
        return YELLOW
    elif color == "preto":
        return BLACK
    return (128, 128, 128) # Cinza para cores desconhecidas

def draw_game(screen, board, current_player):
    screen.fill(BLUE_DARK)  # Fundo azul escuro

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
            # Cor do nó igual à cor da doença da cidade
            city_color_to_draw = get_disease_color(city.color)
            # Destacar jogador
            if current_player and city == current_player.location:
                city_color_to_draw = PLAYER_COLORS[board.players.index(current_player) % len(PLAYER_COLORS)]
            elif board.players:
                for i, player in enumerate(board.players):
                    if city == player.location:
                        city_color_to_draw = PLAYER_COLORS[i % len(PLAYER_COLORS)]
                        break

            pygame.draw.circle(screen, city_color_to_draw, pos, 18)
            
            # Draw city name with background for better visibility
            if city_name in city_name_surfaces:
                text_surface = city_name_surfaces[city_name]
                text_rect = text_surface.get_rect(center=pos)
                # Draw background rectangle
                bg_rect = text_rect.inflate(10, 5)  # Make background slightly larger than text
                pygame.draw.rect(screen, BLUE_DARK, bg_rect)
                screen.blit(text_surface, text_rect)

            y_offset = 20
            for color, level in city.infection_levels.items():
                if level > 0:
                    # Draw infection level with background for better visibility
                    infection_text = font.render(f"{color}: {level}", True, WHITE)
                    text_rect = infection_text.get_rect(topleft=(pos[0] - 30, pos[1] + y_offset))
                    # Draw background rectangle
                    bg_rect = text_rect.inflate(10, 5)  # Make background slightly larger than text
                    pygame.draw.rect(screen, BLUE_DARK, bg_rect)
                    screen.blit(infection_text, text_rect)
                    y_offset += 18
            if city.has_research_station:
                pygame.draw.rect(screen, RESEARCH_STATION_COLOR, (pos[0] - 12, pos[1] - 30, 24, 8))

    # Exibir informações do jogo
    info_text = font.render(f"Surtos: {board.outbreak_count}", True, WHITE)
    screen.blit(info_text, (10, 10))
    if current_player:
        actions_text = font.render(f"Ações de {current_player.name}: {current_player.actions_left}", True, WHITE)
        screen.blit(actions_text, (10, 30))

    pygame.display.flip()
    clock.tick(FPS)

def display_win_message(screen):
    win_text = large_font.render("Vitória!", True, BLUE_DARK)
    text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(win_text, text_rect)
    pygame.display.flip()

def display_lose_message(screen):
    lose_text = large_font.render("Derrota!", True, RED)
    text_rect = lose_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(lose_text, text_rect)
    pygame.display.flip()

def initialize_city_positions(board):
    city_name_surfaces.clear()
    for city_name in board.cities:
        if city_name in city_positions:
            # Create text with white color
            city_name_surfaces[city_name] = font.render(city_name, True, WHITE)
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import sys # Importa o módulo sys para sair do jogo
import time
import pygame
from src.board import Board
from src.player import Player
from src.graphs.graph_gui import screen, draw_game, initialize_city_positions, display_win_message, display_lose_message, font, BLUE_DARK, WHITE
from src.graphs.start_screen import tela_inicial
from src.graphs.game_screen import game_screen

# --- NOVO: Tela inicial visual ---
def tela_inicial():
    clock = pygame.time.Clock()
    input_boxes = []
    num_players = 2
    player_names = ["" for _ in range(4)]
    active_box = None
    state = "choose_num_players"
    selected_players = 2
    start_button_rect = pygame.Rect(300, 500, 200, 50)
    button_y = 160  # Posição Y dos botões (mais abaixo do texto)
    button_spacing = 80  # Espaçamento horizontal entre os botões
    
    def draw():
        screen.fill(BLUE_DARK)
        title = font.render("Zomdemic - Escolha jogadores", True, WHITE)
        screen.blit(title, (220, 40))
        # Escolha número de jogadores
        txt = font.render("Número de jogadores:", True, WHITE)
        screen.blit(txt, (100, 120))
        for i in range(1, 5):
            color = (0,255,0) if i == selected_players else WHITE
            pygame.draw.rect(screen, color, (100 + button_spacing*i, button_y, 50, 40), 2)
            n_txt = font.render(str(i), True, color)
            screen.blit(n_txt, (115 + button_spacing*i, button_y + 10))
        # Campos de nome
        for i in range(selected_players):
            label = font.render(f"Nome do Jogador {i+1}:", True, WHITE)
            screen.blit(label, (100, 250 + i*70))
            box_rect = pygame.Rect(320, 245 + i*70, 250, 40)
            pygame.draw.rect(screen, WHITE, box_rect, 2)
            name_txt = font.render(player_names[i], True, WHITE)
            screen.blit(name_txt, (330, 255 + i*70))
            if active_box == i:
                pygame.draw.rect(screen, (0,255,0), box_rect, 2)
        # Botão iniciar
        pygame.draw.rect(screen, (0,255,0), start_button_rect)
        start_txt = font.render("Iniciar Jogo", True, BLUE_DARK)
        screen.blit(start_txt, (start_button_rect.x+30, start_button_rect.y+10))
        pygame.display.flip()

    while True:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Selecionar número de jogadores
                for i in range(1, 5):
                    if 100 + button_spacing*i <= mx <= 150 + button_spacing*i and 160 <= my <= 200:
                        selected_players = i
                        if active_box is not None and active_box >= selected_players:
                            active_box = None
                # Selecionar campo de nome
                for i in range(selected_players):
                    if 320 <= mx <= 570 and 245 + i*70 <= my <= 285 + i*70:
                        active_box = i
                        break
                else:
                    active_box = None
                # Botão iniciar
                if start_button_rect.collidepoint(mx, my):
                    if all(player_names[i].strip() for i in range(selected_players)):
                        return selected_players, player_names[:selected_players]
            if event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    player_names[active_box] = player_names[active_box][:-1]
                elif event.key == pygame.K_RETURN:
                    active_box = None
                elif len(player_names[active_box]) < 16 and event.unicode.isprintable():
                    player_names[active_box] += event.unicode
        clock.tick(30)

if __name__ == "__main__":
    while True:
        num_players, player_names = tela_inicial()
        board = Board()
        players = []
        for i in range(num_players):
            player = Player(player_names[i], board.get_city("Atlanta"))
            players.append(player)
            board.players.append(player)
        initialize_city_positions(board)
        current_player_index = 0
        # Chama a tela principal do jogo
        game_won, game_over = game_screen(board, players, current_player_index)
        if game_won:
            display_win_message(screen)
            time.sleep(2)
        elif game_over:
            display_lose_message(screen)
            time.sleep(2)
        break

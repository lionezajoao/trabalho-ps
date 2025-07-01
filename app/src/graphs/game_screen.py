import sys
import pygame
from src.graphs.graph_gui import screen, draw_game, font, WHITE, BLUE_DARK

def game_screen(board, players, current_player_index):
    running = True
    game_over = False
    game_won = False
    clock = pygame.time.Clock()
    event_log = []

    menu_x = 820
    menu_y = 50
    menu_width = 250
    button_height = 60
    button_spacing = 20

    actions = [
        ("Mover", "move"),
        ("Tratar", "treat"),
        ("Construir", "build"),
        ("Passar Turno", "pass"),
    ]

    menu_state = "actions"  # "actions", "move", "treat"
    move_options = []
    treat_options = ["vermelho", "azul", "amarelo", "preto"]

    def draw_action_menu(selected=None):
        pygame.draw.rect(screen, BLUE_DARK, (menu_x, 0, menu_width, 600))
        title = font.render("Ações", True, WHITE)
        screen.blit(title, (menu_x + 70, 10))
        buttons = []
        for i, (label, _) in enumerate(actions):
            btn_rect = pygame.Rect(menu_x + 20, menu_y + i * (button_height + button_spacing), menu_width - 40, button_height)
            color = (0, 200, 0) if selected == i else (40, 40, 40)
            pygame.draw.rect(screen, color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, btn_rect, 2, border_radius=8)
            txt = font.render(label, True, WHITE)
            screen.blit(txt, (btn_rect.x + 20, btn_rect.y + 18))
            buttons.append(btn_rect)
        return buttons

    def draw_move_menu(connections):
        pygame.draw.rect(screen, BLUE_DARK, (menu_x, 0, menu_width, 600))
        title = font.render("Mover para:", True, WHITE)
        screen.blit(title, (menu_x + 50, 10))
        buttons = []
        for i, city in enumerate(connections):
            btn_rect = pygame.Rect(menu_x + 20, menu_y + i * (button_height + button_spacing), menu_width - 40, button_height)
            pygame.draw.rect(screen, (40, 40, 40), btn_rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, btn_rect, 2, border_radius=8)
            txt = font.render(city.name, True, WHITE)
            screen.blit(txt, (btn_rect.x + 20, btn_rect.y + 18))
            buttons.append((btn_rect, city))
        # Botão de cancelar
        cancel_rect = pygame.Rect(menu_x + 20, menu_y + len(connections) * (button_height + button_spacing), menu_width - 40, button_height)
        pygame.draw.rect(screen, (200, 0, 0), cancel_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, cancel_rect, 2, border_radius=8)
        cancel_txt = font.render("Cancelar", True, WHITE)
        screen.blit(cancel_txt, (cancel_rect.x + 20, cancel_rect.y + 18))
        buttons.append((cancel_rect, None))
        return buttons

    def draw_treat_menu():
        pygame.draw.rect(screen, BLUE_DARK, (menu_x, 0, menu_width, 600))
        title = font.render("Tratar doença:", True, WHITE)
        screen.blit(title, (menu_x + 40, 10))
        buttons = []
        for i, color in enumerate(treat_options):
            btn_rect = pygame.Rect(menu_x + 20, menu_y + i * (button_height + button_spacing), menu_width - 40, button_height)
            pygame.draw.rect(screen, (40, 40, 40), btn_rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, btn_rect, 2, border_radius=8)
            txt = font.render(color.capitalize(), True, WHITE)
            screen.blit(txt, (btn_rect.x + 20, btn_rect.y + 18))
            buttons.append((btn_rect, color))
        # Botão de cancelar
        cancel_rect = pygame.Rect(menu_x + 20, menu_y + len(treat_options) * (button_height + button_spacing), menu_width - 40, button_height)
        pygame.draw.rect(screen, (200, 0, 0), cancel_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, cancel_rect, 2, border_radius=8)
        cancel_txt = font.render("Cancelar", True, WHITE)
        screen.blit(cancel_txt, (cancel_rect.x + 20, cancel_rect.y + 18))
        buttons.append((cancel_rect, None))
        return buttons

    def draw_event_log():
        log_y = menu_y + 5 * (button_height + button_spacing)
        log_title = font.render("Log do Jogo:", True, WHITE)
        screen.blit(log_title, (menu_x + 20, log_y))
        log_y += 25
        for msg in event_log[-10:]:
            log_line = font.render(msg, True, WHITE)
            screen.blit(log_line, (menu_x + 20, log_y))
            log_y += 20

    while running:
        draw_game(screen, board, players[current_player_index])
        player = players[current_player_index]

        if menu_state == "actions":
            buttons = draw_action_menu()
        elif menu_state == "move":
            move_options = player.location.connections
            buttons = draw_move_menu(move_options)
        elif menu_state == "treat":
            buttons = draw_treat_menu()
        draw_event_log()
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if menu_state == "actions":
                    for idx, btn_rect in enumerate(buttons):
                        if btn_rect.collidepoint(mx, my):
                            action = actions[idx][1]
                            if action == "move":
                                menu_state = "move"
                            elif action == "treat":
                                menu_state = "treat"
                            elif action == "build":
                                if not player.location.has_research_station:
                                    player.build_research_station()
                                    event_log.append(f"{player.name} construiu centro de pesquisa em {player.location.name}.")
                                else:
                                    event_log.append(f"Já existe centro de pesquisa em {player.location.name}.")
                            elif action == "pass":
                                event_log.append(f"{player.name} passou o turno.")
                                # Fase de infecção
                                board.infect_cities(board.infection_rate)
                                # Próximo jogador
                                current_player_index = (current_player_index + 1) % len(players)
                                players[current_player_index].reset_actions()
                                event_log.append(f"Agora é a vez de {players[current_player_index].name}.")
                            break
                elif menu_state == "move":
                    for btn_rect, city in buttons:
                        if btn_rect.collidepoint(mx, my):
                            if city is None:
                                menu_state = "actions"
                            else:
                                if player.actions_left > 0 and city in player.location.connections:
                                    player.move(city)
                                    event_log.append(f"{player.name} moveu para {city.name}.")
                                else:
                                    event_log.append(f"Movimento inválido.")
                                menu_state = "actions"
                            break
                elif menu_state == "treat":
                    for btn_rect, color in buttons:
                        if btn_rect.collidepoint(mx, my):
                            if color is None:
                                menu_state = "actions"
                            else:
                                if player.actions_left > 0 and player.location.infection_levels[color] > 0:
                                    player.treat(color)
                                    event_log.append(f"{player.name} tratou {color} em {player.location.name}.")
                                else:
                                    event_log.append(f"Não há {color} para tratar ou sem ações.")
                                menu_state = "actions"
                            break

        if board.check_win_prototype():
            game_won = True
            running = False
        if board.check_game_over():
            game_over = True
            running = False

    return game_won, game_over

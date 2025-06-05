import sys
import pygame
import time
from src.graphs.graph_gui import screen, draw_game, font, WHITE, BLUE_DARK

def game_screen(board, players, current_player_index):
    running = True
    game_over = False
    game_won = False
    action_popup = False
    action_selected = None
    popup_rect = pygame.Rect(200, 180, 400, 240)
    action_buttons = [
        ("Mover", (popup_rect.x+50, popup_rect.y+60)),
        ("Tratar", (popup_rect.x+250, popup_rect.y+60)),
        ("Construir", (popup_rect.x+50, popup_rect.y+140)),
        ("Passar Turno", (popup_rect.x+250, popup_rect.y+140)),
    ]
    clock = pygame.time.Clock()

    def draw_popup():
        pygame.draw.rect(screen, WHITE, popup_rect, border_radius=12)
        title = font.render("Escolha uma ação:", True, BLUE_DARK)
        screen.blit(title, (popup_rect.x+100, popup_rect.y+20))
        for i, (label, (bx, by)) in enumerate(action_buttons):
            btn_rect = pygame.Rect(bx, by, 120, 50)
            pygame.draw.rect(screen, BLUE_DARK, btn_rect, border_radius=8)
            txt = font.render(label, True, WHITE)
            screen.blit(txt, (bx+10, by+15))
        if action_selected is not None:
            msg = font.render(f"{action_selected} selecionado!", True, BLUE_DARK)
            screen.blit(msg, (popup_rect.x+80, popup_rect.y+200))

    while running:
        draw_game(screen, board, players[current_player_index])
        if not action_popup:
            action_popup = True
            action_selected = None
        if action_popup:
            draw_popup()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if action_popup and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, (label, (bx, by)) in enumerate(action_buttons):
                    btn_rect = pygame.Rect(bx, by, 120, 50)
                    if btn_rect.collidepoint(mx, my):
                        action_selected = label
                        # Placeholder: só mostra mensagem e fecha popup após 1s
                        pygame.display.flip()
                        time.sleep(1)
                        action_popup = False
                        if label == "Passar Turno":
                            current_player_index = (current_player_index + 1) % len(players)
                        break
        clock.tick(30)
        # Placeholder: vitória/derrota automática
        if board.check_win_prototype():
            game_won = True
            running = False
        if board.check_game_over():
            game_over = True
            running = False
    return game_won, game_over 
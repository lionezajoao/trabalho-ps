import sys
import pygame
from app.src.ui.graph_gui import screen, font, BLUE_DARK, WHITE

def tela_inicial():
    clock = pygame.time.Clock()
    player_names = ["" for _ in range(4)]
    active_box = None
    selected_players = 2
    
    # Obter dimensões da tela para centralização
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Posições centralizadas
    title_x = screen_width // 2 - 200  # Centralize o título (ajustado para o texto completo)
    players_text_x = screen_width // 2 - 120  # Centralize o texto "Número de jogadores"
    names_label_x = screen_width // 2 - 120  # Centralize labels dos nomes
    names_input_x = screen_width // 2 - 125   # Centralize campos de entrada
    start_button_x = screen_width // 2 - 100  # Centralize botão iniciar
    
    start_button_rect = pygame.Rect(start_button_x, 420, 200, 50)  # Ajustado para nova posição dos campos
    button_y = 115  # Posição Y dos botões (alinhado com o desenho)
    button_spacing = 50  # Espaçamento entre os botões

    def draw():
        screen.fill(BLUE_DARK)
        
        # Título centralizado
        title = font.render("Zomdemic - Escolha jogadores", True, WHITE)
        screen.blit(title, (title_x, 40))
        
        # Texto "Número de jogadores" e botões na mesma linha
        txt = font.render("Número de jogadores:", True, WHITE)
        txt_width = txt.get_width()
        screen.blit(txt, (players_text_x, 120))
        
        # Botões de número logo após o texto, na mesma linha
        buttons_x_start = players_text_x + txt_width + 20  # 20px de espaço após o texto
        for i in range(1, 5):
            color = (0,255,0) if i == selected_players else WHITE
            btn_x = buttons_x_start + button_spacing * (i - 1)
            pygame.draw.rect(screen, color, (btn_x, 115, 35, 30), 2)  # Y=115 para alinhar com o texto
            n_txt = font.render(str(i), True, color)
            screen.blit(n_txt, (btn_x + 12, 120))
        # Campos de nome centralizados (logo abaixo do seletor)
        names_start_y = 180  # Posição inicial dos campos de nome (mais próximo do seletor)
        for i in range(selected_players):
            # Label acima da caixa de texto
            label = font.render(f"Nome do Jogador {i+1}:", True, WHITE)
            label_x = names_input_x  # Alinhar com a caixa de texto
            screen.blit(label, (label_x, names_start_y + i*70 - 20))  # 20px acima da caixa
            
            # Caixa de texto
            box_rect = pygame.Rect(names_input_x, names_start_y + i*70, 250, 40)
            pygame.draw.rect(screen, WHITE, box_rect, 2)
            name_txt = font.render(player_names[i], True, WHITE)
            screen.blit(name_txt, (names_input_x + 10, names_start_y + i*70 + 10))
            if active_box == i:
                pygame.draw.rect(screen, (0,255,0), box_rect, 2)
        
        # Botão iniciar centralizado
        pygame.draw.rect(screen, (0,255,0), start_button_rect)
        start_txt = font.render("Iniciar Jogo", True, BLUE_DARK)
        screen.blit(start_txt, (start_button_rect.x+50, start_button_rect.y+15))
        pygame.display.flip()

    while True:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Selecionar número de jogadores (botões horizontais)
                txt = font.render("Número de jogadores:", True, WHITE)
                txt_width = txt.get_width()
                buttons_x_start = players_text_x + txt_width + 20
                
                for i in range(1, 5):
                    btn_x = buttons_x_start + button_spacing * (i - 1)
                    if btn_x <= mx <= btn_x + 35 and button_y <= my <= button_y + 30:
                        selected_players = i
                        if active_box is not None and active_box >= selected_players:
                            active_box = None
                # Selecionar campo de nome (posição atualizada para novo layout)
                names_start_y = 180
                for i in range(selected_players):
                    # Área de clique ajustada para novo espaçamento de 70px entre campos
                    if names_input_x <= mx <= names_input_x + 250 and names_start_y + i*70 <= my <= names_start_y + i*70 + 40:
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
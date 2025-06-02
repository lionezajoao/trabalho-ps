# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import sys # Importa o módulo sys para sair do jogo
import time

from src.board import Board
from src.player import Player
from src.graph_gui import pygame, screen, draw_game, initialize_city_positions, city_positions, display_win_message, display_lose_message

if __name__ == "__main__":
    while True: # Loop para permitir jogar novamente
        # *** RECOMEÇAR O JOGO DO ZERO ***
        board = Board()
        num_players = 0
        while num_players < 1 or num_players > 4:
            try:
                num_players = int(input("Digite o número de jogadores (1-4): "))
            except ValueError:
                print("Entrada inválida. Digite um número entre 1 e 4.")

        players = []
        for i in range(num_players):
            name = input(f"Digite o nome do Jogador {i+1}: ")
            player = Player(name, board.get_city("Atlanta"))
            players.append(player)
            board.players.append(player) # Adiciona o jogador à lista do board

        initialize_city_positions(board) # Chamada APÓS a criação dos jogadores

        current_player_index = 0
        running = True
        game_over = False
        game_won = False

        while running:
            current_player = players[current_player_index]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break # Sai do loop do jogo atual

            if not game_over and not game_won:
                draw_game(screen, board, current_player) # Passa o jogador atual para a função de desenho

                if current_player.actions_left > 0:
                    print(f"\nTurno de {current_player.name}. Você está em {current_player.location.name}. Ações restantes: {current_player.actions_left}")
                    print("Escolha uma ação (tecle no terminal e pressione Enter):")
                    print("1. Mover")
                    print("2. Tratar Doença")
                    print("3. Construir Centro de Pesquisa")
                    print("4. Encerrar Turno")
                    choice = input("Ação: ")

                    if choice == "1":
                        print("Conectado a:", [c.name for c in current_player.location.connections])
                        destino = input("Para onde deseja ir? ")
                        destino_city = board.get_city(destino)
                        if destino_city and destino_city in current_player.location.connections:
                            current_player.move(destino_city)
                        elif not board.get_city(destino):
                            print("Cidade inválida.")
                        else:
                            print("Você não pode se mover para essa cidade.")
                    elif choice == "2":
                        color_to_treat = input("Qual cor de doença deseja tratar (vermelho, azul, amarelo, preto)? ").lower()
                        if color_to_treat in ["vermelho", "azul", "amarelo", "preto"]:
                            current_player.treat(color_to_treat)
                        else:
                            print("Cor inválida.")
                    elif choice == "3":
                        current_player.build_research_station()
                    elif choice == "4":
                        current_player.actions_left = 0 # Força o fim do turno
                    else:
                        print("Opção inválida.")
                else:
                    print(f"\nFim do turno de {current_player.name}. Pressione ENTER para avançar para a fase de infecção.")
                    input() # Aguarda o jogador pressionar Enter
                    # *** VERIFICAR CONDIÇÃO DE VITÓRIA AQUI ***
                    if board.check_win_prototype():
                        game_won = True
                        running = False
                        continue

                    print("\n--- Fase de Infecção ---")
                    board.infect_cities(board.infection_rate)
                    time.sleep(0.5)
                    if board.check_game_over():
                        game_over = True
                        running = False
                    else:
                        current_player.reset_actions()
                        current_player_index = (current_player_index + 1) % len(players) # Próximo jogador

            elif game_won:
                display_win_message(screen)
                break # Sai do loop do jogo atual
            elif game_over:
                display_lose_message(screen)
                break # Sai do loop do jogo atual

        # Após o loop do jogo terminar (vitória ou derrota)
        while True:
            play_again = input("Jogar novamente? (s/n): ").lower()
            if play_again == 's':
                break # Sai do loop de jogar novamente e inicia um novo jogo
            elif play_again == 'n':
                pygame.quit()
                sys.exit() # Sai completamente do programa
            else:
                print("Entrada inválida. Digite 's' para sim ou 'n' para não.")

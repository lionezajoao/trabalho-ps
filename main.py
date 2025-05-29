# main.py
from .graph.graph_gui import pygame, screen, draw_game, initialize_city_positions, city_positions
from .core.models.tabuleiro import Board
from .core.models.jogador import Player
import time

def main():
    board = Board()
    player = Player("Pinho", board.get_city("Atlanta"))
    initialize_city_positions(board) # As posições são definidas diretamente em graph_gui.py

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_game(screen, board, player)

        if player.actions_left > 0:
            print(f"\nVocê está em {player.location.name}. Ações restantes: {player.actions_left}")
            print("Escolha uma ação (tecle no terminal e pressione Enter):")
            print("1. Mover")
            print("2. Tratar Doença")
            print("3. Construir Centro de Pesquisa")
            print("4. Encerrar Turno")
            choice = input("Ação: ")

            if choice == "1":
                print("Conectado a:", [c.name for c in player.location.connections])
                destino = input("Para onde deseja ir? ")
                destino_city = board.get_city(destino)
                if destino_city and destino_city in player.location.connections:
                    player.move(destino_city)
                elif not board.get_city(destino):
                    print("Cidade inválida.")
                else:
                    print("Você não pode se mover para essa cidade.")
            elif choice == "2":
                player.treat()
            elif choice == "3":
                player.build_research_station()
            elif choice == "4":
                player.actions_left = 0 # Força o fim do turno
            else:
                print("Opção inválida.")
        else:
            print("\nPressione ENTER para avançar para a fase de infecção.")
            input() # Aguarda o jogador pressionar Enter
            print("\n--- Fase de Infecção ---")
            board.infect_cities(board.infection_rate)
            time.sleep(0.5)
            if not board.check_game_over():
                player.reset_actions()
            else:
                print("O jogo terminou.")
                running = False

        if board.check_game_over():
            running = False
            print("O jogo terminou.")

    pygame.quit()

if __name__ == "__main__":
    main()
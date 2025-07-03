# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import sys # Importa o módulo sys para sair do jogo
import time
import pygame
from app.src.classes.partida import Partida
from app.src.classes.enums import StatusPartida
from app.src.ui.graph_gui import screen, draw_game, initialize_city_positions, display_win_message, display_lose_message, font, BLUE_DARK, WHITE
from app.src.ui.start_screen import tela_inicial
from app.src.ui.game_screen import game_screen

if __name__ == "__main__":
    while True:
        num_players, player_names = tela_inicial()
        
        # Criar partida com os nomes dos jogadores
        partida = Partida(player_names)
        partida.iniciar()
        
        # Configurar interface gráfica (manter compatibilidade)
        board = partida.tabuleiro  # Para compatibilidade com código gráfico existente
        players = partida.jogadores  # Para compatibilidade com código gráfico existente
        
        # Adaptar os objetos para compatibilidade com a interface gráfica
        for i, player in enumerate(players):
            # Mapear novos atributos para os antigos
            player.name = player.nome
            player.location = player.localizacao
            player.actions_left = partida.obter_acoes_restantes()
            
            # Criar funções de compatibilidade usando partial ou lambdas
            def create_move_func(p, partida_ref):
                def move(cidade):
                    partida_ref.processar_turno_jogador("mover", destino=cidade)
                    p.location = p.localizacao  # Atualizar referência
                    p.actions_left = partida_ref.obter_acoes_restantes()
                return move
            
            def create_treat_func(p, partida_ref):
                def treat(cor_nome):
                    from src.classes.enums import CorDoenca
                    cor_map = {
                        "vermelho": CorDoenca.VERMELHO,
                        "azul": CorDoenca.AZUL, 
                        "amarelo": CorDoenca.AMARELO,
                        "preto": CorDoenca.PRETO
                    }
                    if cor_nome in cor_map:
                        partida_ref.processar_turno_jogador("tratar", cor=cor_map[cor_nome])
                        p.actions_left = partida_ref.obter_acoes_restantes()
                return treat
            
            def create_build_func(p, partida_ref):
                def build_research_station():
                    partida_ref.processar_turno_jogador("construir")
                    p.location.has_research_station = p.localizacao.tem_base
                    p.actions_left = partida_ref.obter_acoes_restantes()
                return build_research_station
            
            def create_reset_func(p, partida_ref):
                def reset_actions():
                    # Esta função será chamada mas o controle real está na partida
                    p.actions_left = partida_ref.obter_acoes_restantes()
                return reset_actions
            
            player.move = create_move_func(player, partida)
            player.treat = create_treat_func(player, partida)
            player.build_research_station = create_build_func(player, partida)
            player.reset_actions = create_reset_func(player, partida)
        
        # Adaptar tabuleiro para compatibilidade
        board.cities = {cidade.nome: cidade for cidade in board.cidades}
        board.players = players
        board.outbreak_count = board.marcador_surtos
        board.infection_rate = board.taxa_infeccao
        
        # Adicionar método de infecção para compatibilidade
        def infect_cities(rate):
            board.espalhar_doenca()
            # Atualizar infection_levels nas cidades após infecção
            for cidade in board.cidades:
                if cidade.cor in cidade.cubos_doenca:
                    cidade.infection_levels[cidade.cor.value] = cidade.cubos_doenca[cidade.cor]
        
        board.infect_cities = infect_cities
        
        # Adaptar cidades para compatibilidade
        for cidade in board.cidades:
            cidade.name = cidade.nome
            cidade.color = cidade.cor.value
            cidade.connections = cidade.conexoes
            cidade.has_research_station = cidade.tem_base
            # Mapear cubos_doenca para infection_levels
            cidade.infection_levels = {
                "vermelho": cidade.cubos_doenca.get(cidade.cor, 0) if cidade.cor.value == "vermelho" else 0,
                "azul": cidade.cubos_doenca.get(cidade.cor, 0) if cidade.cor.value == "azul" else 0,
                "amarelo": cidade.cubos_doenca.get(cidade.cor, 0) if cidade.cor.value == "amarelo" else 0,
                "preto": cidade.cubos_doenca.get(cidade.cor, 0) if cidade.cor.value == "preto" else 0,
            }
            # Corrigir infecção da própria cor da cidade
            if cidade.cor in cidade.cubos_doenca:
                cidade.infection_levels[cidade.cor.value] = cidade.cubos_doenca[cidade.cor]
        
        # Adicionar métodos de compatibilidade ao board
        def get_city(name):
            return board.cities.get(name)
        
        def check_win_prototype():
            return board.verificar_vitoria_prototipo()
        
        def check_game_over():
            return board.verificar_derrota_surtos()
        
        def check_victory():
            return board.verificar_vitoria_completa()
        
        board.get_city = get_city
        board.check_win_prototype = check_win_prototype
        board.check_game_over = check_game_over
        board.check_victory = check_victory
        
        # Adicionar referência à partida para as ações do jogo
        board.partida = partida
        
        initialize_city_positions(board)
        current_player_index = partida.indice_jogador_atual
        
        # Chama a tela principal do jogo
        game_won, game_over = game_screen(board, players, current_player_index)
        
        if game_won:
            display_win_message(screen)
            time.sleep(2)
        elif game_over:
            display_lose_message(screen)
            time.sleep(2)
        break

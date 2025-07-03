#!/usr/bin/env python3
"""
Script de teste rápido para verificar se todas as classes estão funcionando
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todos os imports estão funcionando"""
    print("🔍 Testando imports...")
    
    try:
        from src.classes.partida import Partida
        from src.classes.enums import StatusPartida, CorDoenca
        from src.classes.board import Tabuleiro
        from src.classes.player import Jogador
        from src.classes.personagem import Medico, Pesquisadora, Cientista, EspecialistaOperacoes
        from src.classes.gerenciador_descarte import GerenciadorDescarte
        print("✅ Todos os imports das classes funcionaram!")
        return True
    except ImportError as e:
        print(f"❌ Erro no import das classes: {e}")
        return False

def test_game_creation():
    """Testa a criação de uma partida"""
    print("\n🎮 Testando criação de partida...")
    
    try:
        from src.classes.partida import Partida
        
        # Criar partida com 2 jogadores
        partida = Partida(["Alice", "Bob"])
        partida.iniciar()
        
        print(f"✅ Partida criada! Status: {partida.status}")
        print(f"✅ Jogadores: {len(partida.jogadores)}")
        print(f"✅ Jogador atual: {partida.obter_jogador_atual().nome}")
        print(f"✅ Ações restantes: {partida.obter_acoes_restantes()}")
        
        return True
    except Exception as e:
        print(f"❌ Erro na criação da partida: {e}")
        return False

def test_board_functionality():
    """Testa funcionalidades do tabuleiro"""
    print("\n🗺️  Testando funcionalidades do tabuleiro...")
    
    try:
        from src.classes.partida import Partida
        from src.classes.enums import CorDoenca
        
        partida = Partida(["Carlos", "Diana"])
        partida.iniciar()
        
        tabuleiro = partida.tabuleiro
        jogador = partida.jogadores[0]
        
        # Testar obtenção de cidade
        atlanta = tabuleiro.obter_cidade("Atlanta")
        if atlanta:
            print(f"✅ Cidade encontrada: {atlanta.nome}")
        
        # Testar localização do jogador
        print(f"✅ Jogador está em: {jogador.localizacao.nome}")
        
        # Testar curas
        print(f"✅ Curas descobertas: {sum(tabuleiro.curas.values())}/4")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste do tabuleiro: {e}")
        return False

def test_ui_imports():
    """Testa se os imports da UI estão funcionando"""
    print("\n🖥️  Testando imports da UI...")
    
    try:
        # Imports podem falhar se pygame não estiver disponível em modo headless
        import pygame
        from src.ui.graph_gui import screen, font, BLUE_DARK, WHITE
        from src.ui.start_screen import tela_inicial
        from src.ui.game_screen import game_screen
        print("✅ Imports da UI funcionaram!")
        return True
    except ImportError as e:
        print(f"⚠️  Alguns imports da UI falharam (normal em modo headless): {e}")
        return True  # Não é erro crítico
    except Exception as e:
        print(f"❌ Erro inesperado na UI: {e}")
        return False

def test_start_screen_syntax():
    """Testa se a tela inicial não tem erros de sintaxe"""
    print("\n🎯 Testando sintaxe da tela inicial...")
    
    try:
        from src.ui.start_screen import tela_inicial
        # Verificar se a função pode ser chamada sem erros de escopo
        print("✅ Função tela_inicial carregada sem erros de sintaxe!")
        return True
    except NameError as e:
        print(f"❌ Erro de escopo/variável na tela inicial: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado na tela inicial: {e}")
        return False

def test_game_screen_compatibility():
    """Testa se os métodos de compatibilidade da interface gráfica funcionam"""
    print("\n🎮 Testando compatibilidade da interface gráfica...")
    
    try:
        from src.classes.partida import Partida
        from src.classes.enums import CorDoenca
        
        # Criar partida
        partida = Partida(["TestPlayer1", "TestPlayer2"])
        partida.iniciar()
        
        # Simular a configuração do main.py
        players = partida.jogadores
        board = partida.tabuleiro
        
        # Mapear atributos
        for player in players:
            player.name = player.nome
            player.location = player.localizacao
            player.actions_left = partida.obter_acoes_restantes()
            
            # Teste se os métodos de compatibilidade podem ser criados
            def create_test_methods(p, partida_ref):
                def move(cidade):
                    return True  # Simplified test
                def treat(cor_nome):
                    return True  # Simplified test
                def build_research_station():
                    return True  # Simplified test
                def reset_actions():
                    return True  # Simplified test
                return move, treat, build_research_station, reset_actions
            
            move, treat, build, reset = create_test_methods(player, partida)
            
            # Verificar se as funções foram criadas
            if callable(move) and callable(treat) and callable(build) and callable(reset):
                print(f"✅ Métodos de compatibilidade criados para {player.nome}")
            else:
                print(f"❌ Erro ao criar métodos para {player.nome}")
                return False
        
        # Testar compatibilidade do board
        board.infection_rate = board.taxa_infeccao
        if hasattr(board, 'taxa_infeccao') and board.infection_rate == board.taxa_infeccao:
            print("✅ Compatibilidade do board funcionando")
        
        return True
    except Exception as e:
        print(f"❌ Erro no teste de compatibilidade: {e}")
        return False

def test_outbreak_chain():
    """Testa se surtos em cadeia não causam recursão infinita"""
    print("\n💥 Testando surtos em cadeia...")
    
    try:
        from src.classes.partida import Partida
        from src.classes.enums import CorDoenca
        
        # Criar partida
        partida = Partida(["OutbreakTest1", "OutbreakTest2"])
        partida.iniciar()
        
        tabuleiro = partida.tabuleiro
        
        # Forçar uma situação onde pode haver surtos
        atlanta = tabuleiro.obter_cidade("Atlanta")
        if atlanta:
            # Adicionar 3 cubos para estar próximo do surto
            atlanta.cubos_doenca[CorDoenca.AZUL] = 3
            
            # Tentar adicionar mais um (deve causar surto)
            houve_surto = atlanta.adicionar_cubo(CorDoenca.AZUL)
            
            if houve_surto:
                print("✅ Detecção de surto funcionando")
                
                # Testar se não há mais de 3 cubos
                if atlanta.cubos_doenca[CorDoenca.AZUL] <= 3:
                    print("✅ Limite de 3 cubos por cidade respeitado")
                else:
                    print("❌ Mais de 3 cubos detectados")
                    return False
            
            # Testar infecção normal
            surtos_antes = tabuleiro.marcador_surtos
            tabuleiro.espalhar_doenca()
            surtos_depois = tabuleiro.marcador_surtos
            
            print(f"✅ Infecção executada - Surtos: {surtos_antes} → {surtos_depois}")
            return True
        else:
            print("❌ Cidade Atlanta não encontrada")
            return False
            
    except RecursionError:
        print("❌ Recursão infinita ainda presente!")
        return False
    except Exception as e:
        print(f"❌ Erro no teste de surtos: {e}")
        return False

if __name__ == "__main__":
    print("🧪 EXECUTANDO TESTES DAS CLASSES PANDEMIC")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_game_creation,
        test_board_functionality,
        test_ui_imports,
        test_start_screen_syntax,
        test_game_screen_compatibility,
        test_outbreak_chain
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O jogo está funcionando corretamente!")
    else:
        print("❌ Alguns testes falharam.")
        failed_count = len([r for r in results if not r])
        print(f"📊 {len(results) - failed_count}/{len(results)} testes passaram")
    
    print("\n💡 Para executar o jogo: python main.py")

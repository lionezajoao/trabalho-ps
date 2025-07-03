from abc import ABC, abstractmethod
from collections import deque
from .enums import TipoCartaJogador, CorDoenca

class Carta(ABC):
    """Classe abstrata base para todas as cartas"""
    pass

class CartaJogador(Carta):
    """Carta do baralho do jogador"""
    
    def __init__(self, tipo: TipoCartaJogador, cidade=None):
        self.tipo = tipo
        self.cidade = cidade

class CartaInfeccao(Carta):
    """Carta do baralho de infecção"""
    
    def __init__(self, cidade, cor: CorDoenca):
        self.cidade = cidade
        self.cor = cor

class CartaEvento(CartaJogador):
    """Carta de evento especial"""
    
    def __init__(self, descricao: str):
        super().__init__(TipoCartaJogador.EVENTO)
        self.descricao = descricao
    
    def ativar(self, partida):
        """Ativa o efeito da carta de evento"""
        print(f"Ativando evento: {self.descricao}")
        # Implementar efeitos específicos dos eventos aqui

class CartaEpidemia(CartaJogador):
    """Carta de epidemia"""
    
    def __init__(self):
        super().__init__(TipoCartaJogador.EPIDEMIA)
    
    def ativar_epidemia(self, partida):
        """Ativa o efeito da epidemia"""
        print("EPIDEMIA! Aumentando taxa de infecção e embaralhando descarte")
        # 1. Aumentar taxa de infecção
        if partida.tabuleiro.taxa_infeccao < 4:
            partida.tabuleiro.taxa_infeccao += 1
        
        # 2. Infectar cidade do fundo do baralho
        if partida.tabuleiro.baralho_infeccao.cartas:
            carta_fundo = partida.tabuleiro.baralho_infeccao.cartas[-1]
            partida.tabuleiro.baralho_infeccao.cartas.remove(carta_fundo)
            cidade = carta_fundo.cidade
            
            # Adicionar 3 cubos da cor da cidade
            for _ in range(3):
                cidade.adicionar_cubo(cidade.cor)
            
            partida.tabuleiro.gerenciador_descarte.descartar_infeccao(carta_fundo)
        
        # 3. Embaralhar descarte e colocar em cima do baralho
        import random
        descarte_infeccao = partida.tabuleiro.gerenciador_descarte.limpar_descarte_infeccao()
        random.shuffle(descarte_infeccao)
        partida.tabuleiro.baralho_infeccao.cartas = (descarte_infeccao + 
                                                     list(partida.tabuleiro.baralho_infeccao.cartas))
        partida.tabuleiro.baralho_infeccao.cartas = deque(partida.tabuleiro.baralho_infeccao.cartas)

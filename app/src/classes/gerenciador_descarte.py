from typing import List
from .baralho import Baralho
from .cartas import CartaJogador, CartaInfeccao

class GerenciadorDescarte:
    """Gerencia o descarte de cartas do jogador e de infecção"""
    
    def __init__(self):
        self.descarte_jogador: List[CartaJogador] = []
        self.descarte_infeccao: List[CartaInfeccao] = []
    
    def descartar_jogador(self, carta: CartaJogador):
        """Descarta uma carta do jogador"""
        self.descarte_jogador.append(carta)
    
    def descartar_infeccao(self, carta: CartaInfeccao):
        """Descarta uma carta de infecção"""
        self.descarte_infeccao.append(carta)
    
    def obter_descarte_jogador(self) -> List[CartaJogador]:
        """Retorna a pilha de descarte do jogador"""
        return self.descarte_jogador.copy()
    
    def obter_descarte_infeccao(self) -> List[CartaInfeccao]:
        """Retorna a pilha de descarte de infecção"""
        return self.descarte_infeccao.copy()
    
    def limpar_descarte_jogador(self):
        """Limpa o descarte do jogador"""
        cartas = self.descarte_jogador.copy()
        self.descarte_jogador.clear()
        return cartas
    
    def limpar_descarte_infeccao(self):
        """Limpa o descarte de infecção"""
        cartas = self.descarte_infeccao.copy()
        self.descarte_infeccao.clear()
        return cartas
    
    def tamanho_descarte_jogador(self) -> int:
        """Retorna o tamanho do descarte do jogador"""
        return len(self.descarte_jogador)
    
    def tamanho_descarte_infeccao(self) -> int:
        """Retorna o tamanho do descarte de infecção"""
        return len(self.descarte_infeccao)

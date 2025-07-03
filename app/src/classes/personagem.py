from abc import ABC
from .habilidades import (IHabilidadeEspecial, HabilidadeMedico, 
                           HabilidadePesquisadora, HabilidadeCientista, 
                           HabilidadeOperacoes)

class Personagem(ABC):
    """Classe abstrata base para personagens"""
    
    def __init__(self, nome: str, habilidade: IHabilidadeEspecial):
        self.nome = nome
        self.habilidade = habilidade
    
    def usar_habilidade(self, jogador, partida):
        """Usa a habilidade especial do personagem"""
        self.habilidade.executar(jogador, partida)

class Medico(Personagem):
    """Personagem Médico"""
    
    def __init__(self):
        super().__init__("Médico", HabilidadeMedico())

class Pesquisadora(Personagem):
    """Personagem Pesquisadora"""
    
    def __init__(self):
        super().__init__("Pesquisadora", HabilidadePesquisadora())

class Cientista(Personagem):
    """Personagem Cientista"""
    
    def __init__(self):
        super().__init__("Cientista", HabilidadeCientista())

class EspecialistaOperacoes(Personagem):
    """Personagem Especialista em Operações"""
    
    def __init__(self):
        super().__init__("Especialista em Operações", HabilidadeOperacoes())

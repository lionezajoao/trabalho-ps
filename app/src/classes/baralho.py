import random
from typing import TypeVar, Generic, List
from collections import deque

T = TypeVar('T')

class Baralho(Generic[T]):
    """Classe genérica para representar um baralho de cartas"""
    
    def __init__(self):
        self.cartas: deque[T] = deque()
    
    def embaralhar(self):
        """Embaralha as cartas do baralho"""
        cartas_lista = list(self.cartas)
        random.shuffle(cartas_lista)
        self.cartas = deque(cartas_lista)
    
    def sacar(self) -> T:
        """Saca uma carta do topo do baralho"""
        if self.cartas:
            return self.cartas.popleft()
        raise IndexError("Baralho vazio")
    
    def descartar(self, carta: T):
        """Descarta uma carta (adiciona ao final do baralho)"""
        self.cartas.append(carta)
    
    def adicionar_carta(self, carta: T):
        """Adiciona uma carta ao baralho"""
        self.cartas.append(carta)
    
    def adicionar_cartas(self, cartas: List[T]):
        """Adiciona múltiplas cartas ao baralho"""
        self.cartas.extend(cartas)
    
    def esta_vazio(self) -> bool:
        """Verifica se o baralho está vazio"""
        return len(self.cartas) == 0
    
    def tamanho(self) -> int:
        """Retorna o número de cartas no baralho"""
        return len(self.cartas)
    
    def ver_topo(self) -> T:
        """Visualiza a carta do topo sem removê-la"""
        if self.cartas:
            return self.cartas[0]
        raise IndexError("Baralho vazio")

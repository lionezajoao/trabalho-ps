from typing import List, Dict
from .enums import CorDoenca

class Cidade:
    def __init__(self, nome: str, cor: CorDoenca):
        self.nome = nome
        self.cor = cor
        self.cubos_doenca: Dict[CorDoenca, int] = {
            CorDoenca.VERMELHO: 0,
            CorDoenca.AZUL: 0,
            CorDoenca.AMARELO: 0,
            CorDoenca.PRETO: 0
        }
        self.conexoes: List['Cidade'] = []
        self.tem_base = False

    def adicionar_cubo(self, cor: CorDoenca) -> bool:
        """
        Adiciona um cubo de doença da cor especificada.
        Retorna True se houve surto (mais de 3 cubos), False caso contrário.
        """
        if self.cubos_doenca[cor] < 3:
            self.cubos_doenca[cor] += 1
            return False  # Não houve surto
        else:
            # Já há 3 cubos - houve surto mas não adiciona mais cubos
            # Máximo é 3 cubos por cor por cidade
            return True

    def remover_cubo(self, cor: CorDoenca) -> bool:
        """
        Remove um cubo de doença da cor especificada.
        Retorna True se conseguiu remover, False se não havia cubos.
        """
        if self.cubos_doenca[cor] > 0:
            self.cubos_doenca[cor] -= 1
            return True
        return False

    def esta_conectada_com(self, cidade: 'Cidade') -> bool:
        """Verifica se esta cidade está conectada com outra cidade"""
        return cidade in self.conexoes

    def adicionar_conexao(self, cidade: 'Cidade'):
        """Adiciona uma conexão bidirecional entre cidades"""
        if cidade not in self.conexoes:
            self.conexoes.append(cidade)
            cidade.conexoes.append(self)

    def total_cubos_doenca(self) -> int:
        """Retorna o total de cubos de doença na cidade"""
        return sum(self.cubos_doenca.values())

    def tem_doenca(self, cor: CorDoenca) -> bool:
        """Verifica se a cidade tem doença da cor especificada"""
        return self.cubos_doenca[cor] > 0

    def __str__(self):
        return f"{self.nome} ({self.cor.value}), Cubos: {self.cubos_doenca}, Base: {self.tem_base}"

# Manter compatibilidade com código existente
City = Cidade
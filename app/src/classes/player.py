from typing import List
from .cartas import CartaJogador
from .personagem import Personagem
from .city import Cidade
from .enums import CorDoenca

class Jogador:
    def __init__(self, nome: str, personagem: Personagem, localizacao: Cidade):
        """
        Inicializa um novo jogador.

        Args:
            nome (str): O nome do jogador.
            personagem (Personagem): O personagem do jogador.
            localizacao (Cidade): A cidade inicial do jogador.
        """
        self.nome = nome
        self.personagem = personagem
        self.mao: List[CartaJogador] = []
        self.localizacao = localizacao

    def realizar_acao(self, acao: str, destino: Cidade = None, cor: CorDoenca = None):
        """
        Realiza uma ação do jogador.

        Args:
            acao (str): Tipo de ação ('mover', 'tratar', 'construir', 'habilidade')
            destino (Cidade, optional): Cidade de destino para movimento
            cor (CorDoenca, optional): Cor da doença para tratamento
        """
        if acao == "mover" and destino:
            self.mover(destino)
        elif acao == "tratar" and cor:
            self.tratar(cor)
        elif acao == "construir":
            self.construir_base()
        elif acao == "habilidade":
            self.usar_habilidade_especial()
        else:
            print(f"Ação inválida ou parâmetros insuficientes: {acao}")

    def mover(self, cidade: Cidade):
        """
        Move o jogador para uma cidade conectada.

        Args:
            cidade (Cidade): A cidade para a qual o jogador deseja se mover.
        """
        if cidade in self.localizacao.conexoes:
            print(f"{self.nome} se moveu de {self.localizacao.nome} para {cidade.nome}.")
            self.atualizar_localizacao(cidade)
        else:
            print(f"{self.nome} não pode se mover para {cidade.nome}. Não estão conectados.")

    def atualizar_localizacao(self, destino: Cidade):
        """Atualiza a localização do jogador"""
        self.localizacao = destino

    def tratar(self, cor: CorDoenca):
        """
        Tenta tratar uma doença na cidade atual.

        Args:
            cor (CorDoenca): A cor da doença a ser tratada.
        """
        if self.localizacao.tem_doenca(cor):
            if self.localizacao.tem_base:
                # Com base de pesquisa, remove todos os cubos da cor
                self.localizacao.cubos_doenca[cor] = 0
                print(f"{self.nome} curou completamente a doença {cor.value} em {self.localizacao.nome} (centro de pesquisa).")
            else:
                # Sem base, remove apenas um cubo
                self.localizacao.remover_cubo(cor)
                print(f"{self.nome} tratou a doença {cor.value} em {self.localizacao.nome}.")
        else:
            print(f"Não há infecção de {cor.value} para tratar em {self.localizacao.nome}.")

    def construir_base(self, partida=None):
        """
        Constrói um centro de pesquisa na cidade atual.
        Requer carta da cidade atual (exceto para Especialista em Operações)
        """
        if self.localizacao.tem_base:
            print(f"Já existe um centro de pesquisa em {self.localizacao.nome}.")
            return False
        
        # Especialista em Operações pode construir sem carta
        if self.personagem.nome == "Especialista em Operações":
            self.localizacao.tem_base = True
            print(f"{self.nome} (Especialista em Operações) construiu um centro de pesquisa em {self.localizacao.nome}.")
            return True
        
        # Outros personagens precisam da carta da cidade
        carta_da_cidade = None
        for carta in self.mao:
            if (hasattr(carta, 'cidade') and carta.cidade and 
                carta.cidade.nome == self.localizacao.nome):
                carta_da_cidade = carta
                break
        
        if carta_da_cidade:
            # Descartar a carta e construir a base
            self.mao.remove(carta_da_cidade)
            if partida:
                partida.gerenciador_descarte.descartar_jogador(carta_da_cidade)
            self.localizacao.tem_base = True
            print(f"{self.nome} construiu um centro de pesquisa em {self.localizacao.nome}.")
            return True
        else:
            print(f"{self.nome} precisa da carta de {self.localizacao.nome} para construir uma base aqui.")
            return False

    def compartilhar_carta(self, destinatario: 'Jogador', carta: CartaJogador):
        """
        Compartilha uma carta com outro jogador.
        
        Args:
            destinatario (Jogador): Jogador que receberá a carta
            carta (CartaJogador): Carta a ser compartilhada
        """
        if carta in self.mao and destinatario.localizacao == self.localizacao:
            # Verificar se pode compartilhar (deve estar na mesma cidade que a carta representa, 
            # ou usar habilidade especial da Pesquisadora)
            pode_compartilhar = False
            
            if hasattr(carta, 'cidade') and carta.cidade:
                # Carta de cidade - deve estar na cidade representada
                pode_compartilhar = (self.localizacao == carta.cidade or 
                                   self.personagem.nome == "Pesquisadora")
            else:
                # Carta de evento - Pesquisadora pode compartilhar qualquer carta
                pode_compartilhar = self.personagem.nome == "Pesquisadora"
            
            if pode_compartilhar:
                self.mao.remove(carta)
                destinatario.mao.append(carta)
                print(f"{self.nome} compartilhou a carta {carta.cidade.nome if hasattr(carta, 'cidade') and carta.cidade else 'especial'} com {destinatario.nome}")
                return True
            else:
                print("Não é possível compartilhar essa carta (deve estar na cidade representada ou ser Pesquisadora)")
                return False
        else:
            print("Não é possível compartilhar a carta (carta não encontrada ou jogadores em locais diferentes)")
            return False

    def descartar_carta(self, carta: CartaJogador, partida=None):
        """Descarta uma carta da mão do jogador"""
        if carta in self.mao:
            self.mao.remove(carta)
            if partida:
                partida.gerenciador_descarte.descartar_jogador(carta)
            print(f"{self.nome} descartou uma carta.")
            return True
        else:
            print(f"{self.nome} não possui essa carta.")
            return False

    def usar_habilidade_especial(self):
        """Usa a habilidade especial do personagem"""
        print(f"{self.nome} está usando a habilidade especial do {self.personagem.nome}")
        # A habilidade será executada pela partida com contexto completo

    def adicionar_carta(self, carta: CartaJogador):
        """Adiciona uma carta à mão do jogador"""
        self.mao.append(carta)
        print(f"{self.nome} recebeu uma carta.")

    def tem_cartas_demais(self) -> bool:
        """Verifica se o jogador tem mais de 7 cartas na mão"""
        return len(self.mao) > 7

    def __str__(self):
        return f"Jogador: {self.nome} ({self.personagem.nome}), Localização: {self.localizacao.nome}, Cartas: {len(self.mao)}"

# Manter compatibilidade com código existente
Player = Jogador
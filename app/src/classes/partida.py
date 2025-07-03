from typing import List
from .enums import StatusPartida
from .board import Tabuleiro
from .player import Jogador
from .turno import Turno
from .personagem import Medico, Pesquisadora, Cientista, EspecialistaOperacoes
from .cartas import CartaEpidemia
from .gerenciador_descarte import GerenciadorDescarte
import random

class Partida:
    """Classe principal que gerencia a partida do jogo"""
    
    def __init__(self, nomes_jogadores: List[str]):
        self.status = StatusPartida.EM_ANDAMENTO
        self.tabuleiro = Tabuleiro()
        self.jogadores: List[Jogador] = []
        self.turno_atual: Turno = None
        self.indice_jogador_atual = 0
        
        self._criar_jogadores(nomes_jogadores)
        self._distribuir_cartas_iniciais()
        self.turno_atual = Turno(self.jogadores[0])
    
    @property
    def gerenciador_descarte(self) -> GerenciadorDescarte:
        """Acesso ao gerenciador de descarte"""
        return self.tabuleiro.gerenciador_descarte

    def _criar_jogadores(self, nomes: List[str]):
        """Cria os jogadores com personagens aleatórios"""
        personagens_disponiveis = [Medico(), Pesquisadora(), Cientista(), EspecialistaOperacoes()]
        random.shuffle(personagens_disponiveis)
        
        atlanta = self.tabuleiro.obter_cidade("Atlanta")
        atlanta.tem_base = True  # Atlanta começa com base de pesquisa
        
        for i, nome in enumerate(nomes):
            personagem = personagens_disponiveis[i % len(personagens_disponiveis)]
            jogador = Jogador(nome, personagem, atlanta)
            self.jogadores.append(jogador)

    def _distribuir_cartas_iniciais(self):
        """Distribui cartas iniciais para os jogadores"""
        # Cada jogador recebe 2-4 cartas dependendo do número de jogadores
        num_cartas = {2: 4, 3: 3, 4: 2}
        cartas_por_jogador = num_cartas.get(len(self.jogadores), 2)
        
        for jogador in self.jogadores:
            for _ in range(cartas_por_jogador):
                if not self.tabuleiro.baralho_jogador.esta_vazio():
                    carta = self.tabuleiro.baralho_jogador.sacar()
                    jogador.adicionar_carta(carta)

    def iniciar(self):
        """Inicia a partida"""
        print(f"Iniciando partida com {len(self.jogadores)} jogadores")
        print(f"Jogadores: {', '.join([j.nome + ' (' + j.personagem.nome + ')' for j in self.jogadores])}")
        self.status = StatusPartida.EM_ANDAMENTO

    def processar_turno_jogador(self, acao: str, **kwargs):
        """Processa uma ação do jogador no turno atual"""
        if not self.turno_atual.pode_realizar_acao():
            print("Não é possível realizar ações nesta fase do turno")
            return False
        
        jogador_atual = self.turno_atual.jogador_atual
        
        if acao == "mover":
            destino = kwargs.get('destino')
            if destino:
                self.tabuleiro.mover_jogador(jogador_atual, destino)
                self.turno_atual.decrementar_acoes()
        
        elif acao == "tratar":
            cor = kwargs.get('cor')
            if cor:
                self.tabuleiro.tratar_doenca(jogador_atual, cor)
                self.turno_atual.decrementar_acoes()
        
        elif acao == "construir":
            if self.tabuleiro.construir_base(jogador_atual, self):
                self.turno_atual.decrementar_acoes()
        
        elif acao == "descobrir_cura":
            cor = kwargs.get('cor')
            if cor:
                if self.tabuleiro.descobrir_cura(jogador_atual, cor):
                    self.turno_atual.decrementar_acoes()
        
        elif acao == "compartilhar":
            destinatario = kwargs.get('destinatario')
            carta = kwargs.get('carta')
            if destinatario and carta:
                if jogador_atual.compartilhar_carta(destinatario, carta):
                    self.turno_atual.decrementar_acoes()
        
        elif acao == "habilidade":
            jogador_atual.personagem.usar_habilidade(jogador_atual, self)
            self.turno_atual.decrementar_acoes()
        
        elif acao == "passar_turno":
            self.turno_atual.acoes_restantes = 0
            self.turno_atual.proxima_fase()
        
        return True

    def finalizar_turno(self):
        """Finaliza o turno atual e passa para o próximo jogador"""
        # Fase de compra de cartas
        if self.turno_atual.fase_atual.value == "compra":
            jogador_atual = self.turno_atual.jogador_atual
            for _ in range(2):  # Comprar 2 cartas
                if not self.tabuleiro.baralho_jogador.esta_vazio():
                    carta = self.tabuleiro.baralho_jogador.sacar()
                    if isinstance(carta, CartaEpidemia):
                        carta.ativar_epidemia(self)
                        self.gerenciador_descarte.descartar_jogador(carta)
                    else:
                        jogador_atual.adicionar_carta(carta)
                        
                    # Verificar se jogador tem cartas demais
                    if jogador_atual.tem_cartas_demais():
                        print(f"{jogador_atual.nome} deve descartar cartas (máximo 7)")
            
            self.turno_atual.proxima_fase()
        
        # Fase de infecção
        if self.turno_atual.fase_atual.value == "infeccao":
            self.tabuleiro.espalhar_doenca()
            
            # Passar para o próximo jogador
            self.indice_jogador_atual = (self.indice_jogador_atual + 1) % len(self.jogadores)
            proximo_jogador = self.jogadores[self.indice_jogador_atual]
            self.turno_atual.reiniciar_turno(proximo_jogador)

    def verificar_condicoes(self) -> StatusPartida:
        """Verifica as condições de vitória e derrota"""
        # Verificar derrota por surtos
        if self.tabuleiro.verificar_derrota_surtos():
            self.status = StatusPartida.DERROTA_SURTOS
            return self.status
        
        # Verificar derrota por baralho vazio
        if self.tabuleiro.baralho_jogador.esta_vazio():
            self.status = StatusPartida.DERROTA_TEMPO
            return self.status
        
        # Verificar vitória (curas descobertas)
        if self.tabuleiro.verificar_vitoria_completa():
            self.status = StatusPartida.VITORIA
            return self.status
        
        # Verificar vitória alternativa (protótipo - sem cubos de doença)
        if self.tabuleiro.verificar_vitoria_prototipo():
            self.status = StatusPartida.VITORIA
            return self.status
        
        return StatusPartida.EM_ANDAMENTO

    def obter_jogador_atual(self) -> Jogador:
        """Retorna o jogador do turno atual"""
        return self.turno_atual.jogador_atual if self.turno_atual else None

    def obter_acoes_restantes(self) -> int:
        """Retorna o número de ações restantes no turno"""
        return self.turno_atual.verificar_acoes_restantes() if self.turno_atual else 0

    def esta_em_andamento(self) -> bool:
        """Verifica se a partida ainda está em andamento"""
        return self.status == StatusPartida.EM_ANDAMENTO

    def __str__(self):
        jogador_atual = self.obter_jogador_atual()
        return f"Partida: {self.status.value}, Turno: {jogador_atual.nome if jogador_atual else 'Nenhum'}, Surtos: {self.tabuleiro.marcador_surtos}"

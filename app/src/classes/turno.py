from .enums import FaseTurno

class Turno:
    """Classe que gerencia o turno atual do jogo"""
    
    def __init__(self, jogador_atual):
        self.jogador_atual = jogador_atual
        self.fase_atual = FaseTurno.ACOES
        self.acoes_restantes = 4
    
    def verificar_acoes_restantes(self) -> int:
        """Retorna o número de ações restantes no turno"""
        return self.acoes_restantes
    
    def decrementar_acoes(self):
        """Decrementa o contador de ações restantes"""
        if self.acoes_restantes > 0:
            self.acoes_restantes -= 1
        
        # Se não há mais ações, passa para a próxima fase
        if self.acoes_restantes == 0 and self.fase_atual == FaseTurno.ACOES:
            self.proxima_fase()
    
    def proxima_fase(self):
        """Avança para a próxima fase do turno"""
        if self.fase_atual == FaseTurno.ACOES:
            self.fase_atual = FaseTurno.COMPRA
        elif self.fase_atual == FaseTurno.COMPRA:
            self.fase_atual = FaseTurno.INFECCAO
        elif self.fase_atual == FaseTurno.INFECCAO:
            # Turno terminou, será reiniciado pela partida
            pass
    
    def reiniciar_turno(self, novo_jogador):
        """Reinicia o turno para um novo jogador"""
        self.jogador_atual = novo_jogador
        self.fase_atual = FaseTurno.ACOES
        self.acoes_restantes = 4
    
    def pode_realizar_acao(self) -> bool:
        """Verifica se o jogador pode realizar uma ação"""
        return self.fase_atual == FaseTurno.ACOES and self.acoes_restantes > 0
    
    def __str__(self):
        return f"Turno de {self.jogador_atual.nome if self.jogador_atual else 'Nenhum'}, Fase: {self.fase_atual.value}, Ações: {self.acoes_restantes}"

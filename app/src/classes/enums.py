from enum import Enum

class CorDoenca(Enum):
    AZUL = "azul"
    AMARELO = "amarelo"
    PRETO = "preto"
    VERMELHO = "vermelho"

class StatusPartida(Enum):
    EM_ANDAMENTO = "em_andamento"
    VITORIA = "vitoria"
    DERROTA_SURTOS = "derrota_surtos"
    DERROTA_DOENCA = "derrota_doenca"
    DERROTA_TEMPO = "derrota_tempo"

class FaseTurno(Enum):
    ACOES = "acoes"
    COMPRA = "compra"
    INFECCAO = "infeccao"

class TipoCartaJogador(Enum):
    CIDADE = "cidade"
    EVENTO = "evento"
    EPIDEMIA = "epidemia"

import random
from typing import List, Dict
from .city import Cidade
from .enums import CorDoenca, TipoCartaJogador
from .baralho import Baralho
from .cartas import CartaJogador, CartaInfeccao, CartaEpidemia
from .gerenciador_descarte import GerenciadorDescarte

class Tabuleiro:
    def __init__(self):
        self.cidades: List[Cidade] = []
        self.cidades_dict: Dict[str, Cidade] = {}
        self.taxa_infeccao = 2
        self.marcador_surtos = 0
        self.curas: Dict[CorDoenca, bool] = {
            CorDoenca.VERMELHO: False,
            CorDoenca.AZUL: False,
            CorDoenca.AMARELO: False,
            CorDoenca.PRETO: False
        }
        self.ponto_controle1 = ""
        self.ponto_controle2 = ""
        self.baralho_jogador: Baralho[CartaJogador] = Baralho()
        self.baralho_infeccao: Baralho[CartaInfeccao] = Baralho()
        self.gerenciador_descarte = GerenciadorDescarte()
        
        self._carregar_cidades()
        self._criar_baralho_infeccao()
        self._criar_baralho_jogador()
        self._infeccao_inicial()

    @property
    def descarte_jogador(self):
        """Propriedade para compatibilidade com código existente"""
        return self.gerenciador_descarte.descarte_jogador

    @property
    def descarte_infeccao(self):
        """Propriedade para compatibilidade com código existente"""
        return self.gerenciador_descarte.descarte_infeccao

    def _carregar_cidades(self):
        """Carrega as cidades e suas conexões"""
        cidades_data = {
            # Azul
            "Atlanta": {"color": CorDoenca.AZUL, "connections": ["Chicago", "Nova York"]},
            "Chicago": {"color": CorDoenca.AZUL, "connections": ["Atlanta", "Londres"]},
            "Nova York": {"color": CorDoenca.AZUL, "connections": ["Atlanta", "Londres"]},
            "Londres": {"color": CorDoenca.AZUL, "connections": ["Chicago", "Nova York", "Miami"]},
            # Amarelo
            "Miami": {"color": CorDoenca.AMARELO, "connections": ["Londres", "Cidade do México"]},
            "Cidade do México": {"color": CorDoenca.AMARELO, "connections": ["Miami", "Los Angeles", "Cairo"]},
            "Los Angeles": {"color": CorDoenca.AMARELO, "connections": ["Cidade do México", "São Paulo"]},
            "São Paulo": {"color": CorDoenca.AMARELO, "connections": ["Los Angeles", "Bagdá"]},
            # Preto
            "Cairo": {"color": CorDoenca.PRETO, "connections": ["Cidade do México", "Istambul"]},
            "Istambul": {"color": CorDoenca.PRETO, "connections": ["Cairo", "Moscou", "Riade"]},
            "Bagdá": {"color": CorDoenca.PRETO, "connections": ["São Paulo", "Riade", "Pequim"]},
            "Riade": {"color": CorDoenca.PRETO, "connections": ["Istambul", "Bagdá", "Seul"]},
            # Vermelho
            "Pequim": {"color": CorDoenca.VERMELHO, "connections": ["Bagdá", "Seul"]},
            "Seul": {"color": CorDoenca.VERMELHO, "connections": ["Riade", "Pequim", "Xangai"]},
            "Tóquio": {"color": CorDoenca.VERMELHO, "connections": ["Seul", "Xangai"]},
            "Xangai": {"color": CorDoenca.VERMELHO, "connections": ["Tóquio"]}
        }
        
        # Criar cidades
        for nome, dados in cidades_data.items():
            cidade = Cidade(nome, dados["color"])
            self.cidades.append(cidade)
            self.cidades_dict[nome] = cidade
        
        # Criar conexões
        for nome, dados in cidades_data.items():
            cidade = self.cidades_dict[nome]
            for conexao_nome in dados["connections"]:
                if conexao_nome in self.cidades_dict:
                    cidade_conexao = self.cidades_dict[conexao_nome]
                    if not cidade.esta_conectada_com(cidade_conexao):
                        cidade.adicionar_conexao(cidade_conexao)

    def _criar_baralho_infeccao(self):
        """Cria o baralho de infecção"""
        for cidade in self.cidades:
            carta = CartaInfeccao(cidade, cidade.cor)
            self.baralho_infeccao.adicionar_carta(carta)
        self.baralho_infeccao.embaralhar()

    def _criar_baralho_jogador(self):
        """Cria o baralho do jogador"""
        # Adicionar cartas de cidade
        cartas_cidade = []
        for cidade in self.cidades:
            carta = CartaJogador(TipoCartaJogador.CIDADE, cidade)
            cartas_cidade.append(carta)
        
        # Embaralhar cartas de cidade
        random.shuffle(cartas_cidade)
        
        # Adicionar cartas de epidemia (simplificado - adicionar 2 por agora)
        epidemias = [CartaEpidemia(), CartaEpidemia()]
        
        # Dividir baralho e inserir epidemias
        metade = len(cartas_cidade) // 2
        primeira_parte = cartas_cidade[:metade]
        segunda_parte = cartas_cidade[metade:]
        
        primeira_parte.append(epidemias[0])
        segunda_parte.append(epidemias[1])
        
        random.shuffle(primeira_parte)
        random.shuffle(segunda_parte)
        
        # Montar baralho final
        todas_cartas = primeira_parte + segunda_parte
        self.baralho_jogador.adicionar_cartas(todas_cartas)

    def _infeccao_inicial(self):
        """Executa a infecção inicial do jogo"""
        cidades_infectadas = random.sample(self.cidades, min(9, len(self.cidades)))
        
        for i, cidade in enumerate(cidades_infectadas):
            # 3 cidades com 3 cubos, 3 cidades com 2 cubos, 3 cidades com 1 cubo
            cubos = 3 - (i // 3)
            for _ in range(cubos):
                cidade.adicionar_cubo(cidade.cor)
            
            # Adicionar carta ao descarte
            carta_infeccao = CartaInfeccao(cidade, cidade.cor)
            self.gerenciador_descarte.descartar_infeccao(carta_infeccao)

    def obter_cidade(self, nome: str) -> Cidade:
        """Obtém uma cidade pelo nome"""
        return self.cidades_dict.get(nome)

    def obter_cidade_atual(self, jogador) -> Cidade:
        """Obtém a cidade atual de um jogador"""
        return jogador.localizacao

    def mover_jogador(self, jogador, destino: Cidade):
        """Move um jogador para uma cidade de destino"""
        if destino in jogador.localizacao.conexoes:
            jogador.atualizar_localizacao(destino)
            print(f"{jogador.nome} se moveu para {destino.nome}")
        else:
            print(f"Movimento inválido: {jogador.localizacao.nome} não está conectada a {destino.nome}")

    def tratar_doenca(self, jogador, cor: CorDoenca):
        """Trata doença na cidade atual do jogador"""
        jogador.tratar(cor)

    def construir_base(self, jogador, partida=None):
        """Constrói uma base de pesquisa na cidade atual do jogador"""
        return jogador.construir_base(partida)

    def espalhar_doenca(self):
        """Executa a fase de infecção"""
        for _ in range(self.taxa_infeccao):
            if not self.baralho_infeccao.esta_vazio():
                carta = self.baralho_infeccao.sacar()
                self.gerenciador_descarte.descartar_infeccao(carta)
                
                cidade = carta.cidade
                if cidade.adicionar_cubo(carta.cor):
                    # Usar conjunto para evitar surtos múltiplos na mesma cidade
                    cidades_em_surto = set()
                    self.aplicar_surto(cidade, carta.cor, cidades_em_surto)

    def aplicar_surto(self, cidade: Cidade, cor: CorDoenca, cidades_em_surto: set = None):
        """Aplica um surto na cidade especificada"""
        if cidades_em_surto is None:
            cidades_em_surto = set()
        
        # Evitar surto múltiplo na mesma cidade
        if cidade in cidades_em_surto:
            return
        
        cidades_em_surto.add(cidade)
        self.marcador_surtos += 1
        print(f"SURTO EM {cidade.nome}! ({cor.value})")
        
        # Infectar cidades conectadas
        for cidade_conectada in cidade.conexoes:
            if cidade_conectada.adicionar_cubo(cor):
                # Surto em cadeia - mas só se a cidade não teve surto ainda
                self.aplicar_surto(cidade_conectada, cor, cidades_em_surto)

    def acessar_baralho_jogador(self) -> Baralho[CartaJogador]:
        """Retorna o baralho do jogador"""
        return self.baralho_jogador

    def acessar_baralho_infeccao(self) -> Baralho[CartaInfeccao]:
        """Retorna o baralho de infecção"""
        return self.baralho_infeccao

    def verificar_derrota_surtos(self) -> bool:
        """Verifica se houve derrota por surtos"""
        return self.marcador_surtos >= 8

    def verificar_vitoria_prototipo(self) -> bool:
        """Verifica condição de vitória (protótipo - sem cubos)"""
        for cidade in self.cidades:
            if cidade.total_cubos_doenca() > 0:
                return False
        return True

    def descobrir_cura(self, jogador, cor: CorDoenca) -> bool:
        """
        Tenta descobrir a cura para uma doença
        Requer 5 cartas da mesma cor (4 para Cientista)
        """
        if self.curas[cor]:
            print(f"A cura para {cor.value} já foi descoberta!")
            return False
        
        # Verificar se está em uma base de pesquisa
        if not jogador.localizacao.tem_base:
            print(f"{jogador.nome} deve estar em uma base de pesquisa para descobrir curas!")
            return False
        
        # Contar cartas da cor necessária
        cartas_da_cor = []
        for carta in jogador.mao:
            if hasattr(carta, 'cidade') and carta.cidade and carta.cidade.cor == cor:
                cartas_da_cor.append(carta)
        
        # Determinar quantas cartas são necessárias
        cartas_necessarias = 4 if jogador.personagem.nome == "Cientista" else 5
        
        if len(cartas_da_cor) >= cartas_necessarias:
            # Descartar as cartas usadas
            for i in range(cartas_necessarias):
                carta = cartas_da_cor[i]
                jogador.mao.remove(carta)
                self.gerenciador_descarte.descartar_jogador(carta)
            
            # Descobrir a cura
            self.curas[cor] = True
            print(f"🎉 {jogador.nome} descobriu a cura para {cor.value}!")
            
            # Verificar vitória
            if all(self.curas.values()):
                print("🏆 VITÓRIA! Todas as curas foram descobertas!")
            
            return True
        else:
            print(f"{jogador.nome} precisa de {cartas_necessarias} cartas de {cor.value}, mas tem apenas {len(cartas_da_cor)}")
            return False
    
    def verificar_vitoria_completa(self) -> bool:
        """Verifica se todas as curas foram descobertas"""
        return all(self.curas.values())

# Manter compatibilidade com código existente
Board = Tabuleiro
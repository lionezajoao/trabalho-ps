class Player:
    def __init__(self, name, location):
        """
        Inicializa um novo jogador.

        Args:
            name (str): O nome do jogador.
            location (City): A cidade inicial do jogador.
        """
        self.name = name
        self.location = location
        self.actions_left = 4
        self.hand = []  # Lista para armazenar as cartas do jogador (a ser implementada)

    def move(self, city):
        """
        Move o jogador para uma cidade conectada.

        Args:
            city (City): A cidade para a qual o jogador deseja se mover.
        """
        if city in self.location.connections:
            print(f"{self.name} se moveu de {self.location.name} para {city.name}.")
            self.location = city
            self.actions_left -= 1
        else:
            print(f"{self.name} não pode se mover para {city.name}. Não estão conectados.")

    def treat(self, color=None):
        """
        Tenta tratar uma doença na cidade atual. Se houver um centro de pesquisa, cura completamente a doença.

        Args:
            color (str, optional): A cor da doença a ser tratada ('vermelho', 'azul', 'amarelo', 'preto').
        """
        if color in self.location.infection_levels:
            if self.location.has_research_station:
                if self.location.infection_levels[color] > 0:
                    print(f"{self.name} curou completamente a doença {color} em {self.location.name} (centro de pesquisa).")
                    self.location.infection_levels[color] = 0
                    self.actions_left -= 1
                    print(f"Nível de infecção de {color} em {self.location.name} agora é {self.location.infection_levels[color]}.")
                else:
                    print(f"Não há infecção de {color} para curar em {self.location.name}.")
            else:
                if self.location.infection_levels[color] > 0:
                    print(f"{self.name} tratou a doença {color} em {self.location.name}.")
                    self.location.infection_levels[color] -= 1
                    self.actions_left -= 1
                    print(f"Nível de infecção de {color} em {self.location.name} agora é {self.location.infection_levels[color]}.")
                else:
                    print(f"Não há infecção de {color} para tratar em {self.location.name}.")
        elif color is not None:
            print(f"Cor de doença inválida: {color}.")
        else:
            print("Por favor especifique uma cor para tratar.")

    def build_research_station(self):
        """
        Constrói um centro de pesquisa na cidade atual.
        (A lógica completa depende se já existe um centro e se o jogador tem a carta necessária)
        """
        if not self.location.has_research_station:
            print(f"{self.name} construiu um centro de pesquisa em {self.location.name}.")
            self.location.has_research_station = True
            self.actions_left -= 1
        else:
            print(f"Já existe um centro de pesquisa em {self.location.name}.")

    def reset_actions(self):
        """
        Reseta o número de ações do jogador para o início do turno.
        """
        self.actions_left = 4

    def add_card(self, card):
        """
        Adiciona uma carta à mão do jogador.
        (A ser implementada)
        """
        self.hand.append(card)
        print(f"{self.name} recebeu a carta {card}.")

    def remove_card(self, card):
        """
        Remove uma carta da mão do jogador.
        (A ser implementada)
        """
        if card in self.hand:
            self.hand.remove(card)
            print(f"{self.name} descartou a carta {card}.")
        else:
            print(f"{self.name} não possui a carta {card}.")

    # Outras ações do jogador (compartilhar conhecimento, descobrir cura, ações de cartas de evento)
    # seriam implementadas aqui.

    def __str__(self):
        return f"Jogador: {self.name}, Localização: {self.location.name}, Ações: {self.actions_left}"
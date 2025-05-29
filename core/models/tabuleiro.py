# board.py
import random
from .cidade import City

class Board:
    def __init__(self):
        self.cities = {
            "Atlanta": City("Atlanta", "azul"),
            "Chicago": City("Chicago", "azul"),
            "Miami": City("Miami", "amarelo"),
            "Nova York": City("Nova York", "azul"),
            "Dallas": City("Dallas", "amarelo"),
            "Los Angeles": City("Los Angeles", "amarelo"),
            "São Francisco": City("São Francisco", "azul"),
            "Montreal": City("Montreal", "azul"),
            "Washington": City("Washington", "azul"),
            "Londres": City("Londres", "preto"),
            "Madri": City("Madri", "amarelo"),
            "Paris": City("Paris", "azul"),
            "Milão": City("Milão", "preto"),
            "Roma": City("Roma", "preto"),
            "Argel": City("Argel", "preto"),
            "Cairo": City("Cairo", "preto"),
            "Istambul": City("Istambul", "preto"),
            "Moscou": City("Moscou", "preto"),
            "São Petersburgo": City("São Petersburgo", "azul"),
            "Bagdá": City("Bagdá", "preto"),
            "Teerã": City("Teerã", "preto"),
            "Carachi": City("Carachi", "amarelo"),
            "Mumbai": City("Mumbai", "preto"),
            "Deli": City("Deli", "preto"),
            "Calcutá": City("Calcutá", "amarelo"),
            "Bangcoc": City("Bangcoc", "vermelho"),
            "Pequim": City("Pequim", "vermelho"),
            "Seul": City("Seul", "vermelho"),
            "Tóquio": City("Tóquio", "vermelho"),
            "Xangai": City("Xangai", "vermelho"),
            "Hong Kong": City("Hong Kong", "vermelho"),
            "Taipei": City("Taipei", "vermelho"),
            "Manila": City("Manila", "vermelho"),
            "Sydney": City("Sydney", "vermelho"),
            "Jacarta": City("Jacarta", "amarelo"),
            "Ho Chi Minh": City("Ho Chi Minh", "vermelho")
        }

        # Conexões (adaptado do Pandemic)
        connections_data = {
            "Atlanta": ["Chicago", "Miami", "Washington"],
            "Chicago": ["Atlanta", "Montreal", "Los Angeles", "São Francisco"],
            "Miami": ["Atlanta", "Washington", "Bogotá"], # Bogotá não está implementada
            "Nova York": ["Montreal", "Washington", "Londres", "Madri"],
            "Dallas": ["Los Angeles", "Memphis", "Oklahoma City"], # Memphis e Oklahoma City não implementadas
            "Los Angeles": ["São Francisco", "Chicago", "Dallas", "Sydney"],
            "São Francisco": ["Los Angeles", "Chicago", "Tóquio", "Manila"],
            "Montreal": ["Chicago", "Nova York", "Washington"],
            "Washington": ["Atlanta", "Nova York", "Montreal", "Miami"],
            "Londres": ["Nova York", "Paris", "Madri", "Essen"], # Essen não implementada
            "Madri": ["Londres", "Paris", "Argel", "Nova York", "São Paulo"], # São Paulo não implementada
            "Paris": ["Londres", "Madri", "Milão", "Argel", "Frankfurt"], # Frankfurt não implementada
            "Milão": ["Paris", "Istambul", "Roma"],
            "Roma": ["Milão", "Nápoles", "Atenas"], # Nápoles e Atenas não implementadas
            "Argel": ["Madri", "Paris", "Cairo", "Istambul"],
            "Cairo": ["Argel", "Istambul", "Bagdá", "Riade"], # Riade não implementada
            "Istambul": ["Milão", "Argel", "Cairo", "São Petersburgo", "Bagdá", "Atenas"],
            "Moscou": ["São Petersburgo", "Istambul", "Teerã"],
            "São Petersburgo": ["Moscou", "Estocolmo", "Istambul", "Kiev"], # Estocolmo e Kiev não implementadas
            "Bagdá": ["Cairo", "Istambul", "Teerã", "Carachi", "Riad"],
            "Teerã": ["Bagdá", "Moscou", "Carachi", "Deli"],
            "Carachi": ["Bagdá", "Teerã", "Mumbai", "Deli"],
            "Mumbai": ["Carachi", "Deli", "Calcutá"],
            "Deli": ["Carachi", "Teerã", "Calcutá", "Chennai"], # Chennai não implementada
            "Calcutá": ["Deli", "Mumbai", "Bangcoc", "Hong Kong"],
            "Bangcoc": ["Calcutá", "Hong Kong", "Ho Chi Minh", "Jacarta"],
            "Pequim": ["Seul", "Xangai"],
            "Seul": ["Pequim", "Tóquio", "Xangai"],
            "Tóquio": ["Seul", "Xangai", "Osaka", "São Francisco"], # Osaka não implementada
            "Xangai": ["Pequim", "Seul", "Tóquio", "Hong Kong", "Taipei"],
            "Hong Kong": ["Xangai", "Calcutá", "Bangcoc", "Manila", "Taipei", "Ho Chi Minh"],
            "Taipei": ["Xangai", "Hong Kong", "Manila", "Osaka"],
            "Manila": ["Taipei", "Hong Kong", "São Francisco", "Sydney", "Jacarta"],
            "Sydney": ["Jakarta", "Manila", "Los Angeles"],
            "Jacarta": ["Chennai", "Bangcoc", "Ho Chi Minh", "Sydney"],
            "Ho Chi Minh": ["Bangcoc", "Hong Kong", "Jacarta", "Manila"]
        }

        for city_name, connections in connections_data.items():
            city_obj = self.cities[city_name]
            for connected_name in connections:
                if connected_name in self.cities:
                    city_obj.add_connection(self.cities[connected_name])

        self.outbreak_count = 0
        self.max_outbreaks = 5
        self.disease_colors = ["vermelho", "azul", "amarelo", "preto"]
        self.infection_deck = self._build_infection_deck()
        random.shuffle(self.infection_deck)
        self.infection_rate = 2 # Inicial infection rate

    def _build_infection_deck(self):
        return list(self.cities.keys()) * 2 # Duas cartas de cada cidade

    def infect_cities(self, num_cards):
        infected_this_turn = []
        for _ in range(num_cards):
            if self.infection_deck:
                city_name = self.infection_deck.pop(0)
                city_to_infect = self.get_city(city_name)
                if city_to_infect:
                    color_to_infect = random.choice(self.disease_colors) # Cor aleatória inicialmente
                    if city_to_infect.infect(color_to_infect):
                        self.handle_outbreak(city_to_infect, color_to_infect)
                    infected_this_turn.append(city_name)
                else:
                    print(f"Erro: Cidade '{city_name}' não encontrada no tabuleiro.")
            else:
                print("O baralho de infecção acabou!")
                break
        print("Cidades infectadas:", ", ".join(infected_this_turn))

    def handle_outbreak(self, city, color):
        self.outbreak_count += 1
        print(f"\n!!! SURTO DE {color} EM {city.name} !!! (Total de surtos: {self.outbreak_count})")
        outbroken_cities = {city}
        queue = [city]

        while queue:
            current_city = queue.pop(0)
            for neighbor in current_city.connections:
                if neighbor not in outbroken_cities:
                    outbroken_cities.add(neighbor)
                    if neighbor.infect(color):
                        queue.append(neighbor)

    def get_city(self, name):
        return self.cities.get(name)

    def check_game_over(self):
        if self.outbreak_count >= self.max_outbreaks:
            print("\n!!! GAME OVER !!! Muitos surtos ocorreram.")
            return True
        # Adicionar aqui condição de derrota por muitas infecções no tabuleiro
        return False

    def display_board(self):
        print("\n--- Tabuleiro ---")
        for city_name, city_obj in self.cities.items():
            connections_str = ", ".join([connected_city.name for connected_city in city_obj.connections])
            print(f"{city_obj} -> Conexões: {connections_str}")
        print(f"Total de Surtos: {self.outbreak_count}")
        print("------------------")
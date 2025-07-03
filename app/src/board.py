import random

from app.src.city import City

class Board:
    def __init__(self, num_players=2): # Podemos definir um padrão para num_players aqui
        self.cities = self.load_cities()
        self.infection_rate = 2
        self.outbreak_count = 0
        self.cured_diseases = {"vermelho": False, "azul": False, "amarelo": False, "preto": False}
        self.research_stations = set()
        self.infection_deck = self.create_infection_deck()
        self.infection_discard = []
        self.player_deck = self.create_player_deck()
        self.player_discard = []
        self.players = []
        self.initial_infection()
        for city in self.cities.values():
            city.board = self # Define a referência ao tabuleiro para cada cidade

    def load_cities(self):
        cities_data_16_connected = {
            # Azul
            "Atlanta": {"color": "azul", "connections": ["Chicago", "Nova York"]},
            "Chicago": {"color": "azul", "connections": ["Atlanta", "Londres"]},
            "Nova York": {"color": "azul", "connections": ["Atlanta", "Londres"]},
            "Londres": {"color": "azul", "connections": ["Chicago", "Nova York", "Miami"]},
            # Amarelo
            "Miami": {"color": "amarelo", "connections": ["Londres", "Cidade do México"]},
            "Cidade do México": {"color": "amarelo", "connections": ["Miami", "Los Angeles", "Cairo"]},
            "Los Angeles": {"color": "amarelo", "connections": ["Cidade do México", "São Paulo"]},
            "São Paulo": {"color": "amarelo", "connections": ["Los Angeles", "Bagdá"]},
            # Preto
            "Cairo": {"color": "preto", "connections": ["Cidade do México", "Istambul"]},
            "Istambul": {"color": "preto", "connections": ["Cairo", "Moscou", "Riade"]},
            "Bagdá": {"color": "preto", "connections": ["São Paulo", "Riade", "Pequim"]},
            "Riade": {"color": "preto", "connections": ["Istambul", "Bagdá", "Seul"]},
            # Vermelho
            "Pequim": {"color": "vermelho", "connections": ["Bagdá", "Seul"]},
            "Seul": {"color": "vermelho", "connections": ["Riade", "Pequim", "Xangai"]},
            "Tóquio": {"color": "vermelho", "connections": ["Seul", "Xangai"]},
            "Xangai": {"color": "vermelho", "connections": ["Tóquio"]}
        }
        cities = {name: City(name, data["color"]) for name, data in cities_data_16_connected.items()}
        for name, data in cities_data_16_connected.items():
            for connection_name in data["connections"]:
                if connection_name in cities:
                    cities[name].add_connection(cities[connection_name])
        return cities

    def get_city(self, city_name):
        return self.cities.get(city_name)

    def create_infection_deck(self):
        return list(self.cities.keys())

    def create_player_deck(self):
        deck = []
        city_cards = list(self.cities.keys())
        random.shuffle(city_cards)
        deck.extend(city_cards)
        # Adicionar cartas de evento
        random.shuffle(deck)
        return deck

    def initial_infection(self):
        infection_cities = random.sample(list(self.cities.keys()), min(9, len(self.cities)))
        for i, city_name in enumerate(infection_cities):
            city = self.get_city(city_name)
            for _ in range(3 - (i // 3)):
                city.infect(city.color)
            self.infection_discard.append(city_name)
        random.shuffle(self.infection_deck)

    def infect_cities(self, num_cards):
        for _ in range(num_cards):
            if not self.infection_deck:
                self.infection_deck = list(self.infection_discard)
                self.infection_discard = []
                random.shuffle(self.infection_deck)
            if self.infection_deck:
                card = self.infection_deck.pop(0)
                self.infection_discard.append(card)
                city = self.get_city(card)
                if city.infect(city.color):
                    self.outbreak_count += 1
                    print(f"SURTO EM {city.name}!")

    def check_game_over(self):
        if self.outbreak_count >= 8:
            print("Você perdeu! Muitos surtos ocorreram.")
            return True
        return False

    def check_win_prototype(self):
        for city in self.cities.values():
            for level in city.infection_levels.values():
                if level > 0:
                    return False
        return True
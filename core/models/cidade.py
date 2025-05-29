# city.py
class City:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.connections = []
        self.infection_levels = {"vermelho": 0, "azul": 0, "amarelo": 0, "preto": 0}
        self.has_research_station = False

    def add_connection(self, city):
        if city not in self.connections:
            self.connections.append(city)
            city.connections.append(self)

    def infect(self, color):
        if color in self.infection_levels:
            if self.infection_levels[color] < 3:
                self.infection_levels[color] += 1
                print(f"{self.name} foi infectada com {color}. Nível: {self.infection_levels[color]}")
                return False
            else:
                print(f"SURTO de {color} em {self.name}!")
                return True
        return False

    def treat(self, color):
        if color in self.infection_levels and self.infection_levels[color] > 0:
            self.infection_levels[color] -= 1
            print(f"Tratada 1 unidade de {color} em {self.name}. Nível restante: {self.infection_levels[color]}")
            return True
        else:
            print(f"Não há {color} para tratar em {self.name}.")
            return False

    def build_research_station(self):
        if not self.has_research_station:
            self.has_research_station = True
            print(f"Centro de pesquisa construído em {self.name}.")
            return True
        else:
            print(f"Já existe um centro de pesquisa em {self.name}.")
            return False

    def __str__(self):
        infection_str = ", ".join([f"{c}: {l}" for c, l in self.infection_levels.items() if l > 0])
        research_station_str = " (Centro de Pesquisa)" if self.has_research_station else ""
        return f"{self.name} ({self.color}, Infecções: {infection_str}){research_station_str}"

    def __repr__(self):
        return f"City('{self.name}', '{self.color}')"
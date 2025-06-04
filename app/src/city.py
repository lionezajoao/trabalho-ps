class City:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.connections = []
        self.infection_levels = {"vermelho": 0, "azul": 0, "amarelo": 0, "preto": 0}
        self.has_research_station = False
        self.board = None # Adicionado para referência ao tabuleiro

    def add_connection(self, city):
        if city not in self.connections:
            self.connections.append(city)
            city.connections.append(self)

    def infect(self, color):
        if self.infection_levels[color] < 3:
            self.infection_levels[color] += 1
            return False  # No surto
        else:
            return True   # Ocorreu um surto

    def treat_disease(self, color):
        if self.infection_levels[color] > 0:
            self.infection_levels[color] -= 1
            return True
        return False

    def __str__(self):
        return f"{self.name} ({self.color}), Infections: {self.infection_levels}, Research: {self.has_research_station}"
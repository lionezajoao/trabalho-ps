# player.py
class Player:
    def __init__(self, name, start_location):
        self.name = name
        self.location = start_location
        self.actions_left = 4

    def move(self, destination):
        if self.actions_left > 0:
            if destination in self.location.connections:
                self.location = destination
                self.actions_left -= 1
                print(f"{self.name} se moveu para {destination.name} (Ações restantes: {self.actions_left})")
                return True
            else:
                print("Movimento inválido.")
                return False
        else:
            print("Você não tem ações restantes para mover.")
            return False

    def treat(self):
        if self.actions_left > 0:
            print("Doenças presentes:", [color for color, level in self.location.infection_levels.items() if level > 0])
            treat_color = input("Qual doença deseja tratar? ").lower()
            if treat_color in self.location.infection_levels and self.location.infection_levels[treat_color] > 0:
                if self.location.treat(treat_color):
                    self.actions_left -= 1
                    return True
                else:
                    return False
            else:
                print("Doença inválida ou não presente nesta cidade.")
                return False
        else:
            print("Você não tem ações restantes para tratar.")
            return False
        return False

    def build_research_station(self):
        if self.actions_left > 0:
            if self.location.build_research_station():
                self.actions_left -= 1
                return True
            return False
        else:
            print("Você não tem ações restantes para construir um centro de pesquisa.")
            return False

    def reset_actions(self):
        self.actions_left = 4
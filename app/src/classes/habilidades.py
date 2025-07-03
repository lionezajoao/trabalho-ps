from abc import ABC, abstractmethod

class IHabilidadeEspecial(ABC):
    """Interface para habilidades especiais dos personagens"""
    
    @abstractmethod
    def executar(self, jogador, partida):
        """Executa a habilidade especial"""
        pass

class HabilidadeMedico(IHabilidadeEspecial):
    """Habilidade do Médico: Pode tratar doenças mais eficientemente"""
    
    def executar(self, jogador, partida):
        # Médico pode tratar automaticamente todas as doenças de uma cor na cidade atual
        # quando trata normalmente, remove todos os cubos ao invés de um
        cidade_atual = jogador.localizacao
        print(f"Médico {jogador.nome} usa habilidade especial em {cidade_atual.nome}")
        
        # Encontrar doenças presentes na cidade
        doencas_presentes = []
        for cor in cidade_atual.cubos_doenca:
            if cidade_atual.cubos_doenca[cor] > 0:
                doencas_presentes.append(cor)
        
        if not doencas_presentes:
            print("Não há doenças para tratar nesta cidade")
            return
        
        # Se há cura descoberta, remover todos os cubos da doença curada
        for cor in doencas_presentes:
            if partida.tabuleiro.curas[cor]:
                cidade_atual.cubos_doenca[cor] = 0
                print(f"Médico removeu automaticamente todos os cubos de {cor.value} (cura descoberta)")
            else:
                # Senão, remove todos os cubos de uma cor escolhida
                cidade_atual.cubos_doenca[cor] = 0
                print(f"Médico removeu todos os cubos de {cor.value} em {cidade_atual.nome}")
                break  # Médico pode escolher uma cor por vez

class HabilidadePesquisadora(IHabilidadeEspecial):
    """Habilidade da Pesquisadora: Pode compartilhar cartas mais facilmente"""
    
    def executar(self, jogador, partida):
        # Pesquisadora pode dar qualquer carta da mão para jogadores na mesma cidade
        # e pode receber cartas de qualquer jogador na mesma cidade
        jogadores_na_mesma_cidade = []
        for outro_jogador in partida.jogadores:
            if outro_jogador != jogador and outro_jogador.localizacao == jogador.localizacao:
                jogadores_na_mesma_cidade.append(outro_jogador)
        
        if jogadores_na_mesma_cidade:
            print(f"Pesquisadora {jogador.nome} pode compartilhar qualquer carta com: {[j.nome for j in jogadores_na_mesma_cidade]}")
            print("A Pesquisadora pode dar ou receber qualquer carta (não apenas da cidade atual)")
        else:
            print(f"Pesquisadora {jogador.nome} está sozinha em {jogador.localizacao.nome}")

class HabilidadeCientista(IHabilidadeEspecial):
    """Habilidade do Cientista: Precisa de menos cartas para descobrir cura"""
    
    def executar(self, jogador, partida):
        # Cientista precisa de apenas 4 cartas da mesma cor para descobrir cura (ao invés de 5)
        # Esta habilidade é passiva, mas pode ser ativada para mostrar status
        if not jogador.localizacao.tem_base:
            print(f"Cientista {jogador.nome} precisa estar em uma base de pesquisa para descobrir curas")
            return
        
        # Mostrar status das cores que pode descobrir
        for cor in partida.tabuleiro.curas:
            if not partida.tabuleiro.curas[cor]:
                cartas_da_cor = sum(1 for carta in jogador.mao 
                                  if hasattr(carta, 'cidade') and carta.cidade and carta.cidade.cor == cor)
                print(f"Cientista tem {cartas_da_cor}/4 cartas para descobrir cura de {cor.value}")

class HabilidadeOperacoes(IHabilidadeEspecial):
    """Habilidade do Especialista em Operações: Pode construir bases mais facilmente"""
    
    def executar(self, jogador, partida):
        # Especialista em Operações pode construir base sem descartar carta da cidade
        if not jogador.localizacao.tem_base:
            jogador.localizacao.tem_base = True
            print(f"Especialista em Operações {jogador.nome} construiu base em {jogador.localizacao.nome} sem descartar carta")
        else:
            print(f"Já existe uma base de pesquisa em {jogador.localizacao.nome}")
            # Pode mover-se para qualquer cidade com base de pesquisa
            cidades_com_base = [cidade for cidade in partida.tabuleiro.cidades if cidade.tem_base and cidade != jogador.localizacao]
            if cidades_com_base:
                print(f"Especialista pode se mover para qualquer cidade com base: {[c.nome for c in cidades_com_base]}")

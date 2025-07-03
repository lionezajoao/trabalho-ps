# 🦠 Pandemic - Jogo de Tabuleiro Digital

**Desenvolvido por:** Carlos Eduardo, Erivelton Campos, Gabriel Pinho, João Pedro Barboza, Leonardo Lima, Pedro Mileipp  
**Disciplina:** Projeto de Software  
**Professor:** João Felipe Nicolaci

---

## **📌 Visão Geral do Jogo**

**Pandemic** é um jogo cooperativo onde os jogadores assumem papéis de especialistas em saúde tentando conter e curar quatro doenças que se espalham pelo mundo. O objetivo é descobrir as curas antes que ocorram **8 surtos**, as doenças se espalhem demais (falta de cubos) ou o tempo acabe (baralho de cartas esgotado).

### **🎯 Objetivo Principal**

-   **Descobrir curas para todas as 4 doenças** (Azul, Amarela, Preta e Vermelha).
-   **Trabalhar em equipe**, utilizando habilidades especiais de cada personagem.

### **⚔️ Condições de Derrota**

1. **8 surtos ocorrerem** (marcador de surtos atinge o limite).
2. **Acabarem os cubos de uma doença** (não é possível colocar mais cubos no tabuleiro).
3. **O baralho de jogador acabar** (tempo esgotado).

---

## **� Como Executar**

### **Executar o Jogo**

```bash
cd /caminho/para/trabalho-ps
python app/main.py
```

### **Executar Demonstração das Classes**

```bash
cd /caminho/para/trabalho-ps
python demo_classes.py
```

### **📋 Requisitos**

-   Python 3.11+
-   Pygame
-   Bibliotecas padrão do Python

---

## **🏗️ Arquitetura do Projeto**

O projeto foi **completamente remodelado** seguindo um diagrama UML bem definido, implementando padrões de design robustos e uma arquitetura orientada a objetos.

### **📊 Estrutura de Classes Implementada**

```
app/src/
├── enums.py          # Enumerações do jogo
├── habilidades.py    # Interface e implementações de habilidades
├── cartas.py         # Hierarquia de cartas
├── baralho.py        # Baralho genérico
├── personagem.py     # Hierarquia de personagens
├── city.py          # Classe Cidade
├── player.py        # Classe Jogador
├── turno.py         # Classe Turno
├── board.py         # Classe Tabuleiro
└── partida.py       # Classe Partida principal
```

### **🎭 Padrões de Design Implementados**

1. **Strategy Pattern**: Sistema de habilidades especiais dos personagens
2. **Template Method**: Classes abstratas para Carta e Personagem
3. **Composition**: Relacionamentos entre classes seguindo UML
4. **Generics**: Baralho type-safe que funciona com qualquer tipo de carta

### **📚 Classes Principais**

#### **Enums** (`src/enums.py`)

-   `CorDoenca`: AZUL, AMARELO, PRETO, VERMELHO
-   `StatusPartida`: EM_ANDAMENTO, VITORIA, DERROTA_SURTOS, etc.
-   `FaseTurno`: ACOES, COMPRA, INFECCAO
-   `TipoCartaJogador`: CIDADE, EVENTO, EPIDEMIA

#### **Sistema de Habilidades** (`src/habilidades.py`)

-   `IHabilidadeEspecial`: Interface Strategy
-   `HabilidadeMedico`: Trata doenças mais eficientemente
-   `HabilidadePesquisadora`: Compartilha cartas facilmente
-   `HabilidadeCientista`: Precisa de menos cartas para curas
-   `HabilidadeOperacoes`: Constrói bases sem cartas

#### **Sistema de Cartas** (`src/cartas.py`)

-   `Carta`: Classe abstrata base
-   `CartaJogador`: Cartas do baralho do jogador
-   `CartaInfeccao`: Cartas do baralho de infecção
-   `CartaEvento`: Cartas de eventos especiais
-   `CartaEpidemia`: Cartas de epidemia com lógica específica

#### **Classes de Jogo**

```python
class Partida:
    - status: StatusPartida
    - jogadores: List[Jogador]
    - turno_atual: Turno
    - tabuleiro: Tabuleiro

class Jogador:
    - nome: str
    - personagem: Personagem
    - mao: List[CartaJogador]
    - localizacao: Cidade

class Tabuleiro:
    - cidades: List[Cidade]
    - taxa_infeccao: int
    - marcador_surtos: int
    - baralho_jogador: Baralho[CartaJogador]
    - baralho_infeccao: Baralho[CartaInfeccao]
```

---

## **📋 Funcionalidades Implementadas**

✅ **Movimentação de jogadores entre cidades**  
✅ **Tratamento de doenças (remoção de cubos)**  
✅ **Construção de bases de pesquisa**  
✅ **Compartilhamento de cartas entre jogadores**  
✅ **Mecanismo de espalhamento da infecção**  
✅ **Fases de epidemia e surtos em cadeia**  
✅ **Verificação de condições de vitória/derrota**  
✅ **Sistema de turnos com 4 ações por jogador**  
✅ **Habilidades especiais dos personagens**  
✅ **Interface gráfica com Pygame**

---

## **📋 Requisitos Funcionais Detalhados**

### **1. Gerenciamento do Tabuleiro**

-   Representação de **16 cidades** e suas conexões
-   Controle de **cubos de doença** (máximo de 3 por cidade)
-   Marcadores de **surtos, taxa de infecção e curas**

### **2. Controle do Fluxo do Jogo**

-   **Turnos** com 4 ações por jogador
-   **Fases**: Ações do jogador, compra de cartas e infecção
-   Verificação automática de **condições de vitória/derrota**

### **3. Sistema de Movimento**

-   **Movimentação entre cidades conectadas**
-   Validação de **movimentos válidos**

### **4. Tratamento de Doenças**

-   **Remoção de cubos** de doença das cidades
-   **Tratamento completo** em cidades com bases de pesquisa

### **5. Construção de Bases**

-   **Construção de bases de pesquisa** para facilitar o tratamento

### **6. Habilidades Especiais**

-   **Médico**: Remove todos os cubos de uma doença
-   **Pesquisadora**: Compartilha qualquer carta
-   **Cientista**: Precisa de apenas 4 cartas para curas
-   **Especialista em Operações**: Constrói bases sem cartas

### **7. Mecânica de Epidemias**

-   **Cartas de epidemia** que intensificam a infecção
-   **Surtos em cadeia** quando cidades atingem limite

---

## **⚙️ Requisitos Não Funcionais**

### **1. Interface de Usuário**

-   **Interface gráfica intuitiva** com Pygame
-   **Indicadores visuais** de estado do jogo
-   **Feedback claro** para ações do jogador

### **2. Desempenho**

-   **Processamento eficiente** de ações e surtos
-   **Arquitetura modular** para fácil manutenção

### **3. Multiplayer**

-   **Suporte a 2-4 jogadores** locais
-   **Sistema de turnos** bem definido

### **4. Extensibilidade**

-   **Arquitetura orientada a objetos** para fácil extensão
-   **Padrões de design** para adicionar novas funcionalidades

---

## **� Documentação Técnica**

### **Diagramas UML**

-   **Diagrama de Classes** ([Ver diagrama](docs/diagram/class/pandemic_class_diagram.png))
-   **Diagrama de Comunicação** ([Ver diagrama](docs/diagram/communication/))
-   **Diagrama de Sequência** ([Ver diagrama](docs/diagram/sequence/))

### **Documentação Adicional**

-   [Documentação de Instalação](docs/start.md)
-   [Documentação de Remodelação](REFACTORING.md)
-   [Demonstração das Classes](demo_classes.py)

---

## **🔄 Benefícios da Remodelação**

1. **Arquitetura Limpa**: Segue princípios SOLID
2. **Extensibilidade**: Fácil adicionar novos personagens, cartas ou habilidades
3. **Manutenibilidade**: Código organizado em classes específicas
4. **Type Safety**: Uso de enums e tipos específicos
5. **Testabilidade**: Classes isoladas e bem definidas
6. **Compatibilidade**: Interface gráfica mantida funcionando

---

## **📅 Roadmap do Projeto**

### **✅ Fase 1 - Concluída**

-   Implementação das classes base
-   Diagrama de Classes UML
-   Sistema básico de turnos

### **✅ Fase 2 - Concluída**

-   Remodelação completa seguindo UML
-   Implementação de padrões GRASP/GoF
-   Sistema de habilidades com Strategy Pattern

### **� Fase 3 - Em Desenvolvimento**

-   Melhorias na UI interativa
-   Implementação completa de cartas de evento
-   Sistema de descoberta de curas

### **� Próximas Etapas**

-   Testes automatizados
-   Balanceamento de regras
-   Modo online/multiplayer

---

## **👥 Contribuições**

Para colaborar com este projeto, **todos os commits devem ser assinados** (GPG ou SSH).  
Isso garante a autenticidade e segurança das contribuições.

Veja como assinar seus commits na [documentação oficial do GitHub](https://docs.github.com/pt/authentication/managing-commit-signature-verification/signing-commits).

**Pull requests sem commits assinados não serão aceitos.**

---

## **📄 Licença**

Este projeto é desenvolvido para fins educacionais como parte da disciplina de Projeto de Software.

# **Pandemic - Visão Geral do Projeto**

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

## **📋 Requisitos Funcionais**

### **1. Gerenciamento do Tabuleiro e Componentes**

-   Representação das **48 cidades** e suas conexões.
-   Controle de **cubos de doença** (máximo de 3 por cidade).
-   Marcadores de **surtos, velocidade de infecção e curas**.

### **2. Controle do Fluxo do Jogo**

-   **Turnos** com 4 ações por jogador.
-   **Fases**: Ações do jogador, compra de cartas e infecção de cidades.
-   Verificação automática de **condições de vitória/derrota**.

### **3. Sistema de Movimento**

-   **Movimentação de jogadores entre cidades** (viagens normais, voos diretos/fretados e ponte aérea).

### **4. Limpeza de Cidades Infectadas**

-   **Remoção de zumbis** em cidades infectadas.

### **5. Construção de Bases de Sobrevivência**

-   **Construção de bases** para facilitar o combate à infecção.

### **6. Compartilhamento de Cartas**

-   **Troca de cartas** entre jogadores para facilitar a descoberta de curas.

### **7. Mecânica de Infecção e Surtos**

-   **Espalhamento da infecção zumbi** com base na taxa de infecção atual.
-   **Surtos em cadeia** (quando uma cidade com 3 cubos recebe mais um).

### **8. Fases de Epidemia**

-   **Epidemias** que aumentam a taxa de infecção e intensificam os surtos.

### **9. Descoberta de Curas**

-   **5 cartas da mesma cor** (ou 4 para o Cientista) em um centro de pesquisa.
-   **Doenças erradicadas** (se todos os cubos forem removidos após a cura).

### **10. Habilidades Especiais dos Personagens**

-   **Médico**: Remove todos os cubos de uma doença de uma cidade.
-   **Pesquisadora**: Pode compartilhar qualquer carta de cidade.
-   **Especialista em Operações**: Constrói centros de pesquisa sem descartar cartas.

### **11. Gerenciamento de Cartas**

-   **Baralho de Jogador** (cartas de cidade, evento e epidemia).
-   **Baralho de Infecção** (cartas que determinam onde as doenças se espalham).

### **12. Eventos Especiais**

-   **Cartas de Evento** (ações extras como "Voo Charter" ou "Quarentena").

---

## **⚙️ Requisitos Não Funcionais**

### **1. Interface de Usuário (UI)**

-   **Intuitiva e responsiva**, com representação visual do tabuleiro e cartas.
-   **Indicadores claros** de surtos, infecção e curas.

### **2. Desempenho**

-   **Processamento rápido** de ações e surtos em cadeia.
-   **Salvamento de partida** para continuar depois.

### **3. Regras e Validações**

-   **Verificação automática** de ações inválidas (ex.: movimento impossível).
-   **Feedback claro** sobre erros (ex.: "Não há cubos suficientes para um surto").

### **4. Multiplayer**

-   **Suporte a 2-4 jogadores** (local ou online).
-   **Sistema de turnos** bem definido.

### **5. Dificuldade Ajustável**

-   **Níveis de dificuldade** (Iniciante, Padrão, Heróico) variando o número de cartas de Epidemia.


## **📚 Documentação do Projeto**

[Documentação](docs/START.md) de como instalar e jogar.

---

## **🛠️ Implementações Iniciais**

As seguintes funcionalidades já foram implementadas na primeira versão do projeto:

-   Movimentação de jogadores entre cidades.
-   Limpeza de cidades infectadas (remoção de zumbis).
-   Construção de bases de sobrevivência.
-   Compartilhamento de cartas entre jogadores.
-   Mecanismo de espalhamento da infecção zumbi.
-   Fases de epidemia e surtos.
-   Verificação de condições de vitória ou derrota.

---

## **🏛️ Padrões de Projeto Utilizados**

### **GRASP**

-   **Creator (Criador):** O padrão Creator recomenda que uma classe crie instâncias de objetos que ela contém ou usa fortemente. Isso é respeitado ao fazer a Partida conter e gerenciar a criação de: `Jogadores`, `Baralhos de cartas`, `Turnos` e `Tabuleiro`.
-   **Information Expert (Especialista da Informação):** As responsabilidades estão atribuídas às classes que possuem a informação necessária para executá-las. Por exemplo, `Cidade` manipula seus próprios cubos, o que é exatamente o objetivo deste padrão.
-   **Controller:** `Partida` atua como um controlador do sistema, coordenando a lógica principal do jogo, enquanto `Turno` gerencia as transições entre as fases, alinhado ao papel de controlador de um caso de uso.
-   **Polymorphism (Polimorfismo):** Permite que cada `Personagem` ou `Carta` implemente sua lógica específica, como `habilidadeEspecial()` ou `ativar()`, sem alterar o código do chamador.
-   **Low Coupling (Baixo Acoplamento):** Uso de enums (`CorDoenca`, `TipoCartaJogador`, etc.) reduz dependência entre objetos, e `Baralho<T>` é genérico e reutilizável.
-   **High Cohesion (Alta Coesão):** Cada classe possui responsabilidades bem definidas e focadas: `CartaEvento` trata exclusivamente eventos, `CartaEpidemia` lida apenas com a lógica de epidemia, `Turno` gerencia somente as fases do turno e `Cidade` é responsável pela manipulação das doenças em seu contexto.

### **GoF**

-   **Strategy:** Permite definir uma família de algoritmos, encapsulá-los e torná-los intercambiáveis, facilitando a escolha dinâmica de comportamentos no jogo.  
    No projeto, o método `habilidadeEspecial()` de `Personagem` pode receber diferentes estratégias de habilidade, permitindo que cada personagem tenha um comportamento especial distinto. Da mesma forma, o método `ativar()` em `CartaEvento` pode aplicar diferentes efeitos de forma intercambiável. Isso é possível ao utilizar interfaces como `IEfeitoEvento` ou `IHabilidade`, tornando fácil plugar novos comportamentos e estratégias conforme necessário.

---

## **📊 Diagramas**

-   **Diagrama de Classes** ([Diagrama de Classes](./docs/diagram/class/pandemic_class_diagram.png))
-   **Diagrama de Comunicação** ([Diagrama de Comunicação - Mover](./docs/diagram/communication/pandemic_comunication_diagram_move.png))
-   **Diagrama de Sequência** ([Diagrama de Sequência - Mover](./docs/diagram/sequence/pandemic_sequence_diagram_move.png))

> Foram elaborados diagramas de comunicação e de sequência para ilustrar o fluxo de mensagens e interações entre os objetos durante o turno básico do jogo, facilitando o entendimento da dinâmica entre as classes principais.

---

## **📅 Próximas Etapas**

-   Desenvolver UI interativa (Fase 3)
-   Testes e balanceamento de regras

---

## **👥 Contribuições**

-   Em desenvolvimento

---

**Desenvolvido por:** Carlos Eduardo, Erivelton Campos, Gabriel Pinho, João Pedro Barboza, Leonardo Lima, Pedro Mileipp  
**Disciplina:** Projeto de Software  
**Professor:** João Felipe Nicolaci

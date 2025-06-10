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

[Documentação](docs/start.md) de como instalar e jogar.

---

## **📜 README do Projeto**

```markdown
# 🦠 Pandemic - Jogo de Tabuleiro Digital

**Desenvolvido por:** Carlos Eduardo, Erivelton Campos, Gabriel Pinho, João Pedro Barboza, Leonardo Lima, Pedro Mileipp  
**Disciplina:** Projeto de Software  
**Professor:** João Felipe Nicolaci

## 🎮 Sobre o Jogo

Pandemic é um jogo cooperativo onde os jogadores controlam especialistas em saúde tentando curar quatro doenças antes que elas causem um colapso global. O jogo requer estratégia, planejamento em equipe e gerenciamento de recursos.

## 🛠️ Funcionalidades que serão implementadas

✔️ **Movimentação de jogadores entre cidades**  
✔️ **Limpeza de cidades infectadas (remoção de zumbis)**  
✔️ **Construção de bases de sobrevivência**  
✔️ **Compartilhamento de cartas entre jogadores**  
✔️ **Mecanismo de espalhamento da infecção zumbi**  
✔️ **Fases de epidemia e surtos**  
✔️ **Verificação de condições de vitória ou derrota**

## 📋 Requisitos

-   Em desenvolvimento

## 📊 Diagramas (Fase 1)

-   **Diagrama de Classes** (Visual Paradigm)
-   **Diagrama de Comunicação** (Turno básico)

## 📅 Próximas Etapas

-   Implementar **padrões GRASP/GoF** (Fase 2)
-   Desenvolver **UI interativa** (Fase 3)
-   Testes e balanceamento de regras

## 👥 Contribuições

-   Em desenvolvimento

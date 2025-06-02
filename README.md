# Pandemic (Trabalho de Programação de Software)

Este projeto é uma implementação simplificada do jogo de tabuleiro Pandemic, utilizando Python 3.11 e a biblioteca gráfica `pygame` para visualização do tabuleiro e das ações dos jogadores.

## Estrutura do Projeto

```
app/
  main.py
  src/
    board.py
    city.py
    graph_gui.py
    player.py
```

- `main.py`: Ponto de entrada do jogo, gerencia o loop principal, entrada dos jogadores e integração com a interface gráfica.
- `src/board.py`: Lógica do tabuleiro, cidades, infecção e condições de vitória/derrota.
- `src/city.py`: Representação das cidades, conexões e infecções.
- `src/player.py`: Lógica dos jogadores e suas ações.
- `src/graph_gui.py`: Interface gráfica usando `pygame`.

## Requisitos

- Python 3.11
- [pygame](https://www.pygame.org/) >= 2.6.1
- [uv](https://github.com/astral-sh/uv) (gerenciador de ambientes e dependências)

## Instalação e Execução

Este projeto recomenda o uso do [uv](https://github.com/astral-sh/uv) para instalar dependências e rodar o ambiente de forma rápida e eficiente.

### Passos para rodar o projeto

1. **Instale o uv** (caso ainda não tenha):

   ```sh
   pip install uv
   ```

2. **Instale as dependências**:

   ```sh
   uv pip install -r pyproject.toml
   ```

   Ou, para instalar e criar o ambiente virtual automaticamente:

   ```sh
   uv venv
   uv pip install -r pyproject.toml
   ```

3. **Execute o jogo**:

   ```sh
   uv run app/main.py
   ```

   Ou, se estiver usando um ambiente virtual ativado:

   ```sh
   python app/main.py
   ```

## Sobre o uv

O [uv](https://github.com/astral-sh/uv) é um gerenciador de ambientes e dependências para Python, muito mais rápido que o pip tradicional. Ele facilita a criação de ambientes virtuais e a instalação de pacotes, tornando o setup do projeto mais ágil e confiável.

**Recomendamos fortemente o uso do uv para garantir reprodutibilidade e velocidade na instalação das dependências.**

## Como Jogar

- O jogo é iniciado no terminal, onde você define o número de jogadores e seus nomes.
- As ações dos jogadores são feitas pelo terminal, enquanto o estado do tabuleiro é exibido graficamente via pygame.
- O objetivo é tratar todas as doenças antes que ocorram muitos surtos.

## Licença

Este projeto é apenas para fins educacionais.
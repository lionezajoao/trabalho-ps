# Earned Value Management (EVM) - Projeto Pandemic

## Definições das Métricas

### Valores Base

-   **PV (Planned Value)**: Valor planejado do trabalho que deveria estar completo
-   **EV (Earned Value)**: Valor do trabalho realmente completado
-   **AC (Actual Cost)**: Custo real do trabalho realizado
-   **BAC (Budget at Completion)**: Orçamento total do projeto (120h)

### Índices de Performance

-   **CPI (Cost Performance Index)**: EV / AC

    -   CPI > 1.0: Abaixo do orçamento
    -   CPI = 1.0: No orçamento
    -   CPI < 1.0: Acima do orçamento

-   **SPI (Schedule Performance Index)**: EV / PV
    -   SPI > 1.0: Adiantado
    -   SPI = 1.0: No cronograma
    -   SPI < 1.0: Atrasado

### Variações

-   **CV (Cost Variance)**: EV - AC
-   **SV (Schedule Variance)**: EV - PV

### Projeções

-   **EAC (Estimate at Completion)**: AC + ETC
-   **ETC (Estimate to Complete)**: (BAC - EV) / CPI
-   **VAC (Variance at Completion)**: BAC - EAC

## Análise do Projeto

### Performance Geral

-   **CPI Final**: 1.00 (Excelente controle de custos)
-   **SPI Final**: 1.00 (Cronograma recuperado)
-   **Eficiência**: 100% (120h planejadas = 120h executadas)

### Fases do Projeto

#### Fase 1: Sprint 1 (Semana 1)

-   **SPI**: 1.25 - Adiantado no cronograma
-   **CPI**: 1.00 - No orçamento
-   **Status**: Início forte com documentação e estrutura

#### Fase 2: Intervalo (Semanas 2-5)

-   **SPI**: 0.25-0.42 - Significativamente atrasado
-   **CPI**: 1.00 - Mantido no orçamento
-   **Status**: Período de baixa atividade

#### Fase 3: Desenvolvimento (Semanas 6-8)

-   **SPI**: 0.36-0.67 - Recuperação gradual
-   **CPI**: 1.00 - Controle de custos mantido
-   **Status**: Retomada das atividades

#### Fase 4: Finalização (Semanas 11-12)

-   **SPI**: 0.90-1.00 - Recuperação completa
-   **CPI**: 1.00 - Orçamento mantido
-   **Status**: Sprint final eficiente

### Lições Aprendidas

#### Pontos Positivos

1. **Controle de Custos**: CPI mantido em 1.00 durante todo o projeto
2. **Recuperação**: Capacidade de acelerar trabalho nos sprints finais
3. **Qualidade**: 50 commits organizados e bem documentados

#### Pontos de Melhoria

1. **Distribuição**: Trabalho muito concentrado em períodos específicos
2. **Regularidade**: Longos intervalos sem atividade
3. **Monitoramento**: Necessidade de acompanhamento mais frequente

### Recomendações para Projetos Futuros

1. **Estabelecer check-ins semanais** para evitar longos períodos de inatividade
2. **Implementar alertas de cronograma** quando SPI < 0.8
3. **Distribuir trabalho** de forma mais uniforme ao longo do tempo
4. **Manter documentação** de EVM atualizada semanalmente

## Fórmulas Utilizadas

```
CPI = EV / AC
SPI = EV / PV
CV = EV - AC
SV = EV - PV
EAC = AC + ETC
ETC = (BAC - EV) / CPI
VAC = BAC - EAC
TCPI = (BAC - EV) / (BAC - AC)
```

## Gráficos Sugeridos

1. **Gráfico de EVM**: PV, EV, AC ao longo do tempo
2. **Índices de Performance**: CPI e SPI por sprint
3. **Variações**: CV e SV acumuladas
4. **Projeções**: EAC vs BAC

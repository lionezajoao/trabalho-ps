# Testando GitHub Actions Localmente

Este diretório contém ferramentas e configurações para testar os GitHub Actions do projeto localmente usando o **act**.

## Arquivos de Configuração

-   `.actrc` - Configurações padrão do act
-   `.env.act` - Variáveis de ambiente para execução local
-   `test-actions.sh` - Script de conveniência para executar testes
-   `docs/TESTING_WITH_ACT.md` - Documentação completa

## Início Rápido

### 1. Instalar Pré-requisitos

```bash
# Instalar Docker (Ubuntu/Debian)
sudo apt update && sudo apt install docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER

# Instalar act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Logout e login novamente para aplicar permissões do Docker
```

### 2. Verificar Instalação

```bash
./test-actions.sh check
```

### 3. Executar Testes

```bash
# Teste rápido (apenas Ubuntu)
./test-actions.sh ubuntu

# Teste completo (todos os OS)
./test-actions.sh full

# Listar workflows
./test-actions.sh list

# Ver ajuda
./test-actions.sh help
```

## Comandos Úteis

```bash
# Executar workflow específico
act -j build

# Executar apenas para Ubuntu
act -j build --matrix os:ubuntu-latest

# Dry run (não executa)
act -n

# Verbose output
act -v

# Listar workflows
act -l
```

## Troubleshooting

### Docker não está rodando

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Permissão negada para Docker

```bash
sudo usermod -aG docker $USER
# Logout e login novamente
```

### act não encontrado

```bash
# Reinstalar act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Workflow falha em steps específicos

-   Verifique se todas as dependências estão disponíveis no container
-   Use `act -v` para ver logs detalhados
-   Teste steps individuais com `./test-actions.sh step "nome-do-step"`

## Limitações

-   O act simula apenas runners Linux
-   Alguns resources específicos do GitHub podem não estar disponíveis
-   Performance pode ser diferente do ambiente real do GitHub

Para mais detalhes, consulte `docs/TESTING_WITH_ACT.md`.

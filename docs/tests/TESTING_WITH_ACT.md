# Testando GitHub Actions com act

Este guia explica como usar o `act` para testar os workflows do GitHub Actions localmente.

## Pré-requisitos

1. **Docker**: O act usa Docker para simular os runners do GitHub Actions
2. **act**: Ferramenta para executar GitHub Actions localmente

## ⚠️ Importante: Ambiente Flatpak

Se você está usando VS Code como Flatpak (como detectado), você precisará:

1. **Instalar Docker no sistema host** (não dentro do Flatpak)
2. **Dar permissões ao Flatpak** para acessar o Docker
3. **Usar comandos específicos** para Flatpak

### Verificar se está em Flatpak

```bash
echo $FLATPAK_ID
# Se retornar algo como com.visualstudio.code, você está em Flatpak
```

## Instalação

### 1. Instalar Docker

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Fedora/RHEL
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Arch Linux
sudo pacman -S docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 2. Instalar act

```bash
# Usando curl (recomendado)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Ou usando package manager específico
# Ubuntu/Debian
sudo apt install act

# Arch Linux
yay -S act

# macOS
brew install act
```

### 3. Instalação em Ambiente Flatpak (VS Code Flatpak)

Se você está usando VS Code como Flatpak, siga estes passos:

#### 3.1. Instalar Docker no Sistema Host

```bash
# Abrir terminal do sistema (não do VS Code)
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Fedora
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

#### 3.2. Dar Permissões ao Flatpak

```bash
# Permitir acesso ao Docker socket
sudo flatpak override --system --socket=session-bus com.visualstudio.code
sudo flatpak override --system --filesystem=/var/run/docker.sock com.visualstudio.code

# Ou para usuário específico
flatpak override --user --filesystem=/var/run/docker.sock com.visualstudio.code
```

#### 3.3. Instalar act no Sistema Host

```bash
# No terminal do sistema (não VS Code)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

#### 3.4. Criar Wrapper para act no Flatpak

Crie um script wrapper que será usado dentro do VS Code:

```bash
# Criar diretório para scripts locais (se não existir)
mkdir -p ~/.local/bin

# Criar wrapper para act
cat > ~/.local/bin/act << 'EOF'
#!/bin/bash
flatpak-spawn --host act "$@"
EOF

# Tornar executável
chmod +x ~/.local/bin/act

# Criar wrapper para docker
cat > ~/.local/bin/docker << 'EOF'
#!/bin/bash
flatpak-spawn --host docker "$@"
EOF

# Tornar executável
chmod +x ~/.local/bin/docker
```

#### 3.5. Adicionar ao PATH

Adicione ao seu `~/.bashrc` ou `~/.profile`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

E reinicie o terminal ou execute:

```bash
source ~/.bashrc
```

## Configuração

### 1. Criar arquivo .actrc (opcional)

Crie um arquivo `.actrc` na raiz do projeto para configurações personalizadas:

```
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-22.04=catthehacker/ubuntu:act-22.04
-P ubuntu-20.04=catthehacker/ubuntu:act-20.04
--container-architecture linux/amd64
```

### 2. Criar arquivo .secrets (se necessário)

Se o workflow usar secrets, crie um arquivo `.secrets`:

```
GITHUB_TOKEN=seu_token_aqui
```

## Comandos Básicos do act

### Listar todos os workflows

```bash
act -l
```

### Executar todos os jobs

```bash
act
```

### Executar um job específico

```bash
act -j build
```

### Executar com um evento específico

```bash
# Push event
act push

# Pull request event
act pull_request
```

### Executar apenas um step específico

```bash
act -j build --matrix os:ubuntu-latest
```

### Executar com variáveis de ambiente

```bash
act -s GITHUB_TOKEN=your_token --env-file .env
```

### Executar com verbose output

```bash
act -v
```

### Executar sem realmente executar (dry run)

```bash
act -n
```

## Testando o Workflow do Projeto

Para testar o workflow `build.yaml` do projeto:

```bash
# Executar o workflow completo
act

# Executar apenas o job build
act -j build

# Executar apenas para Ubuntu (mais rápido para testes)
act -j build --matrix os:ubuntu-latest

# Executar com verbose para debug
act -j build --matrix os:ubuntu-latest -v
```

## Limitações do act

1. **Matriz de OS**: O act roda apenas em containers Linux, então os jobs para Windows e macOS podem não funcionar exatamente igual
2. **Actions específicas**: Algumas actions podem não funcionar perfeitamente em ambiente local
3. **Recursos**: Algumas funcionalidades específicas do GitHub podem não estar disponíveis

## Dicas e Boas Práticas

### 1. Use imagens Docker apropriadas

O act usa imagens Docker para simular os runners. Use imagens específicas para melhor compatibilidade:

```bash
act -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

### 2. Configure o ACT environment variable

No workflow, você pode detectar quando está rodando no act:

```yaml
env:
    ACT: ""

steps:
    - name: Skip on act
      if: ${{ env.ACT != 'true' }}
      run: echo "This step runs only on GitHub"
```

### 3. Use arquivo de configuração

Crie `.actrc` para evitar repetir parâmetros:

```
-P ubuntu-latest=catthehacker/ubuntu:act-latest
--container-architecture linux/amd64
-v
```

### 4. Teste incrementalmente

Comece testando jobs individuais antes do workflow completo:

```bash
# Teste step por step
act -j build --matrix os:ubuntu-latest -s

# Se funcionar, teste o workflow completo
act
```

## Troubleshooting

### Erro: "Cannot connect to Docker daemon"

```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
# Logout e login novamente
```

### Erro: "No such file or directory"

Certifique-se de estar na raiz do projeto onde está o `.github/workflows/`

### Performance lenta

```bash
# Use apenas Ubuntu para testes rápidos
act -j build --matrix os:ubuntu-latest

# Ou use imagens menores
act -P ubuntu-latest=node:16-alpine
```

### Actions não encontradas

```bash
# Force pull das actions
act --pull
```

## Exemplo Prático

Para testar o workflow deste projeto:

```bash
# 1. Navegue até a raiz do projeto
cd /media/carloseduardo/Backup/Github/trabalho-ps

# 2. Liste os workflows disponíveis
act -l

# 3. Execute o job build apenas para Ubuntu (mais rápido)
act -j build --matrix os:ubuntu-latest

# 4. Se quiser ver todos os detalhes
act -j build --matrix os:ubuntu-latest -v

# 5. Para testar o workflow completo (demora mais)
act
```

## Referencias

-   [Documentação oficial do act](https://github.com/nektos/act)
-   [Imagens Docker para act](https://github.com/catthehacker/docker_images)
-   [GitHub Actions documentation](https://docs.github.com/en/actions)

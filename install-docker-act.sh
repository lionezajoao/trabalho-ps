#!/bin/bash

# Script para instalar Docker e act em ambiente Flatpak
# Este script deve ser executado FORA do VS Code Flatpak

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detectar distribuição
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    else
        print_error "Não foi possível detectar a distribuição Linux"
        exit 1
    fi
    
    print_info "Distribuição detectada: $PRETTY_NAME"
}

# Verificar se está sendo executado como root
check_not_root() {
    if [ "$EUID" -eq 0 ]; then
        print_error "Não execute este script como root (sudo)"
        print_info "O script usará sudo quando necessário"
        exit 1
    fi
}

# Verificar se está em ambiente Flatpak
check_flatpak_env() {
    if [ -n "$FLATPAK_ID" ]; then
        print_error "Este script deve ser executado FORA do ambiente Flatpak"
        print_info "Abra um terminal do sistema (não do VS Code) e execute este script"
        exit 1
    fi
    print_success "Executando fora do ambiente Flatpak"
}

# Instalar Docker
install_docker() {
    print_info "Instalando Docker..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y docker.io
            ;;
        fedora)
            sudo dnf install -y docker
            ;;
        arch)
            sudo pacman -S --noconfirm docker
            ;;
        *)
            print_warning "Distribuição não reconhecida. Tentando instalação genérica..."
            if command -v apt > /dev/null; then
                sudo apt update && sudo apt install -y docker.io
            elif command -v dnf > /dev/null; then
                sudo dnf install -y docker
            elif command -v pacman > /dev/null; then
                sudo pacman -S --noconfirm docker
            else
                print_error "Gerenciador de pacotes não suportado"
                exit 1
            fi
            ;;
    esac
    
    print_success "Docker instalado"
}

# Configurar Docker
configure_docker() {
    print_info "Configurando Docker..."
    
    # Iniciar e habilitar serviço
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Adicionar usuário ao grupo docker
    sudo usermod -aG docker $USER
    
    print_success "Docker configurado"
    print_warning "Você precisará fazer logout e login novamente para usar Docker sem sudo"
}

# Instalar act
install_act() {
    print_info "Instalando act..."
    
    # Baixar e instalar act
    curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
    
    if command -v act > /dev/null; then
        print_success "act instalado: $(act --version)"
    else
        print_error "Falha na instalação do act"
        exit 1
    fi
}

# Configurar permissões Flatpak
configure_flatpak_permissions() {
    print_info "Configurando permissões do Flatpak..."
    
    # Verificar se o VS Code Flatpak está instalado
    if flatpak list | grep -q com.visualstudio.code; then
        print_info "VS Code Flatpak encontrado. Configurando permissões..."
        
        # Dar acesso ao socket do Docker
        sudo flatpak override --system --filesystem=/var/run/docker.sock com.visualstudio.code
        
        print_success "Permissões do Flatpak configuradas"
    else
        print_warning "VS Code Flatpak não encontrado. Pulando configuração de permissões."
    fi
}

# Criar wrappers
create_wrappers() {
    print_info "Criando scripts wrapper..."
    
    # Criar diretório se não existir
    mkdir -p ~/.local/bin
    
    # Wrapper para docker
    cat > ~/.local/bin/docker << 'EOF'
#!/bin/bash
flatpak-spawn --host docker "$@"
EOF
    chmod +x ~/.local/bin/docker
    
    # Wrapper para act
    cat > ~/.local/bin/act << 'EOF'
#!/bin/bash
flatpak-spawn --host act "$@"
EOF
    chmod +x ~/.local/bin/act
    
    print_success "Wrappers criados em ~/.local/bin/"
}

# Configurar PATH
configure_path() {
    print_info "Configurando PATH..."
    
    # Verificar se ~/.local/bin já está no PATH
    if echo "$PATH" | grep -q "$HOME/.local/bin"; then
        print_info "~/.local/bin já está no PATH"
    else
        # Adicionar ao .bashrc se existir
        if [ -f ~/.bashrc ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
            print_info "PATH adicionado ao ~/.bashrc"
        fi
        
        # Adicionar ao .profile se existir
        if [ -f ~/.profile ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
            print_info "PATH adicionado ao ~/.profile"
        fi
    fi
    
    print_success "PATH configurado"
}

# Testar instalação
test_installation() {
    print_info "Testando instalação..."
    
    # Testar Docker
    if sudo docker run --rm hello-world > /dev/null 2>&1; then
        print_success "Docker funcionando corretamente"
    else
        print_warning "Docker instalado mas pode precisar de reinicialização"
    fi
    
    # Testar act
    if act --version > /dev/null 2>&1; then
        print_success "act funcionando: $(act --version)"
    else
        print_warning "act instalado mas pode não estar no PATH"
    fi
}

# Mostrar próximos passos
show_next_steps() {
    print_info "Instalação concluída!"
    echo ""
    print_warning "PRÓXIMOS PASSOS:"
    echo "1. Faça logout e login novamente (ou reinicie o sistema)"
    echo "2. Abra o VS Code Flatpak"
    echo "3. No terminal do VS Code, execute: ./test-actions.sh check"
    echo "4. Se tudo estiver OK, execute: ./test-actions.sh ubuntu"
    echo ""
    print_info "Para testar agora (com sudo):"
    echo "sudo docker run --rm hello-world"
    echo "act --version"
}

# Main
main() {
    echo "=================================="
    echo "Instalador Docker + act (Flatpak)"
    echo "=================================="
    echo ""
    
    check_not_root
    check_flatpak_env
    detect_distro
    
    print_info "Este script irá:"
    echo "1. Instalar Docker"
    echo "2. Configurar Docker"
    echo "3. Instalar act"
    echo "4. Configurar permissões Flatpak"
    echo "5. Criar wrappers para uso no VS Code"
    echo ""
    
    read -p "Continuar? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Instalação cancelada"
        exit 0
    fi
    
    install_docker
    configure_docker
    install_act
    configure_flatpak_permissions
    create_wrappers
    configure_path
    test_installation
    show_next_steps
}

main "$@"

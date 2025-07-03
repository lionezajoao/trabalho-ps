#!/bin/bash

# Script para testar GitHub Actions localmente usando act
# Uso: ./test-actions.sh [opções]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
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

# Verificar se o Docker está rodando
check_docker() {
    # Detectar se está em ambiente Flatpak
    if [ -n "$FLATPAK_ID" ]; then
        print_info "Detectado ambiente Flatpak. Tentando acessar Docker do sistema host..."
        if ! flatpak-spawn --host docker info > /dev/null 2>&1; then
            print_error "Docker não está rodando no sistema host ou não está instalado"
            print_info "Para ambiente Flatpak, consulte a seção específica em docs/TESTING_WITH_ACT.md"
            print_info "Resumo rápido:"
            echo "1. Instale Docker no sistema host (fora do Flatpak)"
            echo "2. sudo systemctl start docker"
            echo "3. sudo usermod -aG docker \$USER"
            echo "4. Configure permissões do Flatpak (veja documentação)"
            exit 1
        fi
        print_success "Docker está rodando no sistema host"
    else
        if ! docker info > /dev/null 2>&1; then
            print_error "Docker não está rodando ou não está instalado"
            print_info "Por favor, instale e inicie o Docker antes de continuar"
            exit 1
        fi
        print_success "Docker está rodando"
    fi
}

# Verificar se o act está instalado
check_act() {
    # Detectar se está em ambiente Flatpak
    if [ -n "$FLATPAK_ID" ]; then
        if ! flatpak-spawn --host act --version > /dev/null 2>&1; then
            print_error "act não está instalado no sistema host"
            print_info "Para instalar o act no sistema host, execute no terminal do sistema:"
            echo "curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
            print_info "Ou configure o wrapper conforme documentação em docs/TESTING_WITH_ACT.md"
            exit 1
        fi
        local version=$(flatpak-spawn --host act --version)
        print_success "act está instalado no sistema host ($version)"
    else
        if ! command -v act > /dev/null 2>&1; then
            print_error "act não está instalado"
            print_info "Para instalar o act, execute:"
            echo "curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
            exit 1
        fi
        print_success "act está instalado ($(act --version))"
    fi
}

# Listar workflows disponíveis
list_workflows() {
    print_info "Workflows disponíveis:"
    act -l
}

# Executar testes apenas no Ubuntu (mais rápido)
test_ubuntu() {
    print_info "Executando testes apenas no Ubuntu..."
    act -j build --matrix os:ubuntu-latest
}

# Executar testes completos (todos os OS)
test_full() {
    print_info "Executando testes completos (todos os OS)..."
    print_warning "Isso pode demorar bastante..."
    act
}

# Executar apenas um step específico
test_step() {
    local step_name="$1"
    if [ -z "$step_name" ]; then
        print_error "Nome do step é obrigatório"
        print_info "Uso: $0 step 'nome-do-step'"
        exit 1
    fi
    
    print_info "Executando step: $step_name"
    act -j build --matrix os:ubuntu-latest -s "$step_name"
}

# Dry run (não executa, apenas mostra o que seria executado)
dry_run() {
    print_info "Executando dry run..."
    act -n
}

# Executar com debug verbose
test_verbose() {
    print_info "Executando com output verbose..."
    act -j build --matrix os:ubuntu-latest -v
}

# Mostrar ajuda
show_help() {
    echo "Script para testar GitHub Actions localmente"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  check        - Verificar pré-requisitos (Docker e act)"
    echo "  list         - Listar workflows disponíveis"
    echo "  ubuntu       - Executar testes apenas no Ubuntu (rápido)"
    echo "  full         - Executar testes completos (lento)"
    echo "  verbose      - Executar com output detalhado"
    echo "  dry          - Dry run (não executa, apenas mostra)"
    echo "  step <nome>  - Executar um step específico"
    echo "  help         - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 check"
    echo "  $0 ubuntu"
    echo "  $0 step 'Run tests'"
    echo ""
    echo "Pré-requisitos:"
    echo "  - Docker instalado e rodando"
    echo "  - act instalado"
    echo ""
    echo "Para instalar act:"
    echo "  curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
}

# Main
main() {
    case "${1:-help}" in
        "check")
            check_docker
            check_act
            print_success "Todos os pré-requisitos estão OK!"
            ;;
        "list")
            check_docker
            check_act
            list_workflows
            ;;
        "ubuntu")
            check_docker
            check_act
            test_ubuntu
            ;;
        "full")
            check_docker
            check_act
            test_full
            ;;
        "verbose")
            check_docker
            check_act
            test_verbose
            ;;
        "dry")
            check_docker
            check_act
            dry_run
            ;;
        "step")
            check_docker
            check_act
            test_step "$2"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Executar função principal
main "$@"

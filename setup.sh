#!/bin/bash

# LLM Backend Playground Setup Script
# This script installs all prerequisites needed to run the project

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            echo "ubuntu"
        elif command_exists yum; then
            echo "centos"
        elif command_exists dnf; then
            echo "fedora"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Function to install Python
install_python() {
    local os=$(detect_os)
    
    # Check if Python 3.13 is already installed (regardless of what python3 points to)
    if command_exists python3.13; then
        print_success "Python 3.13 is already installed"
        
        # Check if python3 command points to 3.13
        if command_exists python3; then
            local current_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
            if [[ "$current_version" != "3.13" ]]; then
                print_status "Updating python3 alternative to point to Python 3.13..."
                sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
                sudo update-alternatives --set python3 /usr/bin/python3.13
                print_success "python3 now points to Python 3.13"
                
                # Verify the change
                local new_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
                if [[ "$new_version" == "3.13" ]]; then
                    print_success "Successfully updated python3 to Python 3.13"
                else
                    print_error "python3 still shows version $new_version. You may need to restart your shell or check for aliases."
                    print_error "Try running: alias python3"
                    exit 1
                fi
            fi
        fi
        return 0
    fi
    
    # Check if any compatible Python version is already the default
    if command_exists python3; then
        local version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
        if [[ "$version" == "3.11" || "$version" == "3.12" || "$version" == "3.13" ]]; then
            print_success "Python $version is already installed and set as default"
            return 0
        fi
    fi
    
    print_status "Installing Python 3.13..."
    
    case $os in
        "ubuntu")
            sudo apt-get update
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.13 python3.13-venv python3.13-dev python3-pip
            sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
            ;;
        "centos"|"fedora")
            sudo dnf install -y python3.13 python3.13-pip python3.13-devel
            ;;
        "macos")
            if command_exists brew; then
                brew install python@3.13
            else
                print_error "Homebrew not found. Please install Homebrew first: https://brew.sh/"
                return 1
            fi
            ;;
        *)
            print_error "Unsupported OS: $os"
            return 1
            ;;
    esac
    
    print_success "Python 3.13 installed successfully"
}

# Function to install Docker
install_docker() {
    if command_exists docker; then
        print_success "Docker is already installed"
        return 0
    fi
    
    print_status "Installing Docker..."
    
    local os=$(detect_os)
    
    case $os in
        "ubuntu")
            # Remove old versions
            sudo apt-get remove -y docker docker-engine docker.io containerd runc || true
            
            # Install prerequisites
            sudo apt-get update
            sudo apt-get install -y ca-certificates curl gnupg lsb-release
            
            # Add Docker's official GPG key
            sudo mkdir -p /etc/apt/keyrings
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
            
            # Set up repository
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            
            # Install Docker
            sudo apt-get update
            sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            
            # Add user to docker group
            sudo usermod -aG docker $USER
            ;;
        "centos"|"fedora")
            sudo dnf install -y docker
            sudo systemctl start docker
            sudo systemctl enable docker
            sudo usermod -aG docker $USER
            ;;
        "macos")
            if command_exists brew; then
                brew install --cask docker
            else
                print_error "Homebrew not found. Please install Docker Desktop manually: https://www.docker.com/products/docker-desktop/"
                return 1
            fi
            ;;
        *)
            print_error "Unsupported OS: $os"
            return 1
            ;;
    esac
    
    print_success "Docker installed successfully"
    print_warning "You may need to log out and back in for Docker group changes to take effect"
}

# Function to install curl (needed for health checks)
install_curl() {
    if command_exists curl; then
        print_success "curl is already installed"
        return 0
    fi
    
    print_status "Installing curl..."
    
    local os=$(detect_os)
    
    case $os in
        "ubuntu")
            sudo apt-get update && sudo apt-get install -y curl
            ;;
        "centos"|"fedora")
            sudo dnf install -y curl
            ;;
        "macos")
            if command_exists brew; then
                brew install curl
            else
                print_warning "curl should be available by default on macOS"
            fi
            ;;
    esac
    
    print_success "curl installed successfully"
}

# Function to setup Python virtual environment
setup_venv() {
    if [[ -d "venv" ]]; then
        print_status "Virtual environment already exists"
    else
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    print_status "Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Python dependencies installed"
}

# Function to build Docker image
build_docker() {
    if command_exists docker; then
        print_status "Building Docker image..."
        docker build -t llm-be-playground .
        print_success "Docker image built successfully"
        
        # Test docker compose command
        if docker compose version >/dev/null 2>&1; then
            print_success "Docker Compose is available"
        else
            print_warning "Docker Compose not available, you may need to install it separately"
        fi
    else
        print_warning "Docker not available, skipping Docker build"
    fi
}

# Main setup function
main() {
    print_status "Starting LLM Backend Playground setup..."
    
    # Check if running as root
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        exit 1
    fi
    
    # Install prerequisites
    install_python
    install_curl
    install_docker
    
    # Setup Python environment
    setup_venv
    
    # Build Docker image if Docker is available
    build_docker
    
    print_success "Setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "  1. For local development: make dev"
    echo "  2. For Docker: make docker-run"
    echo "  3. To stop Docker: make docker-stop"
    echo ""
    print_warning "If you installed Docker, you may need to log out and back in for group changes to take effect"
}

# Run main function
main "$@" 
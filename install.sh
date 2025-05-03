#!/data/data/com.termux/files/usr/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

# Banner do instalador
echo -e "\e[1;32m"
cat << "EOF"
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
EOF
echo -e "\e[0m"

echo -e "\e[1;34m🚀 WOLF TOOLS - INSTALADOR AUTOMÁTICO 🔥"
echo -e "🛠️ By: jottap_62 | 🐍 Python Power 🐙\e[0m"
echo ""
sleep 1

echo -e "${YELLOW}[1/9] Atualizando Termux...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[2/9] Instalando pacotes do sistema...${NC}"
pkg install -y python git curl wget zip unzip

echo -e "${YELLOW}[3/9] Atualizando pip...${NC}"
pip install --upgrade pip

echo -e "${YELLOW}[4/9] Instalando dependências Python...${NC}"

# Lista de dependências
deps=("colorama" "tqdm" "python-dotenv" "requests" "pygithub")
for package in "${deps[@]}"; do
    echo -e "${BLUE}>> Instalando $package...${NC}"
    pip install "$package"
    version=$(pip show "$package" 2>/dev/null | grep -i version | awk '{print $2}')
    echo -e "${GREEN}✓ $package versão $version instalada${NC}"
    sleep 0.5
done

echo -e "${YELLOW}[5/9] Criando diretório ~/wolf_tools (se não existir)...${NC}"
mkdir -p ~/wolf_tools

echo -e "${YELLOW}[6/9] TUTORIAL: Como criar um GitHub Token${NC}"
echo -e "${BLUE}1. Acesse: https://github.com/settings/tokens"
echo -e "2. Clique em: 'Generate new token (classic)'"
echo -e "3. Marque: 'repo' e 'read:org'"
echo -e "4. Copie o token gerado"
echo -e "5. Cole abaixo quando solicitado${NC}"
sleep 6

echo -e "${YELLOW}[7/9] Solicitação do token...${NC}"
read -p "Digite seu GitHub Token: " GITHUB_TOKEN
echo "GITHUB_TOKEN=$GITHUB_TOKEN" > ~/wolf_tools/.env
echo -e "${GREEN}✓ Token salvo com sucesso em ~/wolf_tools/.env${NC}"

echo -e "${YELLOW}[8/9] Criando alias 'wolf' para execução rápida...${NC}"
echo 'alias wolf="cd ~/wolf_tools && python wolf-tools.py"' >> ~/.bashrc
source ~/.bashrc

echo -e "${YELLOW}[9/9] Instalação finalizada com sucesso!${NC}"
echo -e "${BLUE}Lembre-se de mover seu arquivo 'wolf-tools.py' para: ~/wolf_tools/"
echo -e "Use o comando: ${GREEN}wolf${BLUE} para iniciar a ferramenta.${NC}"

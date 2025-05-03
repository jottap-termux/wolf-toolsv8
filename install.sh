#!/bin/bash

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
echo -e "\e[1;31m\"Somos numerosos. Nós não esquecemos. Nós não perdoamos. Esperem por nós\"\e[0m"
echo ""

# Verificar e instalar Python e pip se necessário
echo -e "\e[1;33m[+] Verificando dependências básicas...\e[0m"
if ! command -v python3 &> /dev/null; then
    echo -e "\e[1;32m[*] Instalando Python3...\e[0m"
    pkg install python -y
else
    echo -e "\e[1;32m[✓] Python3 já está instalado.\e[0m"
fi

if ! command -v pip &> /dev/null; then
    echo -e "\e[1;32m[*] Instalando pip...\e[0m"
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
else
    echo -e "\e[1;32m[✓] pip já está instalado.\e[0m"
fi

# Atualizar pip
echo -e "\e[1;32m[*] Atualizando pip...\e[0m"
python -m pip install --upgrade pip

# Instalação das dependências pip
echo -e "\e[1;33m[+] Instalando dependências Python...\e[0m"
pip_packages=(
    "colorama"
    "tqdm"
    "requests"
    "PyGithub"
    "python-dotenv"
)

for pkg in "${pip_packages[@]}"; do
    echo -e "\e[1;32m[*] Instalando $pkg...\e[0m"
    python -m pip install --upgrade $pkg
    if [ $? -eq 0 ]; then
        echo -e "\e[1;32m[✓] $pkg instalado com sucesso!\e[0m"
    else
        echo -e "\e[1;31m[!] Falha ao instalar $pkg\e[0m"
        echo -e "\e[1;33m[*] Tentando instalar com pip3...\e[0m"
        pip3 install --upgrade $pkg
        if [ $? -eq 0 ]; then
            echo -e "\e[1;32m[✓] $pkg instalado com sucesso usando pip3!\e[0m"
        else
            echo -e "\e[1;31m[!] Falha crítica ao instalar $pkg\e[0m"
        fi
    fi
done

echo -e "\e[1;32m\n[+] Todas as dependências foram instaladas com sucesso!\e[0m"
echo -e "\e[1;36mExecute o script principal com: python3 wolf-tools.py\e[0m"

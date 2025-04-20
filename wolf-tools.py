#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import re
import requests
import json
from collections import OrderedDict
from colorama import Fore, Back, Style, init
from tqdm import tqdm
from github import Github
from dotenv import load_dotenv

# Inicialização do colorama
init()

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações globais
LANGUAGE = "pt"  # Idioma padrão: pt (português), en (inglês), es (espanhol)
INSTALL_PATH = os.path.expanduser("~/wolf_tools")  # Diretório de instalação padrão
MENU_SPACE = 2  # Espaçamento no menu
SLEEP_TIME = 2  # Tempo de espera entre operações
LARGURA_MAXIMA = 60  # Largura máxima do menu
THEME = "hacker"  # Tema padrão: hacker, dark, matrix
AUTO_UPDATE = True  # Atualização automática ativada por padrão

# Configurações sensíveis via variáveis de ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print(f"{Fore.RED}❌ ERRO: Token GitHub não encontrado no arquivo .env{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}ℹ️ Crie um arquivo .env com GITHUB_TOKEN=seu_token{Style.RESET_ALL}")
    sys.exit(1)

REPO_NAME = "jottap-termux/wolf-tools-server"  # Repositório de ferramentas
JSON_FILE = "tools.json"  # Arquivo JSON com as ferramentas
REMOTE_JSON_URL = "https://jottap-termux.github.io/wolf-tools-server/tools.json"  # URL do JSON remoto

# Definição de temas
THEMES = {
    "dark": {
        "TITLE": Fore.RED + Style.BRIGHT,
        "TEXT": Fore.WHITE + Style.BRIGHT,
        "WARNING": Fore.YELLOW + Style.BRIGHT,
        "SUCCESS": Fore.GREEN + Style.BRIGHT,
        "OPTION": Fore.CYAN + Style.BRIGHT,
        "BORDER": Fore.RED + Style.BRIGHT
    },
    "hacker": {
        "TITLE": Fore.GREEN + Style.BRIGHT,
        "TEXT": Fore.LIGHTGREEN_EX + Style.BRIGHT,
        "WARNING": Fore.LIGHTYELLOW_EX + Style.BRIGHT,
        "SUCCESS": Fore.LIGHTGREEN_EX + Style.BRIGHT,
        "OPTION": Fore.LIGHTCYAN_EX + Style.BRIGHT,
        "BORDER": Fore.GREEN + Style.BRIGHT
    },
    "matrix": {
        "TITLE": Fore.CYAN + Style.BRIGHT,
        "TEXT": Fore.LIGHTCYAN_EX + Style.BRIGHT,
        "WARNING": Fore.LIGHTYELLOW_EX + Style.BRIGHT,
        "SUCCESS": Fore.LIGHTGREEN_EX + Style.BRIGHT,
        "OPTION": Fore.LIGHTMAGENTA_EX + Style.BRIGHT,
        "BORDER": Fore.CYAN + Style.BRIGHT
    }
}

# Seleciona o tema atual
C = THEMES[THEME]
COR_TITULO = C["TITLE"]

# Textos traduzidos
TEXTS = {
    "pt": {
        "title": "WOLF TOOLS - KIT DE HACKING",
        "warning": "⚠ USE COM RESPONSABILIDADE!",
        "mainmenu": "MENU PRINCIPAL",
        "choice": "Escolha uma opção: ",
        "invalid": "Opção inválida!",
        "exit": "Saindo...",
        "install": "Instalando",
        "config": "CONFIGURAÇÕES",
        "return": "Retornar ao menu",
        "update": "Atualizando pacotes...",
        "installed": "já instalado. Atualizando...",
        "configuring": "Configurando",
        "success": "instalado com sucesso!",
        "osint": "Ferramentas de OSINT",
        "ddos": "Ferramentas de DDoS",
        "phishing": "Ferramentas de Phishing",
        "exploit": "Ferramentas de Exploração",
        "bruteforce": "Ferramentas de Brute Force",
        "media": "Mídias & Geradores",
        "language": "Idioma",
        "path": "Caminho de instalação",
        "current_lang": "Idioma atual: Português",
        "change_lang": "Selecione o idioma:\n1. Português\n2. English\n3. Español",
        "lang_set": "Idioma definido como Português",
        "current_path": "Diretório atual: ",
        "new_path": "Novo caminho (deixe em branco para cancelar): ",
        "path_changed": "Caminho alterado para: ",
        "operation_canceled": "Operação cancelada",
        "wifi": "Ferramentas WiFi",
        "exploit_framework": "Frameworks de Exploit",
        "seeker": "Localizador de IP/GPS",
        "ngrok": "Túnel reverso",
        "anonphisher": "Phishing Anônimo",
        "camphish": "Phishing de Câmera",
        "spcwa": "SPCWA Tool",
        "zphisher": "ZPhisher Tool",
        "mobile": "Ferramentas Mobile",
        "pentest": "Ferramentas de Pentest",
        "reverse": "Engenharia Reversa",
        "vpn": "VPN & Anonimato",
        "backup": "Backup & Restauração",
        "education": "Recursos Educacionais",
        "plugins": "Plugins Customizados",
        "root_warning": "⚠ Algumas ferramentas requerem root!",
        "continue_anyway": "Deseja continuar mesmo assim? (S/N): ",
        "checking_updates": "Verificando atualizações...",
        "update_available": "Atualização disponível!",
        "up_to_date": "Você está na versão mais recente",
        "backup_created": "Backup criado em: {}",
        "restore_complete": "Backup restaurado com sucesso!",
        "vpn_started": "VPN iniciada com configuração: {}",
        "tool_docs": "Documentação da ferramenta",
        "tutorials": "Tutoriais Recomendados",
        "dependencies": "Gerenciador de Dependências",
        "install_pkg": "Instalar Pacotes do Sistema",
        "install_pip": "Instalar Pacotes Python",
        "pkg_installed": "Pacotes do sistema instalados!",
        "pip_installed": "Pacotes Python instalados!",
        "installing": "Instalando {}...",
        "already_installed": "{} já está instalado",
        "install_all": "Instalar Todas as Dependências",
        "on": "ativado",
        "off": "desativado",
        "autoupdate": "Auto-atualização",
        "autoupdate_status": "Auto-atualização {}!",
        "theme": "Tema",
        "current_theme": "Tema atual: {}",
        "change_theme": "Selecione o tema:\n1. Dark (Vermelho/Preto)\n2. Hacker (Verde/Preto)\n3. Matrix (Ciano/Preto)",
        "theme_set": "Tema alterado para {}",
        "special_tools": "Ferramentas Especiais",
        "add_tool": "Adicionar Nova Ferramenta",
        "tool_name": "Nome da ferramenta: ",
        "repo_url": "URL do repositório: ",
        "install_cmd": "Comando de instalação (opcional): ",
        "category": "Categoria: ",
        "tool_added": "Ferramenta adicionada com sucesso!",
        "remove_tool": "Remover Ferramenta",
        "tool_removed": "Ferramenta removida com sucesso!",
        "sync_tools": "Sincronizar Ferramentas",
        "sync_complete": "Ferramentas sincronizadas com sucesso!",
        "update_tools": "Atualizar lista de ferramentas"
    },
    "en": {
        "title": "WOLF TOOLS - HACKING KIT",
        "warning": "⚠ USE RESPONSIBLY!",
        "mainmenu": "MAIN MENU",
        "choice": "Choose an option: ",
        "invalid": "Invalid option!",
        "exit": "Exiting...",
        "install": "Installing",
        "config": "SETTINGS",
        "return": "Return to menu",
        "update": "Updating packages...",
        "installed": "already installed. Updating...",
        "configuring": "Configuring",
        "success": "installed successfully!",
        "osint": "OSINT Tools",
        "ddos": "DDoS Tools",
        "phishing": "Phishing Tools",
        "exploit": "Exploit Tools",
        "bruteforce": "Brute Force Tools",
        "media": "Media & Generators",
        "language": "Language",
        "path": "Installation path",
        "current_lang": "Current language: English",
        "change_lang": "Select language:\n1. Portuguese\n2. English\n3. Spanish",
        "lang_set": "Language set to English",
        "current_path": "Current directory: ",
        "new_path": "New path (leave blank to cancel): ",
        "path_changed": "Path changed to: ",
        "operation_canceled": "Operation canceled",
        "wifi": "WiFi Tools",
        "exploit_framework": "Exploit Frameworks",
        "seeker": "IP/GPS Locator",
        "ngrok": "Reverse Tunnel",
        "anonphisher": "Anonymous Phishing",
        "camphish": "Camera Phishing",
        "spcwa": "SPCWA Tool",
        "zphisher": "ZPhisher Tool",
        "mobile": "Mobile Tools",
        "pentest": "Pentesting Tools",
        "reverse": "Reverse Engineering",
        "vpn": "VPN & Anonymity",
        "backup": "Backup & Restore",
        "education": "Educational Resources",
        "plugins": "Custom Plugins",
        "root_warning": "⚠ Some tools require root!",
        "continue_anyway": "Continue anyway? (Y/N): ",
        "checking_updates": "Checking for updates...",
        "update_available": "Update available!",
        "up_to_date": "You are on the latest version",
        "backup_created": "Backup created at: {}",
        "restore_complete": "Backup restored successfully!",
        "vpn_started": "VPN started with config: {}",
        "tool_docs": "Tool documentation",
        "tutorials": "Recommended Tutorials",
        "dependencies": "Dependencies Manager",
        "install_pkg": "Install System Packages",
        "install_pip": "Install Python Packages",
        "pkg_installed": "System packages installed!",
        "pip_installed": "Python packages installed!",
        "installing": "Installing {}...",
        "already_installed": "{} is already installed",
        "install_all": "Install All Dependencies",
        "on": "on",
        "off": "off",
        "autoupdate": "Auto-update",
        "autoupdate_status": "Auto-update {}!",
        "theme": "Theme",
        "current_theme": "Current theme: {}",
        "change_theme": "Select theme:\n1. Dark (Red/Black)\n2. Hacker (Green/Black)\n3. Matrix (Cyan/Black)",
        "theme_set": "Theme changed to {}",
        "special_tools": "Special Tools",
        "add_tool": "Add New Tool",
        "tool_name": "Tool name: ",
        "repo_url": "Repository URL: ",
        "install_cmd": "Install command (optional): ",
        "category": "Category: ",
        "tool_added": "Tool added successfully!",
        "remove_tool": "Remove Tool",
        "tool_removed": "Tool removed successfully!",
        "sync_tools": "Sync Tools",
        "sync_complete": "Tools synced successfully!",
        "update_tools": "Update tools list"
    },
    "es": {
        "title": "WOLF TOOLS - KIT DE HACKING",
        "warning": "⚠ ¡USA CON RESPONSABILIDAD!",
        "mainmenu": "MENÚ PRINCIPAL",
        "choice": "Elige una opción: ",
        "invalid": "¡Opción inválida!",
        "exit": "Saliendo...",
        "install": "Instalando",
        "config": "CONFIGURACIÓN",
        "return": "Volver al menú",
        "update": "Actualizando paquetes...",
        "installed": "ya instalado. Actualizando...",
        "configuring": "Configurando",
        "success": "¡instalado correctamente!",
        "osint": "Herramientas de OSINT",
        "ddos": "Herramientas de DDoS",
        "phishing": "Herramientas de Phishing",
        "exploit": "Herramientas de Explotación",
        "bruteforce": "Herramientas de Fuerza Bruta",
        "media": "Medios & Generadores",
        "language": "Idioma",
        "path": "Ruta de instalación",
        "current_lang": "Idioma actual: Español",
        "change_lang": "Selecciona el idioma:\n1. Portugués\n2. Inglés\n3. Español",
        "lang_set": "Idioma establecido en Español",
        "current_path": "Directorio actual: ",
        "new_path": "Nueva ruta (deja en blanco para cancelar): ",
        "path_changed": "Ruta cambiada a: ",
        "operation_canceled": "Operación cancelada",
        "wifi": "Herramientas WiFi",
        "exploit_framework": "Frameworks de Exploit",
        "seeker": "Localizador IP/GPS",
        "ngrok": "Túnel inverso",
        "anonphisher": "Phishing Anónimo",
        "camphish": "Phishing de Cámara",
        "spcwa": "Herramienta SPCWA",
        "zphisher": "Herramienta ZPhisher",
        "mobile": "Herramientas Mobile",
        "pentest": "Herramientas de Pentesting",
        "reverse": "Ingeniería Inversa",
        "vpn": "VPN & Anonimato",
        "backup": "Backup & Restauración",
        "education": "Recursos Educativos",
        "plugins": "Plugins Personalizados",
        "root_warning": "⚠ ¡Algunas herramientas requieren root!",
        "continue_anyway": "¿Continuar de todos modos? (S/N): ",
        "checking_updates": "Buscando actualizaciones...",
        "update_available": "¡Actualización disponible!",
        "up_to_date": "Estás en la versión más reciente",
        "backup_created": "Backup creado en: {}",
        "restore_complete": "¡Backup restaurado con éxito!",
        "vpn_started": "VPN iniciada con configuración: {}",
        "tool_docs": "Documentación de la herramienta",
        "tutorials": "Tutoriales Recomendados",
        "dependencies": "Gestor de Dependencias",
        "install_pkg": "Instalar Paquetes del Sistema",
        "install_pip": "Instalar Paquetes Python",
        "pkg_installed": "¡Paquetes del sistema instalados!",
        "pip_installed": "¡Paquetes Python instalados!",
        "installing": "Instalando {}...",
        "already_installed": "{} ya está instalado",
        "install_all": "Instalar Todas las Dependencias",
        "on": "activado",
        "off": "desactivado",
        "autoupdate": "Auto-actualización",
        "autoupdate_status": "¡Auto-actualización {}!",
        "theme": "Tema",
        "current_theme": "Tema actual: {}",
        "change_theme": "Selecciona el tema:\n1. Dark (Rojo/Negro)\n2. Hacker (Verde/Negro)\n3. Matrix (Cian/Negro)",
        "theme_set": "Tema cambiado a {}",
        "special_tools": "Herramientas Especiales",
        "add_tool": "Agregar Nueva Herramienta",
        "tool_name": "Nombre de la herramienta: ",
        "repo_url": "URL del repositorio: ",
        "install_cmd": "Comando de instalación (opcional): ",
        "category": "Categoría: ",
        "tool_added": "¡Herramienta agregada con éxito!",
        "remove_tool": "Eliminar Herramienta",
        "tool_removed": "¡Herramienta eliminada con éxito!",
        "sync_tools": "Sincronizar Herramientas",
        "sync_complete": "¡Herramientas sincronizadas con éxito!",
        "update_tools": "Actualizar lista de herramientas"
    }
}

def t(key):
    """Retorna o texto traduzido de acordo com o idioma atual"""
    return TEXTS[LANGUAGE][key]

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def linha_horizontal(esq='╔', dir='╗', preenchimento='═'):
    """Retorna uma linha horizontal formatada com bordas grossas"""
    return f"{C['BORDER']}{esq}{preenchimento * (LARGURA_MAXIMA - 2)}{dir}{Style.RESET_ALL}"

def linha_texto(texto, alinhamento='left'):
    """Retorna uma linha de texto formatada com bordas grossas"""
    texto_sem_cores = re.sub(r'\x1b\[[0-9;]*m', '', texto)
    espaço = LARGURA_MAXIMA - 2 - len(texto_sem_cores)

    if espaço < 0:
        texto = texto[:LARGURA_MAXIMA - 5] + '...'
        espaço = 0

    if alinhamento == 'center':
        left_space = espaço // 2
        right_space = espaço - left_space
        return f"{C['BORDER']}║{Style.RESET_ALL}{' ' * left_space}{C['TEXT']}{texto}{Style.RESET_ALL}{' ' * right_space}{C['BORDER']}║{Style.RESET_ALL}"
    else:
        return f"{C['BORDER']}║{Style.RESET_ALL} {C['TEXT']}{texto}{Style.RESET_ALL}{' ' * (espaço-1)}{C['BORDER']}║{Style.RESET_ALL}"

def run_command(cmd):
    """Executa um comando no terminal e retorna True se for bem-sucedido"""
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{C['WARNING']}Erro ao executar comando: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{C['WARNING']}Erro inesperado: {e}{Style.RESET_ALL}")
        return False

def download_with_progress(url, filename):
    """Baixa um arquivo com barra de progresso"""
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(filename, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                bar.update(len(data))
        return True
    except Exception as e:
        print(f"{C['WARNING']}Erro ao baixar arquivo: {e}{Style.RESET_ALL}")
        return False

def check_root():
    """Verifica se o usuário tem privilégios root"""
    if os.geteuid() != 0:
        print(f"\n{C['WARNING']}[!] {t('root_warning')}{Style.RESET_ALL}")
        choice = input(f"{C['TEXT']}{t('continue_anyway')}{Style.RESET_ALL}").lower()
        if choice not in ['s', 'y', 'sim', 'yes']:
            sys.exit(1)

def show_banner():
    """Exibe o banner completo do Wolf Tools com formatação perfeita"""
    clear_screen()

    # Configuração de cores dinâmicas (cores mais fortes)
    T = C['TITLE'] + Style.BRIGHT    # Cor do título (brilhante)
    TX = C['TEXT'] + Style.BRIGHT    # Cor do texto (brilhante)
    W = C['WARNING'] + Style.BRIGHT  # Cor de aviso (brilhante)
    R = Style.RESET_ALL

    # Arte ASCII completa do Lobo com cores fortes
    wolf_ascii = [
        f"{T}",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⣀⣴⡯⠖⣓⣶⣶⡶⠶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⢀⣴⣯⡾⣻⠽⡾⠽⠛⠚⠷⠯⠥⠤⠤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣢⣾⢿⣶⠿⣻⠿⠿⢋⣁⣠⠤⣶⢶⡆⠀⣀⣀⣀⣀⣀⣐⡻⢷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⠟⠛⠉⠪⠟⣩⠖⠋⢀⡴⢚⣭⠾⠟⠋⡹⣾⠀⠀⢀⣠⠤⠤⠬⠉⠛⠿⣷⡽⢷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⣿⢝⣯⠆⣩⠖⢀⣤⢞⣁⣄⣴⣫⡴⠛⠁⠀⡀⣼⠀⣿⢠⡴⠚⠋⠉⠭⠿⣷⣦⡤⢬⣝⣲⣌⡙⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣷⣿⣿⣾⣿⣷⣿⣿⣿⣿⠋⠀⢀⢀⣶⣷⣿⠀⣿⠀⠀⠀⠀⠀⠀⠐⠚⠻⣿⣶⣮⣛⢯⡙⠂⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣸⣿⠋⠀⡆⣾⣾⣿⣿⠿⢂⣿⣄⠀⠀⠀⠀⠀⠀⠐⠢⢤⣉⢳⣍⠲⣮⣳⣄⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠿⣷⡀⢸⣿⣿⣿⠙⠏⠁⣸⣿⣿⣭⣉⡁⠀⠀⠀⠀⠀⠀⠘⣿⣿⡷⣌⣿⡟⢿⣦⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⡿⡏⢡⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡹⣷⣼⣿⡟⠋⠀⠀⣴⣿⣿⣦⣍⣙⣓⡦⠄⠀⠈⠙⠲⢦⣻⣿⡅⠘⣾⣿⡄⠹⡳⡄⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⢹⠀⠀⠞⢭⣻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⠳⢼⣧⣄⣠⣾⣿⣿⣿⡻⢿⣭⡉⠁⠀⠀⠀⠀⠀⠀⠙⢿⢻⡄⠈⢻⣿⠀⠉⠹⡆⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣻⡇⡆⠀⢀⣶⣾⣳⠏⠉⢹⡿⣿⣿⣟⡿⠿⢿⣿⣿⣿⣧⠘⠒⠮⣿⣿⣿⣿⣿⣿⣿⣦⡬⠉⠀⠀⠀⢦⠀⠰⡀⠀⠈⠃⠓⠀⠈⣿⡀⠀⠀⢹⡀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⣾⡧⣔⠾⡏⠙⠁⠀⣠⣿⢀⡎⠉⠈⠻⠭⠤⠤⣌⡻⣿⡿⡀⠈⠙⠻⠿⠿⣯⣅⠉⠉⣝⠛⢦⡘⣶⡀⠀⢣⠀⠙⢦⡀⠘⢇⣆⠀⣿⡇⠀⠀⠀⡇",
        "⠀⠀⠀⠀⠀⣀⡠⠶⠿⠟⣃⣀⡀⠀⠀⠈⢓⣶⣾⣟⡡⠞⠀⠀⠀⠠⠴⠶⠿⠷⢿⡼⣿⣗⠀⠀⠀⠀⠀⠀⠈⠛⢆⠈⢧⡀⠁⠘⣿⡄⢢⠇⠀⠈⢧⠀⠸⣼⡄⣿⠇⠀⠀⢧⢸",
        "⠀⣠⠴⠾⣿⡛⠛⠛⠁⠀⠀⠀⠙⠲⠈⠉⠀⠀⠀⠀⠤⠤⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠘⢿⠷⣄⠘⣷⣄⡀⡄⠀⢀⡀⠀⢳⡄⠀⠀⠳⠀⡏⠀⠀⠸⡄⠀⢿⣧⣿⠀⠀⠀⡀⣼",
        "⣾⣿⢶⣦⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣀⣤⣶⣶⣒⠢⢤⠀⠀⠈⠁⠉⠛⠿⣎⡛⢦⣀⠈⣿⣴⣾⣿⡞⡄⠀⠀⢹⡀⠀⠀⣿⠀⣾⣿⠇⠀⠀⠀⡇⢸",
        "⠘⣿⣿⡾⡇⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡐⠲⢦⣦⢤⣤⣤⡶⠛⠉⠉⠀⠀⠀⠀⢀⣠⣤⣀⣤⠴⠂⠀⠀⠁⠀⢹⣧⣿⡿⢸⠇⢻⣿⣆⠀⠀⢷⣀⠀⣿⣷⠟⠉⠀⠀⠀⢸⡇⡄",
        "⠀⠈⠳⢭⡗⠒⣛⣻⣽⠿⢿⣯⣷⣾⣿⣿⣿⣶⣬⡉⣉⠈⠑⠒⠉⠙⠻⠯⠉⣩⡟⢁⣾⠏⠀⣾⣷⣤⣄⣀⡀⢨⡿⣿⡇⣸⠀⠘⡿⢹⣆⠀⣸⣿⣷⡿⠁⠀⡀⠀⢸⡀⣾⣧⠀",
        "⠀⠀⠀⠀⠈⠻⠿⣿⢿⡷⣌⣣⡉⠛⢿⣿⣿⣿⣿⣿⣧⡓⢄⠀⠀⠀⠀⠀⢰⡿⠷⣟⠿⠋⠀⢹⣿⡇⠀⠁⠙⣾⢧⠙⠙⠁⠀⠐⠁⠘⠹⣄⣿⠃⠹⣿⡀⠀⡇⠀⡿⣇⡿⢹⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠈⠓⠻⠊⠙⠃⠀⠀⠹⣿⣿⡿⡏⠀⣿⣌⠳⡄⠀⢀⡴⠋⠈⠉⠉⡙⠲⣤⢸⡟⣿⠀⠀⠠⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠿⠃⠀⠀⠈⠃⣸⡇⣼⠇⣿⡇⢸⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡄⢳⣿⣿⣿⡆⢳⠀⡎⠀⠀⠀⠀⢀⣉⠳⣬⣿⠇⠃⠀⠀⢠⠆⢰⢊⡇⠀⠀⠀⠀⠀⠀⢲⠀⢰⡆⠀⠀⣽⣿⡟⠀⢸⡇⡞⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢸⡇⠈⣿⢟⣼⣇⡏⠀⠀⠔⣺⡭⠽⣿⡛⠛⠿⡏⠀⣆⠀⠀⣼⠀⣼⣼⣷⡆⠀⠀⣶⡆⢠⡿⣠⣿⡇⠀⢰⣿⠏⣴⢂⠋⡼⠃⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡆⢻⢿⡁⣼⢣⣿⡿⠀⢀⢀⡴⠋⠀⠀⠀⠀⠙⣶⣦⡅⠀⣿⡄⢠⣿⣾⢿⠿⣿⡇⠀⠘⣾⣇⣼⣷⠟⡼⠀⣰⡿⠋⢠⠏⢦⣾⠃⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡟⢾⢄⣹⣧⡿⡽⠁⠀⣿⠋⠀⠀⠀⠀⠀⠀⠟⠉⣧⡾⡽⣠⣿⢛⠇⠏⠰⣻⠃⣼⣽⣿⡿⡿⠁⣴⣡⡾⠋⠀⢠⣞⣴⡿⠁⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣼⣿⣿⡟⠁⣠⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⠋⠰⠟⣻⣿⢋⠀⠀⣴⣷⣾⠟⡿⠋⠀⣥⠾⠛⡋⠀⠀⢠⣾⣿⠟⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⠽⠒⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⢁⡌⠀⢰⣿⠟⠁⠀⠀⠀⠀⡀⠀⣰⠃⠀⣴⡿⣿⠏⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠋⢀⣴⠏⠀⠀⢸⡋⠀⡀⠀⣀⠖⠋⣠⣾⢃⣠⡾⠟⢡⠇⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠎⣀⣴⡿⠃⠀⠀⠀⠀⢁⡾⠁⢈⣁⣴⣾⣿⣿⠟⠉⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣾⣿⡿⠁⠀⢀⣀⣤⣼⢟⣡⣶⠿⠟⠋⣰⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣟⣿⣿⣃⣴⣶⣿⠿⣿⣿⡿⠋⠀⠀⠀⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣾⣿⣿⣿⠛⠉⠀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⠟⠁⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⠀by:jottap_62⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        f"{R}"
    ]

    # Exibe a arte ASCII do lobo
    for line in wolf_ascii:
        print(line)

    # Logo WOLF TOOLS centralizado
    print(f"\n{T}")
    print(" ██╗    ██╗ ██████╗ ██╗     ███████╗ ")
    print(" ██║    ██║██╔═══██╗██║     ██╔════╝ ")
    print(" ██║ █╗ ██║██║   ██║██║     █████╗   ")
    print(" ██║███╗██║██║   ██║██║     ██╔══╝   ")
    print(" ╚███╔███╔╝╚██████╔╝███████╗██║      ")
    print("  ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝      ")
    print("                                      ")
    print(" ████████╗ ██████╗ ██╗     ██╗     ███████╗ ")
    print(" ╚══██╔══╝██╔═══██╗██║     ██║     ██╔════╝ ")
    print("    ██║   ██║   ██║██║     ██║     ███████╗ ")
    print("    ██║   ██║   ██║██║     ██║     ╚════██║ ")
    print("    ██║   ╚██████╔╝███████╗███████╗███████║ ")
    print("    ╚═╝    ╚═════╝ ╚══════╝╚══════╝╚══════╝ ")
    print(f"{R}")

    # Painel de informações
    print(linha_horizontal())
    print(linha_texto(f" {T}WOLF TOOLS - KIT DE PENTEST PROFISSIONAL{R}", 'center'))
    print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
    print(linha_texto(f"{W}⚠ {TX}Use apenas para testes legais! {W}⚠{R}"))
    print(linha_horizontal(esq='╠', dir='╣', preenchimento='─'))
    print(linha_texto(f"{T}► Versão: 4.0{R}"))
    print(linha_texto(f"{T}► Idioma: {LANGUAGE.upper()}{R}"))
    print(linha_texto(f"{T}► Data: {time.strftime('%d/%m/%Y %H:%M:%S')}{R}"))
    print(linha_texto(f"{T}► Path: {INSTALL_PATH[:25]}...{R}"))
    print(linha_texto(f"{T}► Tema: {THEME.capitalize()}{R}"))
    print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

def self_update():
    """Atualiza o Wolf Tools automaticamente"""
    print(f"\n{C['WARNING']}[*] {t('checking_updates')}{Style.RESET_ALL}")
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if run_command("git pull"):
            print(f"{C['SUCCESS']}[✔] {t('update_available')}{Style.RESET_ALL}")
        else:
            print(f"{C['TEXT']}[i] {t('up_to_date')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{C['WARNING']}Erro ao atualizar: {e}{Style.RESET_ALL}")

    time.sleep(SLEEP_TIME)

def backup_tools():
    """Cria backup das ferramentas instaladas"""
    backup_file = f"wolf_backup_{time.strftime('%Y%m%d')}.tar.gz"
    if run_command(f"tar -czf {backup_file} {INSTALL_PATH}"):
        print(f"{C['SUCCESS']}[✔] {t('backup_created').format(backup_file)}{Style.RESET_ALL}")
    else:
        print(f"{C['WARNING']}[!] Falha ao criar backup{Style.RESET_ALL}")
    time.sleep(SLEEP_TIME)

def install_pip_packages():
    """Instala todos os pacotes Python necessários"""
    packages = ["colorama", "tqdm", "requests", "PyGithub", "python-dotenv"]
    print(f"\n{C['WARNING']}[*] {t('install_pip')}{Style.RESET_ALL}")

    for pkg in packages:
        print(f"{C['TEXT']}[+] {t('installing').format(pkg)}{Style.RESET_ALL}")
        if run_command(f"pip install {pkg}"):
            print(f"{C['SUCCESS']}[✔] {pkg} {t('success')}{Style.RESET_ALL}")
        else:
            print(f"{C['WARNING']}[!] Falha ao instalar {pkg}{Style.RESET_ALL}")

    print(f"{C['SUCCESS']}[✔] {t('pip_installed')}{Style.RESET_ALL}")
    time.sleep(SLEEP_TIME)

def install_system_packages():
    """Menu para instalar pacotes do sistema"""
    while True:
        clear_screen()
        print(linha_horizontal())
        print(linha_texto(" " + t('install_pkg'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto("1. Instalar Pacotes Básicos"))
        print(linha_texto("2. Instalar Pacotes de Rede"))
        print(linha_texto("3. Instalar Pacotes de Desenvolvimento"))
        print(linha_texto("4. Instalar Todos os Pacotes"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            packages = "git python python2 python3 wget curl"
        elif choice == "2":
            packages = "nmap hydra tcpdump openssh"
        elif choice == "3":
            packages = "clang make ruby perl php"
        elif choice == "4":
            packages = "git python python2 python3 wget curl nmap hydra tcpdump openssh clang make ruby perl php"
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)
            continue

        print(f"\n{C['WARNING']}[*] Instalando pacotes...{Style.RESET_ALL}")
        if run_command(f"pkg install -y {packages}"):
            print(f"{C['SUCCESS']}[✔] {t('pkg_installed')}{Style.RESET_ALL}")
        else:
            print(f"{C['WARNING']}[!] Falha ao instalar pacotes{Style.RESET_ALL}")

        time.sleep(SLEEP_TIME)

def dependencies_menu():
    """Menu de gerenciamento de dependências"""
    while True:
        clear_screen()
        print(linha_horizontal())
        print(linha_texto(" " + t('dependencies'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto(f"1. {t('install_pkg')}"))
        print(linha_texto(f"2. {t('install_pip')}"))
        print(linha_texto(f"3. {t('install_all')}"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            install_system_packages()
        elif choice == "2":
            install_pip_packages()
        elif choice == "3":
            install_system_packages()
            install_pip_packages()
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

def install_tool(tool_name, repo_url, install_cmd, category):
    """Instala uma ferramenta específica"""
    print(f"\n{C['OPTION']}[+] {t('install')} {tool_name}...{Style.RESET_ALL}")

    category_dir = os.path.join(INSTALL_PATH, category)
    tool_dir = os.path.join(category_dir, tool_name)

    try:
        os.makedirs(category_dir, exist_ok=True)

        if os.path.exists(tool_dir):
            print(f"{C['WARNING']}[!] {tool_name} {t('installed')}{Style.RESET_ALL}")
            os.chdir(tool_dir)
            run_command("git pull")
            return

        clone_cmd = f"git clone {repo_url} {tool_dir}"
        if not run_command(clone_cmd):
            print(f"{C['WARNING']}[!] Falha ao clonar repositório{Style.RESET_ALL}")
            return

        os.chdir(tool_dir)

        if install_cmd:
            print(f"{C['WARNING']}[*] {t('configuring')} {tool_name}...{Style.RESET_ALL}")
            run_command(install_cmd)

        print(f"{C['SUCCESS']}[✔] {tool_name} {t('success')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{C['WARNING']}Erro na instalação: {e}{Style.RESET_ALL}")

    time.sleep(SLEEP_TIME)

def get_current_tools():
    """Obtém as ferramentas atuais do repositório GitHub"""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents(JSON_FILE)
        return json.loads(contents.decoded_content.decode())
    except Exception as e:
        print(f"{C['WARNING']}Erro ao buscar ferramentas: {e}{Style.RESET_ALL}")
        return None

def update_github_tools(new_data):
    """Atualiza as ferramentas no repositório GitHub"""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents(JSON_FILE)
        repo.update_file(contents.path, "Update tools", json.dumps(new_data, indent=4), contents.sha)
        return True
    except Exception as e:
        print(f"{C['WARNING']}Erro ao atualizar ferramentas: {e}{Style.RESET_ALL}")
        return False

def sync_with_github():
    """Sincroniza as ferramentas com o repositório GitHub"""
    try:
        response = requests.get(REMOTE_JSON_URL)
        if response.status_code == 200:
            remote_tools = response.json()
            for category in remote_tools.get("tools", {}):
                TOOLS[category] = OrderedDict(
                    (tool["name"], (tool["repo"], tool["install_cmd"]))
                    for tool in remote_tools["tools"][category]
                )
            print(f"{C['SUCCESS']}[✔] {t('sync_complete')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{C['WARNING']}Erro na sincronização: {e}{Style.RESET_ALL}")

def check_for_updates():
    """Verifica atualizações no repositório de ferramentas"""
    print(f"\n{C['WARNING']}[*] Verificando atualizações...{Style.RESET_ALL}")
    try:
        # Atualiza o repositório local primeiro
        os.system("git -C " + INSTALL_PATH + " pull")

        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents(JSON_FILE)
        remote_tools = json.loads(contents.decoded_content.decode())

        # Atualiza a lista local de ferramentas
        for category in remote_tools.get("tools", {}):
            if category not in TOOLS:
                TOOLS[category] = OrderedDict()

            for tool in remote_tools["tools"][category]:
                TOOLS[category][tool["name"]] = (tool["repo"], tool.get("install_cmd", ""))

        print(f"{C['SUCCESS']}[✔] Ferramentas atualizadas com sucesso!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{C['WARNING']}[!] Falha ao verificar atualizações: {e}{Style.RESET_ALL}")
        return False

def add_new_tool():
    """Adiciona uma nova ferramenta ao sistema"""
    print(f"\n{C['WARNING']}[*] {t('add_tool')}{Style.RESET_ALL}")

    tool_name = input(t('tool_name'))
    repo_url = input(t('repo_url'))
    install_cmd = input(t('install_cmd'))

    print("\nCategorias disponíveis:")
    for i, category in enumerate(TOOLS.keys(), 1):
        print(f"{i}. {category}")

    category_choice = input("\n" + t('category'))
    try:
        category_index = int(category_choice) - 1
        if 0 <= category_index < len(TOOLS):
            category = list(TOOLS.keys())[category_index]
            TOOLS[category][tool_name] = (repo_url, install_cmd)

            # Atualiza o GitHub
            tools_data = {"tools": {}}
            for cat, tools in TOOLS.items():
                tools_data["tools"][cat] = [
                    {"name": name, "repo": repo, "install_cmd": cmd}
                    for name, (repo, cmd) in tools.items()
                ]

            if update_github_tools(tools_data):
                print(f"{C['SUCCESS']}[✔] {t('tool_added')}{Style.RESET_ALL}")
            else:
                print(f"{C['WARNING']}[!] Ferramenta adicionada localmente mas falha ao atualizar GitHub{Style.RESET_ALL}")
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
    except ValueError:
        print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")

    time.sleep(SLEEP_TIME)

def remove_tool():
    """Remove uma ferramenta do sistema"""
    print(f"\n{C['WARNING']}[*] {t('remove_tool')}{Style.RESET_ALL}")

    print("\nCategorias disponíveis:")
    for i, category in enumerate(TOOLS.keys(), 1):
        print(f"{i}. {category}")

    category_choice = input("\nSelecione a categoria: ")
    try:
        category_index = int(category_choice) - 1
        if 0 <= category_index < len(TOOLS):
            category = list(TOOLS.keys())[category_index]

            print(f"\nFerramentas em {category}:")
            for i, tool in enumerate(TOOLS[category].keys(), 1):
                print(f"{i}. {tool}")

            tool_choice = input("\nSelecione a ferramenta para remover: ")
            try:
                tool_index = int(tool_choice) - 1
                if 0 <= tool_index < len(TOOLS[category]):
                    tool_name = list(TOOLS[category].keys())[tool_index]
                    del TOOLS[category][tool_name]

                    # Atualiza o GitHub
                    tools_data = {"tools": {}}
                    for cat, tools in TOOLS.items():
                        tools_data["tools"][cat] = [
                            {"name": name, "repo": repo, "install_cmd": cmd}
                            for name, (repo, cmd) in tools.items()
                        ]

                    if update_github_tools(tools_data):
                        print(f"{C['SUCCESS']}[✔] {t('tool_removed')}{Style.RESET_ALL}")
                    else:
                        print(f"{C['WARNING']}[!] Ferramenta removida localmente mas falha ao atualizar GitHub{Style.RESET_ALL}")
                else:
                    print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            except ValueError:
                print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
    except ValueError:
        print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
    time.sleep(SLEEP_TIME)

def category_menu(category_name):
    """Menu genérico para categorias de ferramentas"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + category_name, 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))

        tools = TOOLS.get(category_name, OrderedDict())
        for i, tool in enumerate(tools.keys(), 1):
            print(linha_texto(f"{i}. 🛠️ {tool}"))

        print(linha_texto(f"X. ↩️ {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice.lower() == "x":
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(tools):
                tool_name = list(tools.keys())[index]
                repo_url, install_cmd = tools[tool_name]
                install_tool(tool_name, repo_url, install_cmd, category_name)
            else:
                print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
        except ValueError:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")

        time.sleep(SLEEP_TIME)

def osint_menu():
    category_menu("OSINT")

def ddos_menu():
    category_menu("DDoS")

def phishing_menu():
    category_menu("Phishing")

def exploit_menu():
    category_menu("Exploit")

def bruteforce_menu():
    category_menu("BruteForce")

def wifi_menu():
    category_menu("WiFi")

def exploit_framework_menu():
    category_menu("ExploitFramework")

def mobile_menu():
    category_menu("Mobile")

def pentest_menu():
    category_menu("Pentest")

def reverse_menu():
    category_menu("Reverse")

def special_tools_menu():
    """Menu de ferramentas especiais"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + t('special_tools'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto(f"1. {t('seeker')}"))
        print(linha_texto(f"2. {t('ngrok')}"))
        print(linha_texto(f"3. {t('anonphisher')}"))
        print(linha_texto(f"4. {t('zphisher')}"))
        print(linha_texto(f"5. {t('spcwa')}"))
        print(linha_texto(f"6. {t('camphish')}"))
        print(linha_texto(f"7. {t('add_tool')}"))
        print(linha_texto(f"8. {t('remove_tool')}"))
        print(linha_texto(f"9. {t('sync_tools')}"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            install_tool("seeker", "https://github.com/thewhiteh4t/seeker.git",
                        "pip3 install -r requirements.txt", "SpecialTools")
        elif choice == "2":
            install_tool("ngrok", "https://github.com/inconshreveable/ngrok.git",
                        "make release-client", "SpecialTools")
        elif choice == "3":
            install_tool("anonphisher", "https://github.com/Anonymous-Phunter/AnonPhisher.git",
                        "", "SpecialTools")
        elif choice == "4":
            install_tool("zphisher", "https://github.com/htr-tech/zphisher.git",
                        "", "SpecialTools")
        elif choice == "5":
            install_tool("spcwa", "https://github.com/MatrixTM/SPCWA.git",
                        "", "SpecialTools")
        elif choice == "6":
            install_tool("CamPhish", "https://github.com/techchipnet/CamPhish.git",
                        "bash camphish.sh", "SpecialTools")
        elif choice == "7":
            add_new_tool()
        elif choice == "8":
            remove_tool()
        elif choice == "9":
            sync_with_github()
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

def media_menu():
    """Menu para baixar mídias e geradores"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + t('media'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto("1. Baixar Mídia (Wolf-v8)"))
        print(linha_texto("2. Baixar Gerador (Wolf-v8)"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            install_tool("Wolf-Media", "https://github.com/jottap-termux/Wolf-v8", "", "Media")
        elif choice == "2":
            install_tool("Wolf-Generator", "https://github.com/jottap-termux/Wolf-v8", "", "Generator")
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

def vpn_menu():
    """Menu para VPN e ferramentas de anonimato"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + t('vpn'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto("1. Instalar OpenVPN"))
        print(linha_texto("2. Iniciar VPN (config.ovpn)"))
        print(linha_texto("3. Tor Network"))
        print(linha_texto("4. Proxychains"))
        print(linha_texto("5. Anonsurf"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            run_command("pkg install openvpn -y")
            print(f"{C['SUCCESS']}[✔] OpenVPN instalado!{Style.RESET_ALL}")
        elif choice == "2":
            config = input("Caminho para o arquivo .ovpn: ")
            run_command(f"openvpn {config}")
            print(f"{C['SUCCESS']}{t('vpn_started').format(config)}{Style.RESET_ALL}")
        elif choice == "3":
            run_command("pkg install tor -y && tor")
            print(f"{C['SUCCESS']}[✔] Tor iniciado!{Style.RESET_ALL}")
        elif choice == "4":
            run_command("pkg install proxychains-ng -y")
            print(f"{C['SUCCESS']}[✔] Proxychains instalado!{Style.RESET_ALL}")
        elif choice == "5":
            install_tool("Anonsurf", "https://github.com/Und3rf10w/kali-anonsurf.git",
                        "./installer.sh", "VPN")
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

def education_menu():
    """Menu com recursos educacionais"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + t('education'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto(f"1. {t('tool_docs')}"))
        print(linha_texto(f"2. {t('tutorials')}"))
        print(linha_texto("3. Livros de Hacking (PDF)"))
        print(linha_texto("4. Cursos Gratuitos"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            print(f"\n{C['TEXT']}Documentação das ferramentas:{Style.RESET_ALL}")
            print("- Metasploit: https://docs.rapid7.com/metasploit/")
            print("- Nmap: https://nmap.org/book/")
            print("- Wireshark: https://www.wireshark.org/docs/")
            print("- Burp Suite: https://portswigger.net/burp/documentation")
            input("\nPressione Enter para continuar...")
        elif choice == "2":
            print(f"\n{C['TEXT']}Tutoriais recomendados:{Style.RESET_ALL}")
            print("- Cybrary: https://www.cybrary.it/")
            print("- Hack The Box: https://www.hackthebox.com/")
            print("- TryHackMe: https://tryhackme.com/")
            print("- OverTheWire: https://overthewire.org/wargames/")
            input("\nPressione Enter para continuar...")
        elif choice == "3":
            print(f"\n{C['TEXT']}Livros recomendados:{Style.RESET_ALL}")
            print("- The Web Application Hacker's Handbook")
            print("- Hacking: The Art of Exploitation")
            print("- Penetration Testing: A Hands-On Introduction")
            print("- Black Hat Python")
            input("\nPressione Enter para continuar...")
        elif choice == "4":
            print(f"\n{C['TEXT']}Cursos gratuitos:{Style.RESET_ALL}")
            print("- Ethical Hacking from Scratch (Udemy)")
            print("- Penetration Testing and Ethical Hacking (Cybrary)")
            print("- Intro to Information Security (Georgia Tech)")
            input("\nPressione Enter para continuar...")
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

def change_language():
    """Altera o idioma da interface"""
    global LANGUAGE
    print(f"\n{C['WARNING']}{t('change_lang')}{Style.RESET_ALL}")
    choice = input("➤ ")

    if choice == "1":
        LANGUAGE = "pt"
        print(f"{C['SUCCESS']}{t('lang_set')}{Style.RESET_ALL}")
    elif choice == "2":
        LANGUAGE = "en"
        print(f"{C['SUCCESS']}Language set to English{Style.RESET_ALL}")
    elif choice == "3":
        LANGUAGE = "es"
        print(f"{C['SUCCESS']}Idioma establecido en Español{Style.RESET_ALL}")
    else:
        print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")

    time.sleep(SLEEP_TIME)

def change_theme():
    """Altera o tema de cores"""
    global THEME, C, COR_TITULO
    print(f"\n{C['WARNING']}{t('change_theme')}{Style.RESET_ALL}")
    choice = input("➤ ")

    if choice == "1":
        THEME = "dark"
    elif choice == "2":
        THEME = "hacker"
    elif choice == "3":
        THEME = "matrix"
    else:
        print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
        return

    C = THEMES[THEME]
    COR_TITULO = C["TITLE"]
    print(f"{C['SUCCESS']}{t('theme_set').format(THEME)}{Style.RESET_ALL}")
    time.sleep(SLEEP_TIME)

def change_path():
    """Altera o caminho de instalação"""
    global INSTALL_PATH
    print(f"\n{C['WARNING']}{t('current_path')}{INSTALL_PATH}{Style.RESET_ALL}")
    new_path = input(t('new_path')).strip()

    if new_path:
        INSTALL_PATH = os.path.expanduser(new_path)
        os.makedirs(INSTALL_PATH, exist_ok=True)
        print(f"{C['SUCCESS']}{t('path_changed')}{INSTALL_PATH}{Style.RESET_ALL}")
    else:
        print(f"{C['WARNING']}{t('operation_canceled')}{Style.RESET_ALL}")

    time.sleep(SLEEP_TIME)

def toggle_auto_update():
    """Ativa/desativa auto-atualização"""
    global AUTO_UPDATE
    AUTO_UPDATE = not AUTO_UPDATE
    status = t('on') if AUTO_UPDATE else t('off')
    print(f"\n{C['SUCCESS']}{t('autoupdate_status').format(status)}{Style.RESET_ALL}")
    time.sleep(SLEEP_TIME)

def config_menu():
    """Menu de configurações"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + t('config'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto(f"1. {t('language')}: {LANGUAGE}"))
        print(linha_texto(f"2. {t('path')}: {INSTALL_PATH}"))
        print(linha_texto(f"3. {t('autoupdate')}: {'ON' if AUTO_UPDATE else 'OFF'}"))
        print(linha_texto(f"4. {t('theme')}: {THEME}"))
        print(linha_texto(f"5. {t('backup')}"))
        print(linha_texto(f"6. {t('dependencies')}"))
        print(linha_texto(f"7. {t('sync_tools')}"))
        print(linha_texto(f"X. {t('return')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            change_language()
        elif choice == "2":
            change_path()
        elif choice == "3":
            toggle_auto_update()
        elif choice == "4":
            change_theme()
        elif choice == "5":
            backup_tools()
        elif choice == "6":
            dependencies_menu()
        elif choice == "7":
            sync_with_github()
        elif choice.lower() == "x":
            return
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

def main_menu():
    """Menu principal"""
    while True:
        show_banner()
        print(linha_horizontal())
        print(linha_texto(" " + t('mainmenu'), 'center'))
        print(linha_horizontal(esq='╠', dir='╣', preenchimento='═'))
        print(linha_texto(f"1.  {t('osint')}"))
        print(linha_texto(f"2.  {t('ddos')}"))
        print(linha_texto(f"3.  {t('phishing')}"))
        print(linha_texto(f"4.  {t('exploit')}"))
        print(linha_texto(f"5.  {t('bruteforce')}"))
        print(linha_texto(f"6.  {t('wifi')}"))
        print(linha_texto(f"7.  {t('exploit_framework')}"))
        print(linha_texto(f"8.  {t('mobile')}"))
        print(linha_texto(f"9.  {t('pentest')}"))
        print(linha_texto(f"10. {t('reverse')}"))
        print(linha_texto(f"11. {t('media')}"))
        print(linha_texto(f"12. {t('vpn')}"))
        print(linha_texto(f"13. {t('education')}"))
        print(linha_texto(f"14. {t('dependencies')}"))
        print(linha_texto(f"15. {t('config')}"))
        print(linha_texto(f"16. {t('special_tools')}"))
        print(linha_texto(f"17. {t('update_tools')}"))
        print(linha_texto(f"0.  {t('exit')}"))
        print(linha_horizontal(esq='╚', dir='╝', preenchimento='═'))

        choice = input(f"\n➤ {t('choice')} ")

        if choice == "1":
            osint_menu()
        elif choice == "2":
            ddos_menu()
        elif choice == "3":
            phishing_menu()
        elif choice == "4":
            exploit_menu()
        elif choice == "5":
            bruteforce_menu()
        elif choice == "6":
            wifi_menu()
        elif choice == "7":
            exploit_framework_menu()
        elif choice == "8":
            mobile_menu()
        elif choice == "9":
            pentest_menu()
        elif choice == "10":
            reverse_menu()
        elif choice == "11":
            media_menu()
        elif choice == "12":
            vpn_menu()
        elif choice == "13":
            education_menu()
        elif choice == "14":
            dependencies_menu()
        elif choice == "15":
            config_menu()
        elif choice == "16":
            special_tools_menu()
        elif choice == "17":
            check_for_updates()
            time.sleep(2)
        elif choice == "0":
            print(f"{C['WARNING']}{t('exit')}{Style.RESET_ALL}")
            sys.exit()
        else:
            print(f"{C['WARNING']}{t('invalid')}{Style.RESET_ALL}")
            time.sleep(SLEEP_TIME)

# Dicionário com todas as ferramentas
TOOLS = {
    "OSINT": OrderedDict([
        ("Th3inspector", ("https://github.com/Moham3dRiahi/Th3inspector.git", "./install.sh")),
        ("angryFuzzer", ("https://github.com/ihebski/angryFuzzer.git", "pip3 install -r requirements.txt")),
        ("PhoneInfoga", ("https://github.com/sundowndev/PhoneInfoga.git", "pip3 install -r requirements.txt")),
        ("FBI", ("https://github.com/xHak9x/fbi.git", "pip2 install -r requirements.txt")),
        ("Infoga", ("https://github.com/m4ll0k/Infoga.git", "python setup.py install")),
        ("InfoSploit", ("https://github.com/CybernetiX-S3C/InfoSploit.git", "pip3 install -r requirements.txt")),
        ("BillCipher", ("https://github.com/GitHackTools/BillCipher.git", "")),
        ("gasmask", ("https://github.com/twelvesec/gasmask.git", "")),
        ("OSIF", ("https://github.com/ciku370/OSIF.git", "pip2 install -r requirements.txt")),
        ("inmux", ("https://github.com/Amriez/inmux.git", "")),
        ("IP-Tracer", ("https://github.com/rajkumardusad/IP-Tracer.git", "")),
        ("RED_HAWK", ("https://github.com/Tuhinshubhra/RED_HAWK.git", "php install.php")),
        ("TMscanner", ("https://github.com/TechnicalMujeeb/TM-scanner.git", "pip2 install -r requirements.txt")),
        ("sqlmx_termux", ("https://github.com/AnonHackerr/sqlmx_termux.git", "")),
        ("reconspider", ("https://github.com/bhavsec/reconspider.git", "pip3 install -r requirements.txt")),
        ("ReconDog", ("https://github.com/UltimateHackers/ReconDog.git", "")),
        ("IPGeolocation", ("https://github.com/maldevel/IPGeolocation.git", "pip3 install -r requirements.txt")),
        ("Optiva-Framework", ("https://github.com/JavierOlmedo/Optiva-Framework.git", "")),
        ("wpscan", ("https://github.com/wpscanteam/wpscan.git", "bundle install && rake install")),
        ("theHarvester", ("https://github.com/laramies/theHarvester.git", "pip3 install -r requirements.txt")),
        ("KnockMail", ("https://github.com/4w4k3/KnockMail.git", "pip3 install -r requirements.txt")),
        ("SCANNER-INURLBR", ("https://github.com/googleinurl/SCANNER-INURLBR.git", "")),
        ("dmitry", ("https://github.com/jaygreig86/dmitry.git", "./configure && make")),
        ("ShodanHat", ("https://github.com/HatBashBR/ShodanHat.git", "")),
        ("Hatwitch", ("https://github.com/HatBashBR/Hatwitch.git", "")),
        ("URLextractor", ("https://github.com/eschultze/URLextractor.git", "")),
        ("webkiller", ("https://github.com/ultrasecurity/webkiller.git", "")),
        ("creepy", ("https://github.com/ilektrojohn/creepy.git", "")),
        ("seeker", ("https://github.com/thewhiteh4t/seeker.git", "pip3 install -r requirements.txt")),
        ("twifo-cli", ("https://github.com/1000i100/twifo-cli.git", "")),
        ("sherlock", ("https://github.com/sherlock-project/sherlock.git", "pip3 install -r requirements.txt")),
        ("osi.ig", ("https://github.com/th3unkn0n/osi.ig.git", "")),
        ("Arjun", ("https://github.com/s0md3v/Arjun.git", "")),
        ("CloudFail", ("https://github.com/m0rtem/CloudFail.git", "pip3 install -r requirements.txt")),
        ("dnstwist", ("https://github.com/elceef/dnstwist.git", "pip3 install -r requirements.txt")),
        ("holehe", ("https://github.com/megadose/holehe.git", "pip3 install .")),
        ("pwnedOrNot", ("https://github.com/thewhiteh4t/pwnedOrNot.git", "pip3 install -r requirements.txt")),
        ("ipdrone", ("https://github.com/noob-hackers/ipdrone.git", "")),
        ("007-TheBond", ("https://github.com/007revad/TheBond.git", "")),
        ("SpiderFoot", ("https://github.com/smicallef/spiderfoot.git", "pip3 install -r requirements.txt")),
        ("GHunt", ("https://github.com/mxrch/GHunt.git", "pip3 install -r requirements.txt")),
        ("Trape", ("https://github.com/jofpin/trape.git", "pip3 install -r requirements.txt"))
    ]),

    "DDoS": OrderedDict([
        ("Xerxes", ("https://github.com/zanyarjamal/xerxes.git", "clang xerxes.c -o xerxes")),
        ("slowloris.pl", ("https://github.com/llaera/slowloris.pl.git", "")),
        ("hammer", ("https://github.com/cyweb/hammer.git", "")),
        ("Hunner", ("https://github.com/b3-v3r/Hunner.git", "")),
        ("GoldenEye", ("https://github.com/jseidl/GoldenEye.git", "")),
        ("DDos-Attack", ("https://github.com/Ha3MrX/DDos-Attack.git", "")),
        ("Ddoser", ("https://github.com/kotleni/ddoser.git", "")),
        ("torshammer", ("https://github.com/dotfighter/torshammer.git", "")),
        ("LITEDDOS", ("https://github.com/4L13199/LITEDDOS.git", "")),
        ("hulk", ("https://github.com/grafov/hulk.git", "")),
        ("Memcrashed-DDoS-Exploit", ("https://github.com/649/Memcrashed-DDoS-Exploit.git", "")),
        ("Planetwork-DDOS", ("https://github.com/Hydra7/Planetwork-DDOS.git", "")),
        ("ping_of_death", ("https://github.com/Matrix07ksa/ping_of_death.git", "")),
        ("IcmpiFlood", ("https://github.com/Souhardya/IcmpiFlood.git", "")),
        ("exploit-blacknurse", ("https://github.com/jamesbarlow/exploit-blacknurse.git", "")),
        ("PyFlooder", ("https://github.com/NullArray/PyFlooder.git", "")),
        ("Saddam", ("https://github.com/OffensivePython/Saddam.git", "")),
        ("ntpdos", ("https://github.com/noptrix/ntpdos.git", "")),
        ("MHDDoS", ("https://github.com/MatrixTM/MHDDoS.git", "pip3 install -r requirements.txt")),
        ("Impulse", ("https://github.com/LimerBoy/Impulse.git", "pip3 install -r requirements.txt")),
        ("DDoS-Ripper", ("https://github.com/palahsu/DDoS-Ripper.git", ""))
    ]),

    "Phishing": OrderedDict([
        ("SocialFish", ("https://github.com/UndeadSec/SocialFish.git", "pip3 install -r requirements.txt")),
        ("SocialPhish", ("https://github.com/xHak9x/SocialPhish.git", "")),
        ("Phisher-man", ("https://github.com/An0nUD4Y/Phisher-man.git", "")),
        ("shellphish", ("https://github.com/thelinuxchoice/shellphish.git", "")),
        ("HiddenEye", ("https://github.com/DarkSecDevelopers/HiddenEye.git", "pip3 install -r requirements.txt")),
        ("gophish", ("https://github.com/gophish/gophish.git", "go build")),
        ("Turk-Sploit", ("https://github.com/Exploit-install/Turk-Sploit.git", "")),
        ("weeman", ("https://github.com/evait-security/weeman.git", "")),
        ("dnstwist", ("https://github.com/elceef/dnstwist.git", "pip3 install -r requirements.txt")),
        ("Phlexish", ("https://github.com/Phlexish/Phlexish.git", "")),
        ("zphisher", ("https://github.com/htr-tech/zphisher.git", "")),
        ("nexphisher", ("https://github.com/htr-tech/nexphisher.git", "")),
        ("grabcam", ("https://github.com/noob-hackers/grabcam.git", "")),
        ("saycheese", ("https://github.com/thelinuxchoice/saycheese.git", "")),
        ("seeu", ("https://github.com/trustedsec/seeu.git", "")),
        ("maskphish", ("https://github.com/jaykali/maskphish.git", ""))
    ]),

    "Exploit": OrderedDict([
        ("XAttacker", ("https://github.com/Moham3dRiahi/XAttacker.git", "perl XAttacker.pl")),
        ("routersploit", ("https://github.com/threat9/routersploit.git", "pip3 install -r requirements.txt")),
        ("SVScanner", ("https://github.com/radenvodka/SVScanner.git", "")),
        ("Revslider-Auto-Exploiter", ("https://github.com/V1n1v131r4/Revslider-Auto-Exploiter.git", "")),
        ("sqlmap", ("https://github.com/sqlmapproject/sqlmap.git", "")),
        ("exploitdb", ("https://github.com/offensive-security/exploitdb.git", "")),
        ("Pompem", ("https://github.com/rfunix/Pompem.git", "")),
        ("OWScan", ("https://github.com/Gameye98/OWScan.git", "")),
        ("sqlscan", ("https://github.com/Cvar1984/sqlscan.git", "")),
        ("D-TECT-1", ("https://github.com/shawarkhanethicalhacker/D-TECT-1.git", "")),
        ("Striker", ("https://github.com/s0md3v/Striker.git", "pip2 install -r requirements.txt")),
        ("SH33LL", ("https://github.com/LOoLzeC/SH33LL.git", "")),
        ("Xshell", ("https://github.com/Ubaii/Xshell.git", "")),
        ("sqlninja", ("https://github.com/xxgrunge/sqlninja.git", "")),
        ("DirAttack", ("https://github.com/Ranginang67/DirAttack.git", "")),
        ("DirKiller", ("https://github.com/Zian25/DirKiller.git", "")),
        ("NoSQLMap", ("https://github.com/codingo/NoSQLMap.git", "")),
        ("AdminHack", ("https://github.com/samhaxr/AdminHack.git", ""))
    ]),

    "BruteForce": OrderedDict([
        ("Facebook-BruteForce", ("https://github.com/IAmBlackHacker/Facebook-BruteForce.git", "")),
        ("Hydra", ("https://github.com/vanhauser-thc/thc-hydra.git", "./configure && make && make install")),
        ("facebook-cracker", ("https://github.com/Ha3MrX/facebook-cracker.git", "")),
        ("Instahack", ("https://github.com/avramit/Instahack.git", "")),
        ("crunch", ("https://github.com/crunchsec/crunch.git", "make && make install")),
        ("hashcat", ("https://github.com/hashcat/hashcat.git", "make && make install")),
        ("Black-Hydra", ("https://github.com/Gameye98/Black-Hydra.git", "")),
        ("Hash-Buster", ("https://github.com/s0md3v/Hash-Buster.git", "")),
        ("Facebom", ("https://github.com/Oseid/Facebom.git", "")),
        ("brutespray", ("https://github.com/x90skysn3k/brutespray.git", "pip3 install -r requirements.txt")),
        ("hyprPulse", ("https://github.com/Pure-L0G1C/hyprPulse.git", "")),
        ("lazybee", ("https://github.com/noob-hackers/lazybee.git", "")),
        ("Instabruteforce", ("https://github.com/Ha3MrX/Instabruteforce.git", "")),
        ("HackFacebokpass", ("https://github.com/JasonJerry/HackFacebokpass.git", "")),
        ("SocialBox-Termux", ("https://github.com/samsesh/SocialBox-Termux.git", "chmod +x install-sb.sh && ./install-sb.sh")),
        ("EMAGNET", ("https://github.com/wuseman/EMAGNET.git", "")),
        ("ighack", ("https://github.com/noob-hackers/ighack.git", ""))
    ]),

    "WiFi": OrderedDict([
        ("Wifite", ("https://github.com/derv82/wifite2.git", "python setup.py install")),
        ("Airgeddon", ("https://github.com/v1s1t0r1sh3r3/airgeddon.git", "")),
        ("Wifiphisher", ("https://github.com/wifiphisher/wifiphisher.git", "python setup.py install")),
        ("Pixiewps", ("https://github.com/wiire/pixiewps.git", "make && make install")),
        ("Reaver", ("https://github.com/t6x/reaver-wps-fork-t6x.git", "./configure && make && make install")),
        ("Bully", ("https://github.com/aanarchyy/bully.git", "make && make install")),
        ("Fern Wifi Cracker", ("https://github.com/savio-code/fern-wifi-cracker.git", "")),
        ("KickThemOut", ("https://github.com/k4m4/kickthemout.git", "pip3 install -r requirements.txt")),
        ("Zerowsh", ("https://github.com/Devil-Tigers/Zerowsh.git", "")),
        ("Wifi-Hacker", ("https://github.com/esc0rtd3w/wifi-hacker.git", "")),
        ("WifiBroot", ("https://github.com/hash3liZer/WiFiBroot.git", "pip3 install .")),
        ("Wifite2", ("https://github.com/derv82/wifite2.git", "python setup.py install")),
        ("Wifi-Pumpkin", ("https://github.com/P0cL4bs/WiFi-Pumpkin.git", "pip3 install -r requirements.txt")),
        ("fluxion", ("https://github.com/FluxionNetwork/fluxion.git", "")),
        ("Linset", ("https://github.com/vk496/linset.git", "")),
        ("WifiGod", ("https://github.com/zerohack-zz/WifiGod.git", ""))
    ]),

    "ExploitFramework": OrderedDict([
        ("Metasploit", ("https://github.com/rapid7/metasploit-framework.git", "bundle install")),
        ("BeEF", ("https://github.com/beefproject/beef.git", "./install")),
        ("AutoSploit", ("https://github.com/NullArray/AutoSploit.git", "pip2 install -r requirements.txt")),
        ("XSStrike", ("https://github.com/s0md3v/XSStrike.git", "pip3 install -r requirements.txt")),
        ("Commix", ("https://github.com/commixproject/commix.git", "")),
        ("ExploitPack", ("https://github.com/juansacco/exploitpack.git", "")),
        ("TheFatRat", ("https://github.com/Screetsec/TheFatRat.git", "./setup.sh")),
        ("WinSploit", ("https://github.com/SecWiki/windows-kernel-exploits.git", "")),
        ("Linux Exploit Suggester", ("https://github.com/mzet-/linux-exploit-suggester.git", "")),
        ("AutoRoot", ("https://github.com/nilotpalbiswas/Auto-Root-Exploit.git", "")),
        ("RouterSploit", ("https://github.com/threat9/routersploit.git", "pip3 install -r requirements.txt")),
        ("Exploit-DB", ("https://github.com/offensive-security/exploitdb.git", "")),
        ("ShellSploit", ("https://github.com/b3mb4m/shellsploit-framework.git", "python setup.py install")),
        ("XSploit", ("https://github.com/CoderPirata/XSploit.git", "")),
        ("SploitKit", ("https://github.com/merrychap/SploitKit.git", "")),
        ("Vulnx", ("https://github.com/anouarbensaad/vulnx.git", "pip3 install -r requirements.txt")),
        ("Striker", ("https://github.com/s0md3v/Striker.git", "pip2 install -r requirements.txt"))
    ]),

    "Mobile": OrderedDict([
        ("MobSF", ("https://github.com/MobSF/Mobile-Security-Framework-MobSF.git", "pip3 install -r requirements.txt")),
        ("Objection", ("https://github.com/sensepost/objection.git", "pip3 install objection")),
        ("Frida", ("https://github.com/frida/frida.git", "pip3 install frida-tools")),
        ("Apktool", ("https://github.com/iBotPeaches/Apktool.git", "")),
        ("jadx", ("https://github.com/skylot/jadx.git", "")),
        ("dex2jar", ("https://github.com/pxb1988/dex2jar.git", "")),
        ("AndroBugs", ("https://github.com/AndroBugs/AndroBugs_Framework.git", "")),
        ("Droid-Hunter", ("https://github.com/hahwul/Droid-Hunter.git", "")),
        ("MobileHackersWeapons", ("https://github.com/hahwul/MobileHackersWeapons.git", ""))
    ]),

    "Pentest": OrderedDict([
        ("Sn1per", ("https://github.com/1N3/Sn1per.git", "./install.sh")),
        ("CrackMapExec", ("https://github.com/byt3bl33d3r/CrackMapExec.git", "pip3 install -r requirements.txt")),
        ("Empire", ("https://github.com/EmpireProject/Empire.git", "./setup/install.sh")),
        ("Bettercap", ("https://github.com/bettercap/bettercap.git", "make build && make install")),
        ("Nmap", ("https://github.com/nmap/nmap.git", "./configure && make && make install")),
        ("Nikto", ("https://github.com/sullo/nikto.git", "")),
        ("WPSeku", ("https://github.com/m4ll0k/WPSeku.git", "pip3 install -r requirements.txt")),
        ("Jok3r", ("https://github.com/koutto/jok3r.git", "pip3 install -r requirements.txt")),
        ("Osmedeus", ("https://github.com/j3ssie/Osmedeus.git", "./install.sh")),
        ("RedHawk", ("https://github.com/Tuhinshubhra/RED_HAWK.git", "php install.php"))
    ]),

    "Reverse": OrderedDict([
        ("Radare2", ("https://github.com/radareorg/radare2.git", "./sys/install.sh")),
        ("Ghidra", ("https://github.com/NationalSecurityAgency/ghidra.git", "")),
        ("BinaryNinja", ("https://github.com/Vector35/binaryninja.git", "")),
        ("ROPgadget", ("https://github.com/JonathanSalwan/ROPgadget.git", "python setup.py install")),
        ("pwndbg", ("https://github.com/pwndbg/pwndbg.git", "./setup.sh")),
        ("GEF", ("https://github.com/hugsy/gef.git", "")),
        ("angr", ("https://github.com/angr/angr.git", "pip3 install angr")),
        ("RetDec", ("https://github.com/avast/retdec.git", ""))
    ]),

    "SpecialTools": OrderedDict([
        ("seeker", ("https://github.com/thewhiteh4t/seeker.git", "pip3 install -r requirements.txt")),
        ("ngrok", ("https://github.com/inconshreveable/ngrok.git", "make release-client")),
        ("anonphisher", ("https://github.com/Anonymous-Phunter/AnonPhisher.git", "")),
        ("zphisher", ("https://github.com/htr-tech/zphisher.git", "")),
        ("spcwa", ("https://github.com/MatrixTM/SPCWA.git", "")),
        ("CamPhish", ("https://github.com/techchipnet/CamPhish.git", "bash camphish.sh"))
    ])
}

if __name__ == "__main__":
    # Verifica e cria diretórios necessários
    os.makedirs(INSTALL_PATH, exist_ok=True)
    os.makedirs(os.path.join(INSTALL_PATH, "logs"), exist_ok=True)
    os.makedirs(os.path.join(INSTALL_PATH, "backups"), exist_ok=True)

    # Verifica privilégios root
    check_root()

    # Verifica auto-atualização
    if AUTO_UPDATE:
        self_update()
        check_for_updates()

    # Inicia o menu principal
    main_menu()

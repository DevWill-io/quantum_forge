import os
import sys
import pygame

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tela
WIDTH = 1100
HEIGHT = 700
FPS = 60
TITLE = "Quantum Forge"
SAVE_FILE = "savegame.json"

# Paleta de Cores
BG_DARK = (15, 17, 26)
BG_PANEL = (24, 28, 42)
BG_CARD = (34, 40, 58)
BG_CARD_HOVER = (45, 53, 77)
BG_CARD_DISABLED = (20, 22, 32)

ACCENT_CYAN = (0, 240, 255)
ACCENT_PURPLE = (180, 90, 255)
ACCENT_GOLD = (255, 200, 50)
ACCENT_GREEN = (50, 220, 120)
ACCENT_RED = (255, 75, 90)

TEXT_WHITE = (240, 245, 255)
TEXT_GRAY = (150, 160, 185)
TEXT_DARK = (15, 17, 26)

# Loja
UPGRADES_DATA = [
    {
        "id": "cursor",
        "name": "Luva Cinética",
        "desc": "+1 Energia por clique",
        "base_cost": 15,
        "cost_mult": 1.15,
        "click_power": 1,
        "eps": 0,
        "color": ACCENT_CYAN
    },
    {
        "id": "battery",
        "name": "Célula de Íons",
        "desc": "+2 Energia/seg",
        "base_cost": 50,
        "cost_mult": 1.15,
        "click_power": 0,
        "eps": 2,
        "color": ACCENT_GREEN
    },
    {
        "id": "coil",
        "name": "Bobina de Tesla",
        "desc": "+5 Clique e +8/seg",
        "base_cost": 250,
        "cost_mult": 1.18,
        "click_power": 5,
        "eps": 8,
        "color": ACCENT_PURPLE
    },
    {
        "id": "reactor",
        "name": "Reator de Fusão",
        "desc": "+45 Energia/seg",
        "base_cost": 1100,
        "cost_mult": 1.20,
        "click_power": 0,
        "eps": 45,
        "color": ACCENT_GOLD
    },
    {
        "id": "collider",
        "name": "Colisor de Hádrons",
        "desc": "+50 Clique e +220/seg",
        "base_cost": 5500,
        "cost_mult": 1.22,
        "click_power": 50,
        "eps": 220,
        "color": ACCENT_RED
    },
    {
        "id": "dyson",
        "name": "Esfera de Dyson",
        "desc": "+1.500 Energia/seg",
        "base_cost": 28000,
        "cost_mult": 1.25,
        "click_power": 250,
        "eps": 1500,
        "color": ACCENT_CYAN
    }
]

# Conquistas
ACHIEVEMENTS_DATA = [
    {"id": "first_click", "name": "Faísca Inicial", "desc": "Faça seu primeiro clique", "req_type": "clicks", "req_val": 1},
    {"id": "hundred_clicks", "name": "Dedo Rápido", "desc": "Alcance 100 cliques manuais", "req_type": "clicks", "req_val": 100},
    {"id": "energy_1k", "name": "Quilowatt", "desc": "Acumule 1.000 de energia total", "req_type": "total_energy", "req_val": 1000},
    {"id": "energy_100k", "name": "Megawatt", "desc": "Acumule 100.000 de energia total", "req_type": "total_energy", "req_val": 100000},
    {"id": "eps_100", "name": "Automação", "desc": "Atinja 100 de Energia/seg", "req_type": "eps", "req_val": 100},
    {"id": "first_prestige", "name": "Salto Quântico", "desc": "Realize seu primeiro Prestígio", "req_type": "prestige", "req_val": 1},
]

def format_number(num):
    """Formata números grandes para leitura fácil (ex: 1.50K, 2.30M)."""
    if num < 1000:
        return f"{int(num)}" if num == int(num) else f"{num:.1f}"
    suffixes = ["", "K", "M", "B", "T", "Qa", "Qi"]
    magnitude = 0
    while abs(num) >= 1000 and magnitude < len(suffixes) - 1:
        magnitude += 1
        num /= 1000.0
    return f"{num:.2f}{suffixes[magnitude]}"
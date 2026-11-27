import json
import os
import random
from config import UPGRADES_DATA, ACHIEVEMENTS_DATA, SAVE_FILE

class GameState:
    def __init__(self):
        self.energy = 0.0
        self.total_energy_earned = 0.0
        self.total_clicks = 0
        self.dark_matter = 0  # Moeda de Prestígio
        self.prestige_count = 0
        
        # Quantidade comprada
        self.upgrades = {u["id"]: 0 for u in UPGRADES_DATA}
        # IDs conquistas desbloqueadas
        self.unlocked_achievements = []
        
        # Bônus temporário
        self.frenzy_timer = 0.0
        self.frenzy_multiplier = 1.0

        self.load()

    def get_prestige_multiplier(self):
        return 1.0 + (self.dark_matter * 0.10)

    def get_click_power(self):
        base = 1.0
        for u in UPGRADES_DATA:
            base += u["click_power"] * self.upgrades[u["id"]]
        return base * self.get_prestige_multiplier() * self.frenzy_multiplier

    def get_eps(self):
        """Retorna Energia por Segundo (EPS)."""
        base = 0.0
        for u in UPGRADES_DATA:
            base += u["eps"] * self.upgrades[u["id"]]
        return base * self.get_prestige_multiplier() * self.frenzy_multiplier

    def get_upgrade_cost(self, upgrade_id):
        for u in UPGRADES_DATA:
            if u["id"] == upgrade_id:
                count = self.upgrades[upgrade_id]
                return int(u["base_cost"] * (u["cost_mult"] ** count))
        return 999999

    def click_core(self):
        self.total_clicks += 1
        # 10% de chance de clique crítico (3x dano)
        is_crit = random.random() < 0.10
        gain = self.get_click_power() * (3.0 if is_crit else 1.0)
        
        self.energy += gain
        self.total_energy_earned += gain
        return gain, is_crit

    def buy_upgrade(self, upgrade_id):
        cost = self.get_upgrade_cost(upgrade_id)
        if self.energy >= cost:
            self.energy -= cost
            self.upgrades[upgrade_id] += 1
            return True
        return False

    def calculate_pending_dark_matter(self):
        """Calcula quanta Matéria Escura o jogador ganha se resetar agora."""
        if self.total_energy_earned < 50000:
            return 0
        return int((self.total_energy_earned / 50000) ** 0.5)

    def do_prestige(self):
        pending = self.calculate_pending_dark_matter()
        if pending <= 0:
            return False
        
        self.dark_matter += pending
        self.prestige_count += 1
        
        self.energy = 0.0
        self.total_energy_earned = 0.0
        self.upgrades = {u["id"]: 0 for u in UPGRADES_DATA}
        self.frenzy_timer = 0.0
        self.frenzy_multiplier = 1.0
        self.save()
        return True

    def activate_frenzy(self, duration=15.0, mult=3.0):
        self.frenzy_timer = duration
        self.frenzy_multiplier = mult

    def update(self, dt):
        eps = self.get_eps()
        if eps > 0:
            generated = eps * dt
            self.energy += generated
            self.total_energy_earned += generated

        if self.frenzy_timer > 0:
            self.frenzy_timer -= dt
            if self.frenzy_timer <= 0:
                self.frenzy_timer = 0
                self.frenzy_multiplier = 1.0

        # Novas conquistas
        newly_unlocked = []
        for ach in ACHIEVEMENTS_DATA:
            if ach["id"] in self.unlocked_achievements:
                continue
            
            unlocked = False
            if ach["req_type"] == "clicks" and self.total_clicks >= ach["req_val"]:
                unlocked = True
            elif ach["req_type"] == "total_energy" and self.total_energy_earned >= ach["req_val"]:
                unlocked = True
            elif ach["req_type"] == "eps" and self.get_eps() >= ach["req_val"]:
                unlocked = True
            elif ach["req_type"] == "prestige" and self.prestige_count >= ach["req_val"]:
                unlocked = True

            if unlocked:
                self.unlocked_achievements.append(ach["id"])
                newly_unlocked.append(ach)

        return newly_unlocked

    def save(self):
        data = {
            "energy": self.energy,
            "total_energy_earned": self.total_energy_earned,
            "total_clicks": self.total_clicks,
            "dark_matter": self.dark_matter,
            "prestige_count": self.prestige_count,
            "upgrades": self.upgrades,
            "unlocked_achievements": self.unlocked_achievements
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar: {e}")

    def load(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.energy = data.get("energy", 0.0)
                self.total_energy_earned = data.get("total_energy_earned", 0.0)
                self.total_clicks = data.get("total_clicks", 0)
                self.dark_matter = data.get("dark_matter", 0)
                self.prestige_count = data.get("prestige_count", 0)
                saved_upgrades = data.get("upgrades", {})
                for k in self.upgrades:
                    self.upgrades[k] = saved_upgrades.get(k, 0)
                self.unlocked_achievements = data.get("unlocked_achievements", [])
        except Exception as e:
            print(f"Erro ao carregar save: {e}")
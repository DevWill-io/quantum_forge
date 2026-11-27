import pygame
import sys
import math
import random
from config import *
from sound_manager import SoundManager
from game_state import GameState
from ui import FloatingText, Particle, GoldenOrb, AchievementBanner

class QuantumForgeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.sound = SoundManager()
        self.state = GameState()

        self.font_xl = pygame.font.SysFont("segoeui", 38, bold=True)
        self.font_lg = pygame.font.SysFont("segoeui", 24, bold=True)
        self.font_md = pygame.font.SysFont("segoeui", 18, bold=True)
        self.font_sm = pygame.font.SysFont("segoeui", 14)

        self.core_center = (290, 370)
        self.core_base_radius = 95
        self.core_scale = 1.0
        self.core_angle = 0.0

        self.floating_texts = []
        self.particles = []
        self.banners = []
        self.golden_orb = None
        self.orb_spawn_timer = random.uniform(20, 40)

        self.active_tab = "upgrades"
        self.autosave_timer = 15.0

    def spawn_click_effects(self, pos, gain, is_crit):
        color = ACCENT_GOLD if is_crit else ACCENT_CYAN
        prefix = "CRÍTICO! +" if is_crit else "+"
        size = 30 if is_crit else 22
        self.floating_texts.append(
            FloatingText(pos[0], pos[1] - 20, f"{prefix}{format_number(gain)}", color, size)
        )
        for _ in range(18 if is_crit else 8):
            self.particles.append(Particle(pos[0], pos[1], color))

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.save()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.golden_orb and self.golden_orb.is_clicked(mouse_pos):
                    self.state.activate_frenzy(duration=15.0, mult=3.0)
                    self.sound.play("achievement")
                    self.floating_texts.append(FloatingText(mouse_pos[0], mouse_pos[1], "FRENESI 3X (15s)!", ACCENT_GOLD, 28))
                    self.golden_orb = None
                    continue

                dist = math.hypot(mouse_pos[0] - self.core_center[0], mouse_pos[1] - self.core_center[1])
                if dist <= self.core_base_radius * self.core_scale:
                    gain, is_crit = self.state.click_core()
                    self.core_scale = 0.88  # Efeito de compressão ao clicar
                    self.sound.play("crit" if is_crit else "click")
                    self.spawn_click_effects(mouse_pos, gain, is_crit)
                    continue

                btn_sound = pygame.Rect(20, 20, 110, 34)
                btn_save = pygame.Rect(140, 20, 110, 34)
                if btn_sound.collidepoint(mouse_pos):
                    self.sound.toggle()
                    continue
                if btn_save.collidepoint(mouse_pos):
                    self.state.save()
                    self.floating_texts.append(FloatingText(195, 65, "Jogo Salvo!", ACCENT_GREEN, 16))
                    continue

                tab_w = 160
                for idx, tab_id in enumerate(["upgrades", "achievements", "prestige"]):
                    tab_rect = pygame.Rect(580 + idx * (tab_w + 10), 25, tab_w, 42)
                    if tab_rect.collidepoint(mouse_pos):
                        self.active_tab = tab_id
                        self.sound.play("click")

                if self.active_tab == "upgrades":
                    for i, u in enumerate(UPGRADES_DATA):
                        card_rect = pygame.Rect(580, 85 + i * 95, 500, 82)
                        if card_rect.collidepoint(mouse_pos):
                            if self.state.buy_upgrade(u["id"]):
                                self.sound.play("buy")
                                for _ in range(12):
                                    self.particles.append(Particle(mouse_pos[0], mouse_pos[1], u["color"]))
                            else:
                                self.sound.play("error")

                elif self.active_tab == "prestige":
                    prestige_btn = pygame.Rect(650, 420, 360, 60)
                    if prestige_btn.collidepoint(mouse_pos):
                        if self.state.do_prestige():
                            self.sound.play("achievement")
                            self.banners.append(AchievementBanner("Salto Quântico!", "Produção multiplicada com Matéria Escura!"))
                        else:
                            self.sound.play("error")

    def update(self, dt):
        self.core_scale += (1.0 - self.core_scale) * 12 * dt
        self.core_angle += (40 + min(200, self.state.get_eps() * 0.2)) * dt

        unlocked = self.state.update(dt)
        for ach in unlocked:
            self.sound.play("achievement")
            self.banners.append(AchievementBanner(ach["name"], ach["desc"]))

        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]
        self.particles = [p for p in self.particles if p.update(dt)]
        self.banners = [b for b in self.banners if b.update(dt)]

        if self.golden_orb:
            if not self.golden_orb.update(dt):
                self.golden_orb = None
        else:
            self.orb_spawn_timer -= dt
            if self.orb_spawn_timer <= 0:
                self.golden_orb = GoldenOrb()
                self.orb_spawn_timer = random.uniform(25, 45)

        # Auto-Save 
        self.autosave_timer -= dt
        if self.autosave_timer <= 0:
            self.state.save()
            self.autosave_timer = 15.0

    def draw_core_area(self):
        pygame.draw.rect(self.screen, BG_PANEL, (15, 15, 540, HEIGHT - 30), border_radius=16)

        # Botões Som e Salvar
        btn_sound = pygame.Rect(25, 25, 110, 32)
        btn_save = pygame.Rect(145, 25, 110, 32)
        pygame.draw.rect(self.screen, BG_CARD, btn_sound, border_radius=8)
        pygame.draw.rect(self.screen, BG_CARD, btn_save, border_radius=8)

        snd_txt = "Som: ON" if self.sound.enabled else "Som: OFF"
        self.screen.blit(self.font_sm.render(snd_txt, True, ACCENT_CYAN if self.sound.enabled else TEXT_GRAY), (48, 32))
        self.screen.blit(self.font_sm.render("Salvar Agora", True, TEXT_WHITE), (158, 32))

        energy_str = f"{format_number(self.state.energy)} J"
        eps_str = f"{format_number(self.state.get_eps())} J / seg"
        click_str = f"Poder do Clique: {format_number(self.state.get_click_power())} J"

        surf_energy = self.font_xl.render(energy_str, True, ACCENT_CYAN)
        surf_eps = self.font_lg.render(eps_str, True, ACCENT_GREEN)
        surf_click = self.font_sm.render(click_str, True, TEXT_GRAY)

        self.screen.blit(surf_energy, surf_energy.get_rect(center=(285, 115)))
        self.screen.blit(surf_eps, surf_eps.get_rect(center=(285, 155)))
        self.screen.blit(surf_click, surf_click.get_rect(center=(285, 185)))

        if self.state.frenzy_timer > 0:
            frenzy_lbl = self.font_md.render(f"FRENESI 3X ATIVO: {self.state.frenzy_timer:.1f}s", True, ACCENT_GOLD)
            self.screen.blit(frenzy_lbl, frenzy_lbl.get_rect(center=(285, 220)))

        cx, cy = self.core_center
        r = int(self.core_base_radius * self.core_scale)

        glow_color = ACCENT_GOLD if self.state.frenzy_timer > 0 else ACCENT_CYAN
        pygame.draw.circle(self.screen, (25, 45, 65), (cx, cy), r + 28)

        for i in range(3):
            ang = math.radians(self.core_angle + i * 120)
            ox = cx + math.cos(ang) * (r + 22)
            oy = cy + math.sin(ang) * (r + 22)
            pygame.draw.circle(self.screen, ACCENT_PURPLE, (int(ox), int(oy)), 7)

        pygame.draw.circle(self.screen, glow_color, (cx, cy), r)
        pygame.draw.circle(self.screen, BG_DARK, (cx, cy), int(r * 0.78))
        pygame.draw.circle(self.screen, glow_color, (cx, cy), int(r * 0.55))

        lbl_core = self.font_md.render("CLIQUE", True, TEXT_DARK)
        self.screen.blit(lbl_core, lbl_core.get_rect(center=(cx, cy)))

        # Estatísticas
        stats_y = 550
        pygame.draw.line(self.screen, BG_CARD, (45, stats_y - 15), (525, stats_y - 15), 2)
        s1 = self.font_sm.render(f"Cliques Totais: {format_number(self.state.total_clicks)}", True, TEXT_GRAY)
        s2 = self.font_sm.render(f"Energia Histórica: {format_number(self.state.total_energy_earned)} J", True, TEXT_GRAY)
        s3 = self.font_sm.render(f"Matéria Escura: {self.state.dark_matter} (+{self.state.dark_matter * 10}% bônus)", True, ACCENT_PURPLE)
        
        self.screen.blit(s1, (45, stats_y))
        self.screen.blit(s2, (45, stats_y + 25))
        self.screen.blit(s3, (45, stats_y + 50))

    def draw_right_panel(self):
        mouse_pos = pygame.mouse.get_pos()

        tabs = [
            ("upgrades", "FORJA (LOJA)"),
            ("achievements", f"CONQUISTAS ({len(self.state.unlocked_achievements)}/{len(ACHIEVEMENTS_DATA)})"),
            ("prestige", "PRESTÍGIO")
        ]
        tab_w = 160
        for idx, (tab_id, label) in enumerate(tabs):
            rect = pygame.Rect(580 + idx * (tab_w + 10), 25, tab_w, 42)
            is_active = (self.active_tab == tab_id)
            color = ACCENT_CYAN if is_active else BG_CARD
            txt_color = TEXT_DARK if is_active else TEXT_WHITE
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            lbl = self.font_sm.render(label, True, txt_color)
            self.screen.blit(lbl, lbl.get_rect(center=rect.center))

        # LOJA DE UPGRADES
        if self.active_tab == "upgrades":
            for i, u in enumerate(UPGRADES_DATA):
                card_rect = pygame.Rect(580, 85 + i * 95, 500, 82)
                cost = self.state.get_upgrade_cost(u["id"])
                can_afford = self.state.energy >= cost
                owned = self.state.upgrades[u["id"]]

                if can_afford:
                    bg = BG_CARD_HOVER if card_rect.collidepoint(mouse_pos) else BG_CARD
                else:
                    bg = BG_CARD_DISABLED

                pygame.draw.rect(self.screen, bg, card_rect, border_radius=12)
                border_col = u["color"] if can_afford else (50, 55, 70)
                pygame.draw.rect(self.screen, border_col, card_rect, 2, border_radius=12)

                name_surf = self.font_md.render(u["name"], True, TEXT_WHITE if can_afford else TEXT_GRAY)
                desc_surf = self.font_sm.render(u["desc"], True, u["color"] if can_afford else TEXT_GRAY)
                cost_surf = self.font_md.render(f"Custo: {format_number(cost)} J", True, ACCENT_GOLD if can_afford else ACCENT_RED)
                cnt_surf = self.font_xl.render(str(owned), True, TEXT_WHITE if owned > 0 else TEXT_GRAY)

                self.screen.blit(name_surf, (card_rect.x + 16, card_rect.y + 12))
                self.screen.blit(desc_surf, (card_rect.x + 16, card_rect.y + 44))
                self.screen.blit(cost_surf, (card_rect.x + 250, card_rect.y + 28))
                self.screen.blit(cnt_surf, cnt_surf.get_rect(midright=(card_rect.right - 20, card_rect.centery)))

        # CONQUISTAS
        elif self.active_tab == "achievements":
            for i, ach in enumerate(ACHIEVEMENTS_DATA):
                card_rect = pygame.Rect(580, 85 + i * 95, 500, 82)
                unlocked = ach["id"] in self.state.unlocked_achievements
                bg = BG_CARD if unlocked else BG_CARD_DISABLED
                border = ACCENT_GOLD if unlocked else (45, 50, 65)

                pygame.draw.rect(self.screen, bg, card_rect, border_radius=12)
                pygame.draw.rect(self.screen, border, card_rect, 2, border_radius=12)

                status = "[DESBLOQUEADA]" if unlocked else "[BLOQUEADA]"
                title_col = ACCENT_GOLD if unlocked else TEXT_GRAY
                
                t_surf = self.font_md.render(f"{ach['name']}  {status}", True, title_col)
                d_surf = self.font_sm.render(ach["desc"], True, TEXT_WHITE if unlocked else TEXT_GRAY)
                self.screen.blit(t_surf, (card_rect.x + 18, card_rect.y + 14))
                self.screen.blit(d_surf, (card_rect.x + 18, card_rect.y + 45))

        # PRESTÍGIO
        elif self.active_tab == "prestige":
            panel = pygame.Rect(580, 85, 500, 580)
            pygame.draw.rect(self.screen, BG_PANEL, panel, border_radius=14)

            pending = self.state.calculate_pending_dark_matter()
            
            lines = [
                ("COLAPSO QUÂNTICO (PRESTÍGIO)", self.font_lg, ACCENT_PURPLE, 130),
                ("Reinicie sua energia e construções para converter", self.font_sm, TEXT_GRAY, 180),
                ("seu progresso em Matéria Escura permanente.", self.font_sm, TEXT_GRAY, 205),
                (f"Matéria Escura Atual: {self.state.dark_matter}", self.font_md, TEXT_WHITE, 260),
                (f"Bônus Global Atual: +{self.state.dark_matter * 10}%", self.font_md, ACCENT_GREEN, 290),
                (f"Ao reiniciar agora você ganhará: +{pending} Matéria Escura", self.font_md, ACCENT_GOLD, 350),
                ("(Requer pelo menos 50.000 J acumulados na sessão)", self.font_sm, TEXT_GRAY, 380),
            ]
            for text, font, col, y_pos in lines:
                s = font.render(text, True, col)
                self.screen.blit(s, s.get_rect(center=(830, y_pos)))

            btn_rect = pygame.Rect(650, 420, 360, 60)
            can_prestige = pending > 0
            btn_col = ACCENT_PURPLE if can_prestige else BG_CARD_DISABLED
            pygame.draw.rect(self.screen, btn_col, btn_rect, border_radius=12)
            btn_lbl = self.font_md.render("REALIZAR SALTO QUÂNTICO", True, TEXT_WHITE if can_prestige else TEXT_GRAY)
            self.screen.blit(btn_lbl, btn_lbl.get_rect(center=btn_rect.center))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)

            # Renderização
            self.screen.fill(BG_DARK)
            self.draw_core_area()
            self.draw_right_panel()

            if self.golden_orb:
                self.golden_orb.draw(self.screen)

            for p in self.particles:
                p.draw(self.screen)

            for ft in self.floating_texts:
                ft.draw(self.screen)

            for b in self.banners:
                b.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    game = QuantumForgeGame()
    game.run()
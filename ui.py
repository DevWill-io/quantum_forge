import pygame
import random
import math
from config import *

class FloatingText:
    def __init__(self, x, y, text, color=ACCENT_CYAN, size=24):
        self.x = x + random.randint(-20, 20)
        self.y = y + random.randint(-10, 10)
        self.text = text
        self.color = color
        self.alpha = 255
        self.vy = -70.0  
        self.font = pygame.font.SysFont("segoeui", size, bold=True)

    def update(self, dt):
        self.y += self.vy * dt
        self.alpha -= 220 * dt
        return self.alpha > 0

    def draw(self, surface):
        txt_surf = self.font.render(self.text, True, self.color)
        txt_surf.set_alpha(max(0, int(self.alpha)))
        rect = txt_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(txt_surf, rect)


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(60, 220)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.life = random.uniform(0.3, 0.7)
        self.max_life = self.life
        self.radius = random.randint(3, 6)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surface):
        ratio = max(0, self.life / self.max_life)
        r = max(1, int(self.radius * ratio))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), r)


class GoldenOrb:
    """Evento aleatório que aparece na tela dando bônus de Frenesi 3x."""
    def __init__(self):
        self.x = random.randint(100, 480)
        self.y = random.randint(150, 580)
        self.radius = 24
        self.life = 8.0  
        self.pulse = 0.0

    def update(self, dt):
        self.life -= dt
        self.pulse += dt * 6
        return self.life > 0

    def is_clicked(self, pos):
        dist = math.hypot(pos[0] - self.x, pos[1] - self.y)
        return dist <= self.radius + 5

    def draw(self, surface):
        r = self.radius + int(math.sin(self.pulse) * 4)
        pygame.draw.circle(surface, (255, 230, 120), (self.x, self.y), r + 6, 2)
        pygame.draw.circle(surface, ACCENT_GOLD, (self.x, self.y), r)
        font = pygame.font.SysFont("segoeui", 14, bold=True)
        lbl = font.render("3X", True, TEXT_DARK)
        surface.blit(lbl, lbl.get_rect(center=(self.x, self.y)))


class AchievementBanner:
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc
        self.timer = 4.0

    def update(self, dt):
        self.timer -= dt
        return self.timer > 0

    def draw(self, surface):
        rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 85, 360, 65)
        pygame.draw.rect(surface, BG_CARD, rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT_GOLD, rect, 2, border_radius=10)
        
        f_title = pygame.font.SysFont("segoeui", 16, bold=True)
        f_desc = pygame.font.SysFont("segoeui", 14)
        
        t_surf = f_title.render(f"CONQUISTA: {self.title}", True, ACCENT_GOLD)
        d_surf = f_desc.render(self.desc, True, TEXT_WHITE)
        
        surface.blit(t_surf, (rect.x + 15, rect.y + 10))
        surface.blit(d_surf, (rect.x + 15, rect.y + 34))
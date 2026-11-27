import pygame
import math
import array

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sample_rate = 44100
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=512)
            self._generate_sounds()
        except Exception as e:
            print(f"Aviso: Áudio desativado ({e})")
            self.enabled = False

    def _synthesize(self, freq_start, freq_end, duration, volume=0.3, wave_type="sine"):
        """Gera um objeto pygame.mixer.Sound proceduralmente."""
        n_samples = int(self.sample_rate * duration)
        buf = array.array("h")
        max_amp = int(32767 * volume)

        for i in range(n_samples):
            t = i / n_samples
            freq = freq_start + (freq_end - freq_start) * t
            envelope = (1.0 - t) ** 1.5
            
            angle = 2.0 * math.pi * freq * (i / self.sample_rate)
            if wave_type == "sine":
                val = math.sin(angle)
            elif wave_type == "square":
                val = 1.0 if math.sin(angle) >= 0 else -1.0
            elif wave_type == "triangle":
                val = 2.0 * abs(2.0 * (angle / (2 * math.pi) - math.floor(angle / (2 * math.pi) + 0.5))) - 1.0
            else:
                val = math.sin(angle)

            sample = int(val * max_amp * envelope)
            buf.append(sample)

        return pygame.mixer.Sound(buffer=buf)

    def _generate_sounds(self):
        # Som clique
        self.sounds["click"] = self._synthesize(520, 880, 0.06, volume=0.25, wave_type="sine")
        # Som de crítico
        self.sounds["crit"] = self._synthesize(880, 1400, 0.12, volume=0.35, wave_type="triangle")
        # Som compra
        self.sounds["buy"] = self._synthesize(330, 660, 0.14, volume=0.3, wave_type="triangle")
        # Som  erro
        self.sounds["error"] = self._synthesize(160, 110, 0.15, volume=0.25, wave_type="square")
        # Som conquista
        self.sounds["achievement"] = self._synthesize(440, 1100, 0.35, volume=0.35, wave_type="sine")

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled
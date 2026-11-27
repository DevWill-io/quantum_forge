# ⚛️ Quantum Forge — Clicker Game

Um jogo estilo **Incremental / Clicker** com temática Sci-Fi desenvolvido em **Python** e **Pygame**, construído com arquitetura modular e **síntese de áudio procedural em tempo real** (sem dependência de arquivos externos de som ou imagem).

---

## ✨ Funcionalidades

* **Núcleo Quântico Interativo:** Clique para gerar energia com animações de compressão, partículas dinâmicas, números flutuantes e **10% de chance de Acerto Crítico (3x)**.
* **Áudio Procedural (`sound_manager.py`):** Efeitos sonoros gerados matematicamente na memória via ondas senoidais, quadradas e triangulares — zero arquivos `.wav` ou `.mp3` necessários.
* **Loja de Tecnologias:** 6 upgrades progressivos (de *Luva Cinética* até *Esfera de Dyson*) que aumentam tanto o poder do clique quanto a produção passiva por segundo (`J/s`).
* **Eventos Aleatórios (Orbe Dourado):** Aparece periodicamente na tela e ativa o modo **Frenesi 3x** por 15 segundos ao ser clicado.
* **Sistema de Prestígio (Salto Quântico):** Reinicie sua sessão ao atingir 50.000 J para converter seu progresso em **Matéria Escura**, garantindo bônus permanentes de +10% por unidade.
* **Conquistas e Auto-Save:** Sistema de notificações pop-up para metas alcançadas e salvamento automático a cada 15 segundos em `savegame.json`.

---

## 📁 Estrutura do Projeto

```text
quantum_forge/
├── main.py          # Loop principal, captura de eventos e renderização
├── config.py        # Paleta de cores, constantes, balanceamento e caminhos
├── sound_manager.py # Sintetizador de áudio procedural em tempo real
├── game_state.py    # Economia, multiplicadores, conquistas e Save/Load JSON
├── ui.py            # Partículas, textos flutuantes, Orbe Dourado e banners
└── README.md        # Documentação do projeto

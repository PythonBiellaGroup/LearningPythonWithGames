# 🎮 Stranger Stars

Un gioco di abilità ispirato alla serie TV **Stranger Things**, realizzato con **Pygame Zero** per scopi didattici.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame Zero](https://img.shields.io/badge/Pygame%20Zero-1.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Descrizione

**Stranger Stars** è un gioco dove devi salvare il tuo personaggio preferito di Stranger Things mentre cade (o sale!) insieme ad altri personaggi. Attenzione: ogni tanto entrerai nel **Sottosopra**, dove la gravità si inverte e tutto diventa più caotico!

### 🎯 Obiettivo

- Clicca il personaggio corretto tra quelli che cadono sullo schermo
- Supera tutti i 10 livelli senza sbagliare
- Sopravvivi alle inversioni casuali del Sottosopra!

## 🎬 Come si gioca

1. **Scegli il personaggio**: All'inizio scegli quale dei 5 personaggi vuoi salvare
2. **Clicca veloce**: Durante il gioco, clicca solo il TUO personaggio mentre cade
3. **Attenzione al Sottosopra**: Periodicamente la gravità si inverte e tutto diventa più difficile!
4. **Game Over**: Se clicchi il personaggio sbagliato o lo lasci cadere, hai perso
5. **Vittoria**: Supera tutti i 10 livelli per vincere!

### 📊 Difficoltà crescente

Ogni livello aumenta:
- ⚡ Il numero di personaggi sullo schermo
- 🚀 La velocità di caduta
- 🌀 La frequenza del Sottosopra

## 🛠️ Installazione

### Prerequisiti

- Python 3.7 o superiore
- Pygame Zero

### Setup

1. **Clona il repository**
   ```bash
   git clone https://github.com/tuousername/stranger-stars.git
   cd stranger-stars
   ```

2. **Installa Pygame Zero**
   ```bash
   pip install pgzero
   ```

3. **Verifica la struttura del progetto**
   ```
   stranger-stars/
   ├── stranger_stars.py          # File principale del gioco
   ├── images/                    # Cartella delle immagini
   │   ├── dustin.png
   │   ├── lucas.png
   │   ├── mike.png
   │   ├── undici.png
   │   ├── will.png
   │   ├── sfondo.png
   │   └── sfondo-sottosopra.png
   └── README.md
   ```

4. **Avvia il gioco**
   ```bash
   python stranger_stars.py
   ```

   oppure con Pygame Zero direttamente:
   ```bash
   pgzrun stranger_stars.py
   ```

## 🎨 Personaggi disponibili

- 🧢 **Dustin** - Il simpatico genio del gruppo
- 🎯 **Lucas** - Il tiratore scelto con la fionda
- 🚴 **Mike** - Il leader del gruppo
- 🔮 **Undici (Eleven)** - La ragazza con i poteri telecinetici
- 🎨 **Will** - L'artista che è stato nel Sottosopra

## 🎓 Aspetti didattici

Questo gioco è stato creato come progetto educativo per insegnare:

### Concetti di programmazione
- ✅ **Variabili globali e locali**
- ✅ **Funzioni e modularizzazione del codice**
- ✅ **Liste e gestione delle collezioni**
- ✅ **Condizioni (if/else)**
- ✅ **Cicli (for/while)**
- ✅ **Gestione degli eventi** (mouse, timer)

### Concetti di game development
- 🎮 **Game loop** (update/draw)
- 🎯 **Collision detection**
- 📊 **Gestione degli stati** (menu, gioco, game over)
- 🎨 **Rendering e grafica**
- ⏱️ **Timer e animazioni**
- 🌊 **Movimento sinusoidale** (oscillazione)

### Struttura del codice

Il codice è organizzato in sezioni chiare:

```python
# 1. COSTANTI - Valori fissi del gioco
WIDTH = 800
HEIGHT = 600

# 2. VARIABILI DI STATO - Stato corrente del gioco
livello_corrente = 1
gioco_terminato = False

# 3. FUNZIONI PRINCIPALI
def draw():      # Disegna tutto
def update():    # Aggiorna logica
def on_mouse_down(): # Gestisce input

# 4. FUNZIONI DI SUPPORTO
def genera_personaggi():
def muovi_personaggi():
def attiva_sottosopra():
```

## 🔧 Personalizzazione

### Modificare la difficoltà

Puoi facilmente modificare le costanti nel codice per rendere il gioco più facile o difficile:

```python
# Velocità dei personaggi
VELOCITA_BASE_MIN = 0.3  # Riduci per rallentare
VELOCITA_BASE_MAX = 0.6  # Aumenta per accelerare

# Frequenza del Sottosopra
TEMPO_MIN_SOTTOSOPRA = 3  # Aumenta per meno caos
TEMPO_MAX_SOTTOSOPRA = 10 # Riduci per più Sottosopra
```

### Aggiungere nuovi personaggi

1. Aggiungi l'immagine nella cartella `images/` (es. `max.png`)
2. Aggiungi il nome alla lista:
   ```python
   LISTA_PERSONAGGI = ["dustin", "lucas", "mike", "undici", "will", "max"]
   ```

## 🐛 Problemi comuni

### Il gioco non parte
- Verifica di aver installato Pygame Zero: `pip install pgzero`
- Controlla che tutte le immagini siano nella cartella `images/`

### Le immagini non si vedono
- Pygame Zero cerca le immagini in una cartella chiamata esattamente `images` (minuscolo)
- I nomi dei file devono corrispondere esattamente a quelli nel codice

### Il gioco è troppo veloce/lento
- Modifica le costanti `VELOCITA_BASE_MIN` e `VELOCITA_BASE_MAX`

## 📚 Risorse utili

- [Documentazione Pygame Zero](https://pygame-zero.readthedocs.io/)
- [Tutorial Python](https://docs.python.org/it/3/tutorial/)
- [Stranger Things su Netflix](https://www.netflix.com/title/80057281)

## 🤝 Contribuire

Contributi, issues e feature requests sono benvenuti!

1. Fai un Fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa i cambiamenti (`git commit -m 'Add some AmazingFeature'`)
4. Pusha il branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Idee per miglioramenti

- [ ] Sistema di punteggio
- [ ] Suoni ed effetti sonori
- [ ] Power-up speciali
- [ ] Modalità multiplayer
- [ ] Leaderboard locale
- [ ] Più livelli e boss fight
- [ ] Animazioni dei personaggi

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## 👨‍💻 Autore

Creato per scopi didattici da **Python Biella Group**.

## 🙏 Crediti

- Serie TV: **Stranger Things** © Netflix
- Engine: **Pygame Zero**
- Ispirazione: La community dei game developer Python

---

⭐ Se questo progetto ti è stato utile, lascia una stella su GitHub!

🐛 Hai trovato un bug? [Apri un issue](https://github.com/tuousername/stranger-stars/issues)

💡 Hai un'idea? [Condividila nelle discussions](https://github.com/tuousername/stranger-stars/discussions)

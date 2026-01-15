# 🎮 Imparare Python Programmando Giochi

> *Impara Python divertendoti! Un percorso completo per trasformare la teoria in pratica attraverso la creazione di videogiochi.*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyGame Zero](https://img.shields.io/badge/PyGame%20Zero-Latest-green.svg)](https://pygame-zero.readthedocs.io/)
[![Licenza](https://img.shields.io/badge/Licenza-MIT-yellow.svg)](LICENSE)
[![Difficoltà](https://img.shields.io/badge/Difficoltà-Principiante%20→%20Intermedio-orange.svg)]()

---

## 📚 Cosa Troverai Qui

Questo repository contiene una **collezione progressiva di giochi** creati con **PyGame Zero**, pensati per insegnare Python in modo pratico e coinvolgente. Ogni gioco introduce nuovi concetti di programmazione, dalle basi fino a tecniche più avanzate.

**Perfetto per:**
- 🎓 Studenti delle scuole superiori
- 👨‍🏫 Insegnanti che vogliono materiale didattico interattivo
- 🚀 Autodidatti che vogliono imparare Python in modo divertente
- 👨‍💻 Chiunque voglia capire la programmazione attraverso progetti concreti

**Risorse principali:** 🇮🇹 **Italiano**

---

## 🎯 I Giochi

### 📺 Presentati nei Video Tutorial

| Gioco | Difficoltà | Concetti Chiave |
|-------|-----------|----------------|
| **game01** - Colpisci l'Alieno | ⭐ Facile | Eventi mouse, sprite, collisioni base |
| **game02** - Ape Golosa | ⭐ Facile | Movimento, raccolta oggetti, punteggio |
| **game03** - Connetti i Satelliti | ⭐⭐ Medio | Pathfinding, grafi, logica di gioco |
| **game04** - Stella Rossa | ⭐⭐ Medio | Animazioni, timing, gestione stato |
| **game05** - Quiz | ⭐ Facile | Input utente, logica condizionale, UI |
| **game06** - Mongolfiera | ⭐⭐ Medio | Fisica semplice, gravità, controlli |
| **game07** - Flappy Bird | ⭐⭐⭐ Difficile | Game loop, fisica, collision detection |
| **game08** - Karate Kid | ⭐⭐ Medio | Combo, timing preciso, feedback visivo |
| **game09** - Stelle | ⭐⭐ Medio | Generazione procedurale, pattern |
| **game10** - Invasione dallo Spazio | ⭐⭐⭐ Difficile | Nemici multipli, proiettili, game over |

### 🎁 Giochi Bonus (Non nei Video)

| Gioco | Difficoltà | Highlight |
|-------|-----------|-----------|
| **game02_1** - Tony alla Ricerca della Musica | ⭐⭐ Medio | Ricerca file, debugging, percorsi |
| **game04_1** - Stranger Stars | ⭐⭐⭐ Difficile | Debug avanzato, correzione errori |
| **game11** - La Battaglia Finale: Harry vs Voldemort | ⭐⭐⭐⭐ Avanzato | 🔥 **CSV, Polars, DataFrames, AI base, sistema a turni** |

> 💡 **Novità!** Il game11 introduce concetti di **Data Science** e **AI/ML** usando Polars per gestire dati tabulari (incantesimi) e creare un'intelligenza artificiale per Voldemort!

---

## 🎥 Video Tutorial (YouTube)

Un **corso completo gratuito** di circa 8 ore totali, suddiviso in sessioni tematiche:

| # | Titolo | Durata | Link |
|---|--------|--------|------|
| **1** | Introduzione a Python e basi della programmazione | ~2h | [▶️ Guarda](https://youtu.be/zjXXappgQak) |
| **2** | Introduzione a PyGame Zero e primi giochi | ~2h | [▶️ Guarda](https://youtu.be/qqv4d4IbOpM) |
| **3** | Tris di giochi a difficoltà crescente | ~2h | [▶️ Guarda](https://youtu.be/5BB3_hGxU9o) |
| **4** | Quattro giochi avanzati | ~2h | [▶️ Guarda](https://youtu.be/Mks0j17dv8g) |
| **BONUS** | Intervista a Daniel Pope (creatore di PyGame Zero) | ~30min | [▶️ Guarda](https://youtu.be/OXWRhpfB7mQ) |

---

## 🚀 Come Iniziare

### Prerequisiti

```bash
# Python 3.8 o superiore
python --version

# Installa PyGame Zero
pip install pgzero

# Per il game11 (Battaglia Harry vs Voldemort)
pip install polars
```

### Clona il Repository

```bash
git clone https://github.com/PythonBiellaGroup/LearningPythonWithGames.git
cd LearningPythonWithGames
```

### Esegui un Gioco

```bash
# Metodo 1: Con Python
python game01.py

# Metodo 2: Con pgzrun (se configurato)
pgzrun game01.py
```

---

## 📖 Struttura del Progetto

```
LearningPythonWithGames/
├── game01/ - game10/     # Giochi dei video tutorial
├── game02_1/             # Tony alla ricerca della musica
├── game04_1/             # Stranger Stars (debugging)
├── game11/               # Harry vs Voldemort (CSV + Polars)
│   ├── harry_voldemort.py
│   ├── spells.csv        # Database incantesimi
│   └── images/           # Sprite e sfondi
├── images/               # Risorse grafiche condivise
├── sounds/               # Effetti sonori (se presenti)
└── README.md
```

---

## 🎓 Percorso di Apprendimento Consigliato

### 🟢 **Livello 1: Fondamentali** (Settimana 1-2)
1. game01 - Colpisci l'Alieno
2. game02 - Ape Golosa
3. game05 - Quiz

**Cosa impari:** Variabili, funzioni, eventi, sprite, collisioni

---

### 🟡 **Livello 2: Intermedio** (Settimana 3-4)
4. game03 - Connetti i Satelliti
5. game04 - Stella Rossa
6. game06 - Mongolfiera
7. game08 - Karate Kid

**Cosa impari:** Liste, dizionari, animazioni, fisica base, stato del gioco

---

### 🔴 **Livello 3: Avanzato** (Settimana 5-6)
8. game07 - Flappy Bird
9. game09 - Stelle
10. game10 - Invasione dallo Spazio
11. game04_1 - Stranger Stars (debugging)

**Cosa impari:** Game loop complessi, OOP, gestione errori, ottimizzazione

---

### 🔵 **Livello 4: Data & AI** (Settimana 7+)
12. game11 - Harry vs Voldemort

**Cosa impari:** 
- 📊 Lavorare con CSV e DataFrames (Polars)
- 🤖 Creare un'AI semplice
- 🎯 Sistema a turni
- 📈 Manipolazione dati tabulari

---

## 🛠️ Strumenti e Tecnologie

- **Python 3.8+** - Linguaggio di programmazione
- **PyGame Zero** - Framework per creare giochi senza complessità
- **Polars** (game11) - Libreria velocissima per DataFrames
- **CSV** (game11) - Formato per salvare dati tabulari

---

## 📚 Risorse Didattiche

### 📖 Documentazione Ufficiale

- [PyGame Zero - Documentazione](https://pygame-zero.readthedocs.io/en/stable/principles.html)
- [PyGame Zero - PDF Completo](https://buildmedia.readthedocs.org/media/pdf/pygame-zero/latest/pygame-zero.pdf)
- [Polars - Guida Rapida](https://docs.pola.rs/)

### 📘 Libri e Guide

- [PyGame Zero Book](https://electronstudio.github.io/pygame-zero-book/) - Libro interattivo gratuito
- [Simple Game Tutorials](https://simplegametutorials.github.io/pygamezero/) - Tutorial step-by-step
- [PyGame Zero Cheat Sheet](https://github.com/markmillr/pgzero-teaching-resources/blob/master/pygame-zero-cheatsheet-pintman-en.pdf) - Riferimento rapido

### 🎯 Workshop e Tutorial

- [PyGame Zero Workshop](https://github.com/rbricheno/pygamezero-workshop)
- [Teaching Resources](https://github.com/markmillr/pgzero-teaching-resources)
- [Teach Your Kid to Code](https://www.mattlayman.com/blog/2019/teach-kid-code-pygame-zero/)

---

## 🌍 Altri Esempi e Progetti

### Repository Ufficiali

- [Esempi Ufficiali PyGame Zero](https://github.com/lordmauve/pgzero/tree/master/examples)
- [Code the Classics](https://github.com/Wireframe-Magazine/Code-the-Classics) - Remake di giochi classici

### Collezioni Community

- [TechnoVisual Examples](https://github.com/TechnoVisual/Pygame-Zero)
- [PyGame Zero Examples](https://github.com/rajasekaranap/pygamezero-examples)
- [Eric Clack Tutorials](https://github.com/ericclack) - Giochi con tutorial completi
- [Kantel Collection](https://github.com/kantel/pygamezero)

---

## 🎮 Prova Online (Senza Installare)

Non vuoi installare Python? Prova questi ambienti online:

- [**WithCode.uk**](https://create.withcode.uk/) - Editor online per PyGame Zero
- [**Repl.it**](https://repl.it/languages/pygame) - IDE completo nel browser

---

## 🔧 Librerie Utili per PyGame Zero

### PyGame Zero Helper
Estensione con funzioni aggiuntive per semplificare lo sviluppo:
- [Documentazione e Download](https://www.aposteriori.com.sg/pygame-zero-helper/)

---

## 🤝 Come Contribuire

Hai creato un nuovo gioco? Hai migliorato uno esistente? **Contribuisci!**

1. Fai un **fork** del repository
2. Crea un branch: `git checkout -b feature/mio-gioco`
3. Aggiungi il tuo gioco con documentazione
4. Commit: `git commit -m 'Add: Nuovo gioco X'`
5. Push: `git push origin feature/mio-gioco`
6. Apri una **Pull Request**

### Idee per Contributi

- ✨ Nuovi giochi con tutorial
- 🐛 Correzione bug
- 📚 Traduzione documentazione
- 🎨 Nuovi asset grafici/sonori
- 📝 Miglioramenti al README

---

## 💬 Community e Supporto

- 💬 **Discord**: [Python Biella Group](https://discord.gg/pythonbiella) *(link da aggiornare)*
- 🐦 **Twitter**: [@PythonBiella](https://twitter.com/pythonbiella) *(link da aggiornare)*
- 📧 **Email**: info@pythonbiellagroup.it *(email da verificare)*

---

## 📜 Licenza

Questo progetto è distribuito sotto licenza **MIT** - vedi il file [LICENSE](LICENSE) per dettagli.

---

## 🙏 Ringraziamenti

- **Daniel Pope** - Creatore di PyGame Zero
- **Python Biella Group** - Community e supporto
- **Tutti i contributori** - Grazie per rendere questo progetto migliore!

---

## ⭐ Ti Piace Questo Progetto?

Se trovi utile questo repository:
- ⭐ Lascia una **stella** su GitHub
- 🔄 Condividi con amici e studenti
- 🐛 Segnala bug o suggerisci miglioramenti
- 💻 Contribuisci con il tuo codice!

---

<div align="center">

**Fatto con ❤️ da [Python Biella Group](https://github.com/PythonBiellaGroup)**

*"Il miglior modo per imparare è creare qualcosa di divertente!"*

</div>
# Tony alla ricerca... della musica 🎵

Un gioco educativo musicale sviluppato con Pygame Zero dove il giovane Tony deve raccogliere note musicali per diventare un vero musicista!

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Pygame Zero](https://img.shields.io/badge/pygame--zero-1.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📖 Descrizione

In questo gioco didattico, controlli Tony che deve raccogliere quante più note musicali possibile entro 30 secondi. Ogni nota raccolta riproduce un suono della scala musicale (do, re, mi, fa, sol, la, si).

## ✨ Caratteristiche

- 🎮 Controlli semplici e intuitivi con le frecce direzionali
- 🎵 Suoni musicali realistici per ogni nota raccolta
- ⏱️ Sistema a tempo con 30 secondi di gioco
- 🎨 Grafica colorata e accattivante per bambini
- 🔄 Possibilità di rigiocare premendo SPAZIO

## 🎮 Come giocare

1. **Obiettivo**: Raccogli almeno 20 note musicali entro 30 secondi
2. **Controlli**:
   - ⬅️ Freccia SINISTRA: muovi Tony a sinistra
   - ➡️ Freccia DESTRA: muovi Tony a destra
   - ⬆️ Freccia SU: muovi Tony in alto
   - ⬇️ Freccia GIÙ: muovi Tony in basso
   - ␣ SPAZIO: ricomincia il gioco (dopo il game over)

3. **Vittoria**: Supera il punteggio di 20 note per vedere Tony festeggiare!

## 🚀 Installazione

### Requisiti

- Python 3.7 o superiore
- Pygame Zero

## 📁 Struttura del progetto

```
/
│
├── tonygame.py          # File principale del gioco
│
├── images/                 # Cartella delle immagini
│   ├── tony.png           # Sprite di Tony (normale)
│   ├── tony2.png          # Sprite di Tony (felice)
│   ├── nota_musicale.png  # Sprite della nota musicale
│   ├── sfondo_bn.png      # Sfondo del gioco
│   └── vittoria.png       # Sfondo vittoria
│
├── sounds/                 # Cartella dei suoni
│   ├── do.wav             # Nota DO
│   ├── re.wav             # Nota RE
│   ├── mi.wav             # Nota MI
│   ├── fa.wav             # Nota FA
│   ├── sol.wav            # Nota SOL
│   ├── la.wav             # Nota LA
│   ├── si.wav             # Nota SI
│   └── last_note.wav      # Musica di vittoria
│
└── README.md              # Questo file
```

## 🎨 Risorse grafiche

Per far funzionare il gioco, assicurati di avere le seguenti immagini nella cartella `images/`:

- **tony.png**: Personaggio principale (dimensioni consigliate: 50x50px)
- **tony2.png**: Personaggio felice per la vittoria
- **nota_musicale.png**: Nota da raccogliere (dimensioni consigliate: 40x40px)
- **sfondo_bn.png**: Sfondo del gioco (800x600px)
- **guitar.png**: Sfondo per schermata vittoria (800x600px)

## 🔊 Risorse audio

Nella cartella `sounds/` dovranno essere presenti:

- **do.wav, re.wav, mi.wav, fa.wav, sol.wav, la.wav, si.wav**: Note musicali
- **last_note.wav**: Musica celebrativa per la vittoria

## 🛠️ Personalizzazione

Puoi facilmente modificare i parametri del gioco nel codice:

```python
DURATA_GIOCO = 30          # Cambia la durata (in secondi)
VITTORIA_PUNTEGGIO = 20    # Modifica il punteggio necessario per vincere
WIDTH = 800                # Larghezza della finestra
HEIGHT = 600               # Altezza della finestra
```

## 🐛 Risoluzione problemi

### Il gioco non parte
- Verifica di aver installato Pygame Zero: `pip install pgzero`
- Controlla di avere Python 3.7 o superiore: `python --version`

### Mancano le immagini o i suoni
- Assicurati che le cartelle `images/` e `sounds/` siano nella stessa directory del file `.py`
- Verifica che i nomi dei file corrispondano esattamente a quelli specificati nel codice

### Il gioco è troppo veloce/lento
- Modifica i valori di movimento in `update()`:
```python
tony.x -= 5  # Cambia il 5 con un numero più alto (più veloce) o più basso (più lento)
```

## 🤝 Contribuire

I contributi sono benvenuti! Sentiti libero di:

1. Fare un fork del progetto
2. Creare un branch per la tua feature (`git checkout -b feature/NuovaFeature`)
3. Committare le modifiche (`git commit -m 'Aggiungi NuovaFeature'`)
4. Pushare sul branch (`git push origin feature/NuovaFeature`)
5. Aprire una Pull Request

## 📝 Idee per miglioramenti futuri

- [ ] Aggiungere livelli di difficoltà (facile, medio, difficile)
- [ ] Implementare un sistema di vite
- [ ] Creare power-up speciali
- [ ] Aggiungere ostacoli da evitare
- [ ] Includere una classifica dei migliori punteggi
- [ ] Aggiungere animazioni per Tony
- [ ] Creare più brani musicali completi

## 👨‍💻 Autore

Creato con ❤️ per insegnare Python attraverso il gioco

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## 🙏 Ringraziamenti

- Pygame Zero per il fantastico framework
- La comunità Python per il supporto

---

**Buon divertimento e buona musica! 🎵🎮**

Se il gioco ti piace, lascia una ⭐ su GitHub!

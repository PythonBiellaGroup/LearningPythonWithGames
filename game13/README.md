# 🎮 Cyber Quiz - Sistema di Quiz Interattivo con Analisi Dati

Un sistema completo per la creazione, esecuzione e analisi di quiz educativi.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyGame Zero](https://img.shields.io/badge/PyGame_Zero-1.2%2B-green)
![Polars](https://img.shields.io/badge/Polars-0.19%2B-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

---

## 📚 Indice

- [Panoramica](#-panoramica)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Prerequisiti](#-prerequisiti)
- [Installazione](#-installazione)
- [Guida Didattica](#-guida-didattica)
- [FAQ](#-faq)

---

## 🎯 Panoramica

**Cyber Quiz** è un sistema educativo completo che permette di:

1. **Creare quiz interattivi** con domande a scelta multipla
2. **Raccogliere risposte** degli studenti con precisione al millisecondo
3. **Aggregare dati** da più sessioni di quiz
4. **Visualizzare insights** tramite dashboard interattiva

### Obiettivi Didattici

- Apprendere la gestione di file CSV con Python
- Comprendere il ciclo di vita dei dati (input → elaborazione → output)
- Utilizzare librerie moderne (Polars, Streamlit)
- Sviluppare capacità di analisi dati

---

## 📁 Struttura del Progetto

```
cyber-quiz/
│
├── quiz.py                      # Gioco quiz interattivo (PyGame Zero)
├── aggregatore_csv.py           # Script per aggregare risposte studenti
├── dashboard_quiz.py            # Dashboard Streamlit per analisi
│
├── Domande-Biella/              # Set domande su Biella
│   ├── domande.csv
│   └── risposte.csv
│
├── Domande-Python/              # Set domande su Python
│   ├── domande.csv
│   └── risposte.csv
│
├── risposte_studenti/           # Directory per risposte degli studenti
│   ├── alice_risposte.csv
│   ├── bob_risposte.csv
│   └── ...
│
├── risposte_tutti.csv           # File aggregato (generato)
│
└── README.md                    # Questo file
```

---

## 🔧 Prerequisiti

### Software Necessario

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Editor di testo** (VS Code, PyCharm, Thonny o anche Notepad++)

### Librerie Python

```bash
pip install pgzero polars streamlit
```

---

## 📦 Installazione

```bash
# Installa le dipendenze
pip install pgzero polars streamlit
```

---

## 🎓 Guida Didattica

Il progetto è diviso in **3 fasi** didattiche:

---

## 📖 FASE 1: Quiz Interattivo (Lezione 1)

### Obiettivo
Gli studenti giocano al quiz e imparano come vengono salvati i dati.

### Passi

#### 1. Preparazione
```bash
# Copia un set di domande nella directory principale
cp Domande-Biella/domande.csv .
cp Domande-Biella/risposte.csv .
```

#### 2. Esecuzione del Quiz
```bash
python quiz.py
```

#### 3. Come Giocare
1. **Inserisci il tuo nome** (es. "alice")
2. **Premi ENTER** per iniziare
3. **Clicca sulla risposta** che ritieni corretta
4. Il quiz continua fino all'ultima domanda
5. Alla fine, premi **SPAZIO** per far giocare un altro studente

#### 4. Risultato
Viene creato un file: `alice_risposte.csv` con:
- Nome studente
- ID domanda
- Risposta fornita (1-4)
- Tempo di risposta (in millisecondi)

### Esempio Output CSV
```csv
nome_utente,id_domanda,numero_risposta_fornita,tempo_risposta
alice,1,2,3250
alice,2,3,1890
alice,3,1,5420
```

### 💡 Concetti Didattici
- **Lettura CSV**: Come caricare domande da file
- **Scrittura CSV**: Come salvare risposte
- **Gestione del tempo**: Misurazione in millisecondi
- **Randomizzazione**: Le domande appaiono in ordine casuale

---

## 📖 FASE 2: Aggregazione Dati (Lezione 2)

### Obiettivo
Raccogliere tutte le risposte degli studenti in un unico file.

### Passi

#### 1. Raccolta Risposte
Dopo che tutti gli studenti hanno giocato, sposta i loro file CSV:

```bash
# Crea la directory
mkdir risposte_studenti

# Sposta tutti i file risposte
mv alice_risposte.csv risposte_studenti/
mv bob_risposte.csv risposte_studenti/
mv charlie_risposte.csv risposte_studenti/
```

#### 2. Aggregazione
```bash
python aggregatore_csv.py
```

#### 3. Risultato
Viene creato `risposte_tutti.csv` che contiene TUTTE le risposte.

### 💡 Concetti Didattici
- **Loop sui file**: Iterare su più file
- **Concatenazione DataFrame**: Unire dati da fonti multiple
- **Gestione directory**: Lavorare con percorsi e cartelle

---

## 📖 FASE 3: Dashboard e Analisi (Lezione 3)

### Obiettivo
Visualizzare statistiche e insights tramite dashboard interattiva.

### Passi

#### 1. Verifica File
Assicurati che questi file siano nella stessa cartella:
```bash
ls -la *.csv
# Dovresti vedere:
# - domande.csv
# - risposte.csv
# - risposte_tutti.csv
```

#### 2. Esecuzione Dashboard
```bash
streamlit run dashboard_quiz.py
```

#### 3. Visualizzazione
Il browser si aprirà automaticamente su `http://localhost:8501`

### 📊 Sezioni della Dashboard

1. **Statistiche Generali**: Numero studenti, domande, risposte
2. **Analisi Correttezza**: Percentuale risposte corrette globale
3. **Classifica Studenti**: Tabella ordinata per punteggio
4. **Difficoltà Domande**: Quali domande erano più difficili?
5. **Grafico Prestazioni**: Visualizzazione grafica dei risultati
6. **Tempo Medio**: Analisi dei tempi di risposta

### 💡 Concetti Didattici
- **Join di DataFrame**: Unire dati da tabelle diverse
- **Aggregazioni**: Calcolare medie, somme, conteggi
- **Visualizzazioni**: Grafici e tabelle interattive

---

## 📄 Struttura File CSV

### domande.csv
```csv
id_domanda,domanda,risposta_1,risposta_2,risposta_3,risposta_4
1,Qual è la maschera tipica...,Arlecchino,La Bela Majin,Babi,Gianduia
2,In che anno Biella fu fondata?,1245,1379,1160,1472
```

### risposte.csv
```csv
id_domanda,numero_risposta_corretta
1,2
2,2
3,1
```

### alice_risposte.csv (output quiz)
```csv
nome_utente,id_domanda,numero_risposta_fornita,tempo_risposta
alice,1,2,3250
alice,2,3,1890
```

---

## 🎨 Personalizzazione

### Creare Nuove Domande

1. Crea `domande.csv` con le colonne: `id_domanda,domanda,risposta_1,risposta_2,risposta_3,risposta_4`
2. Crea `risposte.csv` con: `id_domanda,numero_risposta_corretta`
3. Usa nel quiz!

### Modificare il Tempo

In `quiz.py`, cambia:
```python
TEMPO_DOMANDA = 15  # secondi per domanda
```

---

## ❓ FAQ

### Il quiz non parte

**Soluzione**:
```bash
pip install pgzero
```

### Le risposte non si vedono

Verifica che `domande.csv` abbia le colonne con underscore: `risposta_1`, `risposta_2`, etc.

### La dashboard dà errore

Assicurati che:
1. `domande.csv` abbia la colonna `id_domanda`
2. `risposte.csv` abbia la colonna `id_domanda`
3. `risposte_tutti.csv` esista

---

## 🔄 Workflow Tipico in Classe

```
1. PREPARAZIONE (5 min)
   └── Distribuzione file domande

2. QUIZ (15 min)
   └── Ogni studente gioca

3. RACCOLTA (5 min)
   └── Raccogli file CSV in risposte_studenti/

4. AGGREGAZIONE (2 min)
   └── python aggregatore_csv.py

5. ANALISI (20 min)
   └── streamlit run dashboard_quiz.py
   └── Discussione risultati

6. RIFLESSIONE (10 min)
   └── Cosa abbiamo imparato?
```

---

## 📚 Risorse

- **Polars**: https://pola-rs.github.io/polars/
- **Streamlit**: https://docs.streamlit.io/
- **PyGame Zero**: https://pygame-zero.readthedocs.io/

---

## 📝 Licenza

MIT License - Materiale didattico per Liceo Scientifico

---

<div align="center">

**Fatto con ❤️ da [Python Biella Group](https://github.com/PythonBiellaGroup)**

*"Il miglior modo per imparare è creare qualcosa di divertente!"*

</div>
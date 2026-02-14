# dashboard_quiz.py
import streamlit as st
import polars as pl

# ========================================
# CONFIGURAZIONE PAGINA
# ========================================
st.set_page_config(
    page_title="Risultati Quiz Python",
    page_icon="🎮",
    layout="wide"
)

# ========================================
# TITOLO PRINCIPALE
# ========================================
st.title("🎮 Dashboard Risultati Quiz Python")
st.write("Analisi delle risposte degli studenti")

# ========================================
# CARICAMENTO DATI
# ========================================
# Carica i 3 CSV
df_domande = pl.read_csv("domande.csv")
df_risposte = pl.read_csv("risposte.csv")
df_studenti = pl.read_csv("risposte_tutti.csv")

# ========================================
# SEZIONE 1: STATISTICHE GENERALI
# ========================================
st.header("📊 Statistiche Generali")

# Calcola metriche base
num_studenti = df_studenti.select("nome_utente").unique().height
num_domande = df_domande.height
totale_risposte = df_studenti.height

# Mostra le metriche in colonne
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👥 Studenti partecipanti", num_studenti)
with col2:
    st.metric("❓ Domande totali", num_domande)
with col3:
    st.metric("✍️ Risposte date", totale_risposte)

# ========================================
# SEZIONE 2: ANALISI CORRETTEZZA
# ========================================
st.header("✅ Analisi Correttezza Risposte")

# Join per verificare le risposte corrette
df_con_corrette = df_studenti.join(
    df_risposte,
    on="id_domanda",
    how="left"
)

# Aggiungi colonna che indica se la risposta è corretta
df_con_corrette = df_con_corrette.with_columns(
    (pl.col("numero_risposta_fornita") == pl.col("numero_risposta_corretta"))
    .alias("corretta")
)

# Calcola percentuale risposte corrette
risposte_corrette = df_con_corrette.filter(pl.col("corretta") == True).height
percentuale_corrette = (risposte_corrette / totale_risposte * 100) if totale_risposte > 0 else 0

st.metric(
    "Percentuale risposte corrette", 
    f"{percentuale_corrette:.1f}%"
)

# ========================================
# SEZIONE 3: CLASSIFICA STUDENTI
# ========================================
st.header("🏆 Classifica Studenti")

# Calcola punteggio per studente
classifica = (
    df_con_corrette
    .group_by("nome_utente")
    .agg([
        pl.col("corretta").sum().alias("risposte_corrette"),
        pl.col("id_domanda").count().alias("domande_risposte"),
        pl.col("tempo_risposta").mean().alias("tempo_medio")
    ])
    .sort("risposte_corrette", descending=True)
)

# Mostra la classifica
st.dataframe(
    classifica,
    width='stretch',
    hide_index=True
)

# ========================================
# SEZIONE 4: DIFFICOLTÀ DOMANDE
# ========================================
st.header("📈 Difficoltà Domande")

# Calcola percentuale di successo per domanda
difficolta = (
    df_con_corrette
    .group_by("id_domanda")
    .agg([
        pl.col("corretta").sum().alias("risposte_corrette"),
        pl.col("corretta").count().alias("totale_risposte")
    ])
    .with_columns(
        (pl.col("risposte_corrette") / pl.col("totale_risposte") * 100)
        .alias("percentuale_corrette")
    )
    .sort("percentuale_corrette")
)

# Join con il testo delle domande
difficolta = difficolta.join(
    df_domande.select(["id_domanda", "domanda"]),
    on="id_domanda",
    how="left"
)

# Mostra tabella difficoltà
st.dataframe(
    difficolta.select(["id_domanda", "domanda", "percentuale_corrette"]),
    width='stretch',
    hide_index=True
)

# ========================================
# SEZIONE 5: GRAFICO A BARRE
# ========================================
st.header("📊 Grafico Prestazioni")

# Prepara dati per il grafico
dati_grafico = classifica.select(["nome_utente", "risposte_corrette"])

# Crea grafico a barre
st.bar_chart(
    dati_grafico,
    x="nome_utente",
    y="risposte_corrette",
    width='stretch'
)

# ========================================
# SEZIONE 6: TEMPO MEDIO DI RISPOSTA
# ========================================
st.header("⏱️ Tempo Medio di Risposta")

tempo_medio_globale = df_studenti.select(pl.col("tempo_risposta").mean())[0, 0]
st.metric("Tempo medio per risposta", f"{tempo_medio_globale:.0f} ms")

# Grafico tempo per domanda
tempo_per_domanda = (
    df_studenti
    .group_by("id_domanda")
    .agg(pl.col("tempo_risposta").mean().alias("tempo_medio"))
    .sort("id_domanda")
)

st.bar_chart(
    tempo_per_domanda,
    x="id_domanda",
    y="tempo_medio",
    width='stretch'
)
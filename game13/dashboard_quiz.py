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
df_domande = pl.read_csv("domande.csv")
df_risposte = pl.read_csv("risposte.csv")
df_studenti = pl.read_csv("risposte_tutti.csv")

# ========================================
# JOIN E CALCOLO CORRETTEZZA
# ========================================
df_con_corrette = df_studenti.join(
    df_risposte,
    on="id_domanda",
    how="left"
).with_columns(
    (pl.col("numero_risposta_fornita") == pl.col("numero_risposta_corretta"))
    .alias("corretta")
)

# Classifica studenti
classifica = (
    df_con_corrette
    .group_by("nome_utente")
    .agg([
        pl.col("corretta").sum().alias("risposte_corrette"),
        pl.col("id_domanda").count().alias("domande_risposte"),
        pl.col("tempo_risposta").mean().alias("tempo_medio")
    ])
    .with_columns(
        (pl.col("risposte_corrette") / pl.col("domande_risposte") * 100)
        .round(1)
        .alias("percentuale_corrette")
    )
    .sort(["risposte_corrette", "tempo_medio"], descending=[True, False])
)

# ========================================
# SEZIONE 1: STATISTICHE GENERALI
# ========================================
st.header("📊 Statistiche Generali")

num_studenti = df_studenti.select("nome_utente").unique().height
num_domande = df_domande.height
totale_risposte = df_studenti.height
risposte_corrette = df_con_corrette.filter(pl.col("corretta") == True).height
percentuale_corrette = (risposte_corrette / totale_risposte * 100) if totale_risposte > 0 else 0
tempo_medio_globale = df_studenti.select(pl.col("tempo_risposta").mean())[0, 0]

# Studente migliore e peggiore
migliore = classifica.row(0, named=True)
peggiore = classifica.row(-1, named=True)

# Domanda più difficile (minor percentuale di successo)
difficolta = (
    df_con_corrette
    .group_by("id_domanda")
    .agg([
        pl.col("corretta").sum().alias("risposte_corrette"),
        pl.col("corretta").count().alias("totale_risposte")
    ])
    .with_columns(
        (pl.col("risposte_corrette") / pl.col("totale_risposte") * 100)
        .round(1)
        .alias("percentuale_corrette")
    )
    .sort("percentuale_corrette")
)
id_domanda_difficile = difficolta.row(0, named=True)["id_domanda"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👥 Studenti partecipanti", num_studenti)
with col2:
    st.metric("❓ Domande totali", num_domande)
with col3:
    st.metric("✍️ Risposte date", totale_risposte)

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("✅ Risposte corrette (media classe)", f"{percentuale_corrette:.1f}%")
with col5:
    st.metric("⏱️ Tempo medio per risposta", f"{tempo_medio_globale:.0f} ms")
with col6:
    st.metric("❓ Domanda più difficile", f"Domanda #{id_domanda_difficile}")

col7, col8 = st.columns(2)
with col7:
    st.metric(
        "🥇 Studente migliore",
        migliore["nome_utente"],
        f"{migliore['risposte_corrette']} risposte corrette"
    )
with col8:
    st.metric(
        "📚 Da migliorare",
        peggiore["nome_utente"],
        f"{peggiore['risposte_corrette']} risposte corrette",
        delta_color="inverse"
    )

# ========================================
# SEZIONE 2: CLASSIFICA STUDENTI (grafico)
# ========================================
st.header("🏆 Classifica Studenti")

# Classifica con barre progress: ordine garantito, nessuna libreria extra
max_corrette = classifica["risposte_corrette"].max()

for i, row in enumerate(classifica.iter_rows(named=True)):
    st.write(f"{i+1}° **{row['nome_utente']}** — {row['risposte_corrette']} risposte corrette")
    st.progress(int(row["risposte_corrette"]) / int(max_corrette))

# Tabella dettagliata sotto il grafico
with st.expander("📋 Vedi tabella dettagliata"):
    st.dataframe(
        classifica.select([
            "nome_utente",
            "risposte_corrette",
            "domande_risposte",
            "percentuale_corrette",
            "tempo_medio"
        ]),
        width="stretch",
        hide_index=True,
        column_config={
            "nome_utente": "Studente",
            "risposte_corrette": "✅ Corrette",
            "domande_risposte": "❓ Risposte",
            "percentuale_corrette": st.column_config.NumberColumn("% Corrette", format="%.1f%%"),
            "tempo_medio": st.column_config.NumberColumn("⏱️ Tempo medio (ms)", format="%.0f")
        }
    )

# ========================================
# SEZIONE 3: DIFFICOLTÀ DOMANDE
# ========================================
st.header("📈 Difficoltà Domande")

difficolta_con_testo = difficolta.join(
    df_domande.select(["id_domanda", "domanda"]),
    on="id_domanda",
    how="left"
)

st.dataframe(
    difficolta_con_testo.select(["id_domanda", "domanda", "percentuale_corrette"]),
    width="stretch",
    hide_index=True,
    column_config={
        "id_domanda": "ID",
        "domanda": "Domanda",
        "percentuale_corrette": st.column_config.ProgressColumn(
            "% Risposte Corrette",
            format="%.1f%%",
            min_value=0,
            max_value=100
        )
    }
)

# ========================================
# SEZIONE 4: TEMPO DI RISPOSTA PER DOMANDA
# ========================================
st.header("⏱️ Tempo di Risposta per Domanda")

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
    width="stretch"
)

# ========================================
# SEZIONE 5: DOMANDE E RISPOSTE CORRETTE
# ========================================
with st.expander("📖 Visualizza domande e risposte corrette"):
    domande_con_risposta = (
        df_domande.join(df_risposte, on="id_domanda", how="left")
        .sort("id_domanda")
    )
    for row in domande_con_risposta.iter_rows(named=True):
        numero = row["numero_risposta_corretta"]
        risposta_corretta = row[f"risposta_{numero}"]
        st.markdown(f"**#{row['id_domanda']} — {row['domanda']}**")
        st.success(f"✅ {risposta_corretta}")
        st.divider()

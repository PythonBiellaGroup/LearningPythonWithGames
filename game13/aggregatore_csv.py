# merge_risposte.py
import polars as pl
from pathlib import Path

# Leggi tutti i file CSV degli studenti nella cartella
cartella_risposte = Path("risposte_studenti")
tutti_i_file = list(cartella_risposte.glob("*.csv"))

# Lista per raccogliere tutti i dataframe
lista_df = []

for file in tutti_i_file:
    print(f"Aggregando {file} ...")
    df = pl.read_csv(file)
    lista_df.append(df)

# Unisci tutti i dataframe
df_completo = pl.concat(lista_df)

# Salva il risultato
df_completo.write_csv("risposte_tutti.csv")
print(f"Aggregate {len(tutti_i_file)} risposte di studenti")
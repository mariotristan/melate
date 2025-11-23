import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuración
DATA_FILE = "MelateRetro.csv"
REPORT_FILE = "ANALISIS_RETRO.md"
HEATMAP_PNG = "retro_heatmap.png"
FREQ_PNG = "retro_frecuencias.png"

# Cargar datos
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"No se encontró el archivo {DATA_FILE}. Descárgalo desde la página oficial.")

df = pd.read_csv(DATA_FILE)

# Detectar columnas de números
# Adaptación para Melate Retro: columnas F1-F7
num_cols = [col for col in df.columns if col.startswith("F") and col[1:].isdigit()]
if len(num_cols) < 6:
    raise ValueError(f"No se detectaron suficientes columnas de números (F1-F7). Columnas detectadas: {num_cols}")

# Normalizar y limpiar
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=num_cols)

# Análisis de frecuencias
all_numbers = np.concatenate([df[col].values for col in num_cols])
counts = pd.Series(all_numbers).value_counts().sort_index()

n_sorteos = len(df)
numeros_posibles = sorted(counts.index)
N = len(numeros_posibles)

frecuencia_esperada = (n_sorteos * len(num_cols)) / N

# Desviación porcentual
desviacion = ((counts - frecuencia_esperada) / frecuencia_esperada) * 100

# Clasificación de calor
calor = pd.cut(desviacion,
    bins=[-np.inf, -10, -5, 5, 10, np.inf],
    labels=["🧊 Muy frío", "❄️ Frío", "➡️ Normal", "🌡️ Caliente", "🔥 Muy caliente"]
)

# Visualización de frecuencias
plt.figure(figsize=(12,6))
plt.bar(numeros_posibles, counts[numeros_posibles], color='royalblue')
plt.xlabel("Número")
plt.ylabel("Frecuencia absoluta")
plt.title("Frecuencia de aparición - Melate Retro")
plt.tight_layout()
plt.savefig(FREQ_PNG)
plt.close()

# Visualización de calor
colors = calor.map({
    "🧊 Muy frío": "#00bfff",
    "❄️ Frío": "#87ceeb",
    "➡️ Normal": "#cccccc",
    "🌡️ Caliente": "#ffb347",
    "🔥 Muy caliente": "#ff4500"
})
plt.figure(figsize=(12,6))
plt.bar(numeros_posibles, desviacion[numeros_posibles], color=colors)
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.xlabel("Número")
plt.ylabel("Desviación porcentual (%)")
plt.title("Desviación y calor - Melate Retro")
plt.tight_layout()
plt.savefig(HEATMAP_PNG)
plt.close()

# Generar reporte markdown
fecha = datetime.now().strftime('%Y-%m-%d')
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# 📊 Análisis Estadístico Melate Retro\n\n")
    f.write(f"**Fecha de análisis:** {fecha}\n\n")
    f.write(f"- Sorteos analizados: {n_sorteos}\n")
    f.write(f"- Números posibles: {N}\n\n")
    f.write(f"## Frecuencia absoluta por número\n\n")
    f.write(f"![Frecuencias]({FREQ_PNG})\n\n")
    f.write(f"## Desviación porcentual y calor\n\n")
    f.write(f"![Calor]({HEATMAP_PNG})\n\n")
    f.write(f"| Número | Frecuencia | Desviación (%) | Calor |\n")
    f.write(f"|--------|------------|---------------|-------|\n")
    for num in numeros_posibles:
        f.write(f"| {num} | {counts[num]} | {desviacion[num]:.2f} | {calor[num]} |")
        f.write("\n")
    f.write("\n---\n")
    f.write("## Recomendaciones de estrategia\n\n")
    f.write("- Considera los números 'calientes' y 'muy calientes' si buscas explotar posibles sesgos mecánicos.\n")
    f.write("- Alterna con números 'fríos' para diversificar y cubrir regresión a la media.\n")
    f.write("- Recuerda que la lotería es un juego de azar y no existe garantía de éxito.\n")
    f.write("\n> Consulta METODOLOGIA.md para fundamentos teóricos y referencias.\n")

print(f"Análisis completado. Revisa {REPORT_FILE} y los gráficos PNG generados.")

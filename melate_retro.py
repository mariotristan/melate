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

# Estrategias y recomendaciones avanzadas (similar a melate.py)
today = datetime.now()
seed = int(today.strftime("%Y%m%d"))
np.random.seed(seed)

top_numbers = [int(num) for num in counts.sort_values(ascending=False).index[:30]]
cold_numbers = [int(num) for num in counts.sort_values().index[:20]]
all_numbers_list = list(numeros_posibles)

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(f"# 📊 Análisis Estadístico Melate Retro\n\n")
    f.write(f"**Fecha de análisis:** {today.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"- Sorteos analizados: {n_sorteos}\n")
    f.write(f"- Números posibles: {N}\n\n")
    f.write(f"## Frecuencia absoluta por número\n\n")
    f.write(f"![Frecuencias]({FREQ_PNG})\n\n")
    f.write(f"## Desviación porcentual y calor\n\n")
    f.write(f"![Calor]({HEATMAP_PNG})\n\n")
    f.write(f"| Número | Frecuencia | Desviación (%) | Calor |\n")
    f.write(f"|--------|------------|---------------|-------|\n")
    for num in numeros_posibles:
        f.write(f"| {num} | {counts[num]} | {desviacion[num]:.2f} | {calor[num]} |\n")
    f.write("\n---\n")

    # Indicador de Calor - Últimos Resultados
    f.write("## 🌡️ Indicador de Calor - Últimos Resultados\n\n")
    f.write("Esta sección compara los números del último sorteo contra las categorías de temperatura (caliente/frío) basadas en su frecuencia histórica.\n\n")
    # Último sorteo
    if len(df) > 0:
        ultimo = df.iloc[0][num_cols].values.astype(int).tolist()
        f.write(f"### 🎰 Melate Retro - Sorteo más reciente\n\n")
        f.write("| Número | Frecuencia | Desviación (%) | Calor |\n")
        f.write("|:------:|:----------:|:--------------:|:------:|\n")
        for num in ultimo:
            f.write(f"| **{num}** | {counts[num]} | {desviacion[num]:.2f} | {calor[num]} |\n")
        # Resumen de distribución
        muy_calientes = sum(1 for num in ultimo if calor[num] == "🔥 Muy caliente")
        calientes = sum(1 for num in ultimo if calor[num] == "🌡️ Caliente")
        normales = sum(1 for num in ultimo if calor[num] == "➡️ Normal")
        frios = sum(1 for num in ultimo if calor[num] == "❄️ Frío")
        muy_frios = sum(1 for num in ultimo if calor[num] == "🧊 Muy frío")
        f.write(f"\n**📊 Distribución de temperatura:**\n")
        f.write(f"- 🔥 Muy calientes: {muy_calientes}\n")
        f.write(f"- 🌡️ Calientes: {calientes}\n")
        f.write(f"- ➡️ Normales: {normales}\n")
        f.write(f"- ❄️ Fríos: {frios}\n")
        f.write(f"- 🧊 Muy fríos: {muy_frios}\n\n")
    else:
        f.write("No se pudo analizar el último sorteo.\n\n")
    f.write("---\n")

    f.write("## 🎲 Recomendaciones del Día\n\n")
    f.write("### 📊 Cinco Estrategias Diferentes\n\n")
    f.write("Todas las recomendaciones usan la fecha actual como semilla para generar combinaciones consistentes y reproducibles.\n\n")

    # Estrategia 1: Híbrida
    f.write("#### 📋 Estrategia 1: HÍBRIDA (4 calientes + 2 aleatorios)\n\n")
    f.write("Combina números de alta frecuencia con selección aleatoria para diversificar el riesgo.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    np.random.seed(seed)
    for i in range(1, 6):
        selected = list(np.random.choice(top_numbers, 4, replace=False))
        remaining = [n for n in all_numbers_list if n not in selected]
        selected.extend(list(np.random.choice(remaining, 2, replace=False)))
        selected.sort()
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")

    # Estrategia 2: Conservadora
    f.write("#### 🔥 Estrategia 2: CONSERVADORA (solo números calientes)\n\n")
    f.write("Apuesta exclusivamente por los números más frecuentes históricamente.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    np.random.seed(seed + 1000)
    for i in range(1, 6):
        selected = list(np.random.choice(top_numbers[:20], 6, replace=False))
        selected.sort()
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")

    # Estrategia 3: Contrarian
    f.write("#### 🧊 Estrategia 3: CONTRARIAN (números fríos)\n\n")
    f.write("Apuesta a la reversión: números que han salido menos podrían 'compensar' estadísticamente.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    np.random.seed(seed + 2000)
    for i in range(1, 6):
        selected = list(np.random.choice(cold_numbers[:15], 6, replace=False))
        selected.sort()
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")

    # Estrategia 4: Balanceada
    f.write("#### ⚖️ Estrategia 4: BALANCEADA (3 calientes + 3 fríos)\n\n")
    f.write("Equilibrio perfecto entre números frecuentes y poco frecuentes.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    np.random.seed(seed + 3000)
    for i in range(1, 6):
        hot = list(np.random.choice(top_numbers[:15], 3, replace=False))
        cold = list(np.random.choice(cold_numbers[:12], 3, replace=False))
        selected = sorted(hot + cold)
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")

    # Estrategia 5: Serendipity
    f.write("#### ✨ Estrategia 5: SERENDIPITY (mezcla de todas)\n\n")
    f.write("Cada combinación usa aleatoriamente una de las 4 estrategias anteriores. ¡Deja que el destino elija!\n\n")
    f.write("| # | Estrategia | Combinación |\n")
    f.write("|:-:|:----------:|:-----------|\n")
    np.random.seed(seed + 4000)
    for i in range(1, 6):
        strategy_choice = np.random.randint(1, 5)
        if strategy_choice == 1:  # Híbrida
            selected = list(np.random.choice(top_numbers, 4, replace=False))
            remaining = [n for n in all_numbers_list if n not in selected]
            selected.extend(list(np.random.choice(remaining, 2, replace=False)))
        elif strategy_choice == 2:  # Conservadora
            selected = list(np.random.choice(top_numbers[:20], 6, replace=False))
        elif strategy_choice == 3:  # Contrarian
            selected = list(np.random.choice(cold_numbers[:15], 6, replace=False))
        else:  # Balanceada
            hot = list(np.random.choice(top_numbers[:15], 3, replace=False))
            cold = list(np.random.choice(cold_numbers[:12], 3, replace=False))
            selected = hot + cold
        selected.sort()
        strategy_name = ["📋 Híbrida", "🔥 Conservadora", "🧊 Contrarian", "⚖️ Balanceada"][strategy_choice - 1]
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | {strategy_name} | **{nums_str}** |\n")
    f.write("\n---\n")

    f.write("## ⚠️ Disclaimer\n\n")
    f.write("> Este análisis es con fines educativos y estadísticos únicamente. ")
    f.write("Los sorteos de lotería son eventos aleatorios y los resultados pasados ")
    f.write("NO garantizan resultados futuros. Juega responsablemente.\n\n")
    f.write("---\n\n")
    f.write(f"*Generado automáticamente el {today.strftime('%d/%m/%Y a las %H:%M:%S')}*\n")

print(f"Análisis completado. Revisa {REPORT_FILE} y los gráficos PNG generados.")

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Configuración
TRIS_URL = "https://www.loterianacional.gob.mx/Home/Historicos?ARHP=VAByAGkAcwA="
CSV_FILE = "Tris.csv"
REPORT_FILE = "ANALISIS_TRIS.md"
GRAPH_FILE = "tris_frecuencias.png"
    # ...la versión compacta y funcional ya está presente arriba...
# Descarga de datos
# NOTA: El sitio requiere scraping especial, aquí se asume que el CSV está disponible o se descarga manualmente.
def descargar_tris_csv():
    # No hace nada, el archivo ya está presente
    pass

def cargar_datos():
    return pd.read_csv(CSV_FILE, encoding="utf-8")

def analizar_tris(df):
    # Usar columnas R1-R5 como números del sorteo
    num_cols = [col for col in df.columns if col.startswith("R") and col[1:].isdigit()]
    # Frecuencia de cada número (0-9)
    todos = df[num_cols].values.flatten()
    counts = pd.Series(todos).value_counts().sort_index()
    total = len(todos)
    freq = counts / total * 100
    # Desviación respecto a la media
    media = total / 10
    desviacion = (counts - media) / media * 100
    # Calor
    calor = pd.cut(desviacion, [-np.inf, -20, -10, 10, 20, np.inf], labels=["🧊 Muy frío", "❄️ Frío", "➡️ Normal", "🌡️ Caliente", "🔥 Muy caliente"])
    return counts, freq, desviacion, calor

def graficar_frecuencias(counts):
    plt.figure(figsize=(8,4))
    counts.plot(kind="bar", color="royalblue")
    plt.title("Frecuencia de números en Tris")
    plt.xlabel("Número")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(GRAPH_FILE)
    plt.close()


def generar_reporte(df, counts, freq, desviacion, calor):
    import random
    today = datetime.datetime.now()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    calientes = [num for num in range(10) if calor.get(num) in ["🔥 Muy caliente", "🌡️ Caliente"]]
    frios = [num for num in range(10) if calor.get(num) in ["🧊 Muy frío", "❄️ Frío"]]
    normales = [num for num in range(10) if calor.get(num) == "➡️ Normal"]
    todos = list(range(10))

    estrategias = []
    # Híbrida: 3 calientes + 2 aleatorios (no calientes)
    def hibrida():
        c = random.sample(calientes, min(3, len(calientes)))
        restantes = [n for n in todos if n not in c]
        a = random.sample(restantes, 5 - len(c))
        return sorted(c + a)
    estrategias.append(("Híbrida (3 calientes + 2 aleatorios)", hibrida))

    # Conservadora: solo calientes, completar con normales si faltan
    def conservadora():
        c = random.sample(calientes, min(5, len(calientes)))
        if len(c) < 5:
            extra = random.sample(normales, 5 - len(c))
            c += extra
        return sorted(c)
    estrategias.append(("Conservadora (solo calientes)", conservadora))

    # Contrarian: solo fríos, completar con normales si faltan
    def contrarian():
        f = random.sample(frios, min(5, len(frios)))
        if len(f) < 5:
            extra = random.sample(normales, 5 - len(f))
            f += extra
        return sorted(f)
    estrategias.append(("Contrarian (solo fríos)", contrarian))

    # Balanceada: 2 calientes + 2 fríos + 1 normal, completar con aleatorios si faltan
    def balanceada():
        c = random.sample(calientes, min(2, len(calientes)))
        f_ = random.sample(frios, min(2, len(frios)))
        n = random.sample(normales, 1 if len(normales) > 0 else 0)
        comb = c + f_ + n
        if len(comb) < 5:
            extra = random.sample([x for x in todos if x not in comb], 5 - len(comb))
            comb += extra
        return sorted(comb)
    estrategias.append(("Balanceada (2 calientes + 2 fríos + 1 normal)", balanceada))

    # Serendipity: elige una de las anteriores aleatoriamente
    def serendipity():
        strategy = random.choice([0, 1, 2, 3])
        return estrategias[strategy][1]()
    estrategias.append(("Serendipity (mezcla aleatoria)", serendipity))

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# 📊 Análisis Estadístico de Tris\n\n")
        f.write(f" **Fecha de análisis:**  {today.strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"- Sorteos analizados: {len(df)}\n")
        f.write(f"- Números posibles: 10 (0-9)\n\n")
        f.write("---\n\n")
        f.write("**¿Qué es Tris?**\n\n")
        f.write("Tris es el sorteo numérico más accesible de México, donde puedes decidir cuánto quieres ganar según la modalidad que elijas y cuánto desees apostar. Puedes jugar desde $1 peso, seleccionando 1, 2, 3, 4 o 5 dígitos, cada uno de un conjunto diferente de esferas del 0 al 9.\n\n")
        f.write("Las urnas de Tris eligen 5 números al azar para formar una cifra de 5 dígitos. Si tus números coinciden en estricto orden con los del sorteo, ¡puedes ganar muchísimo dinero! Dependiendo de la modalidad, tu oportunidad de ganar más dinero puede aumentar.\n\n")
        f.write("---\n\n")
        f.write("## Tabla de Frecuencias\n\n")
        f.write("| Número | Frecuencia | Porcentaje (%) | Desviación (%) | Calor |\n")
        f.write("|:------:|:----------:|:--------------:|:--------------:|:------:|\n")
        for num in range(10):
            f.write(f"| {num} | {counts.get(num,0)} | {freq.get(num,0):.2f} | {desviacion.get(num,0):.2f} | {calor.get(num,'➡️ Normal')} |\n")
        f.write("\n![Frecuencias](tris_frecuencias.png)\n\n")
        f.write("## 🌡️ Indicador de Calor - Últimos Resultados\n\n")
        num_cols = [col for col in df.columns if col.startswith("R") and col[1:].isdigit()]
        if len(df) > 0:
            ultimo = df.iloc[0][num_cols].values.astype(int).tolist()
            fecha_col = next((col for col in df.columns if 'FECHA' in col.upper()), None)
            fecha_ultimo = str(df.iloc[0][fecha_col]) if fecha_col else "(fecha no disponible)"
            f.write(f"### 🎰 Tris - Sorteo más reciente ({fecha_ultimo})\n\n")
            f.write("| Número | Frecuencia | Desviación (%) | Calor |\n")
            f.write("|:------:|:----------:|:--------------:|:------:|\n")
            for num in ultimo:
                f.write(f"| **{num}** | {counts.get(num,0)} | {desviacion.get(num,0):.2f} | {calor.get(num,'➡️ Normal')} |\n")
            muy_calientes = sum(1 for num in ultimo if calor.get(num) == "🔥 Muy caliente")
            calientes_ = sum(1 for num in ultimo if calor.get(num) == "🌡️ Caliente")
            normales_ = sum(1 for num in ultimo if calor.get(num) == "➡️ Normal")
            frios_ = sum(1 for num in ultimo if calor.get(num) == "❄️ Frío")
            muy_frios = sum(1 for num in ultimo if calor.get(num) == "🧊 Muy frío")
            f.write("\n**📊 Distribución de temperatura:**\n\n")
            f.write(f"- 🔥 Muy calientes: {muy_calientes}\n")
            f.write(f"- 🌡️ Calientes: {calientes_}\n")
            f.write(f"- ➡️ Normales: {normales_}\n")
            f.write(f"- ❄️ Fríos: {frios_}\n")
            f.write(f"- 🧊 Muy fríos: {muy_frios}\n\n")
            f.write("## 🤔 Recomendación de Estrategia según Tendencia de Calor\n\n")
            total = muy_calientes + calientes_ + normales_ + frios_ + muy_frios
            if (muy_calientes + calientes_) >= 3:
                tendencia_text = "El último sorteo tuvo mayoría de números calientes."
                recomendacion_text = "Evita la estrategia conservadora (solo calientes), ya que es probable que los números calientes hayan sido sobreutilizados. Opta por la estrategia balanceada o contrarian (fríos), buscando reversión estadística."
                razonamiento_text = "Cuando los números calientes dominan, la probabilidad de que sigan saliendo disminuye por regresión a la media. Apostar por equilibrio o por fríos puede aprovechar ciclos de reversión."
            elif (muy_frios + frios_) >= 3:
                tendencia_text = "El último sorteo tuvo mayoría de números fríos."
                recomendacion_text = "La estrategia contrarian (fríos) o balanceada tiene más sentido, ya que los números fríos pueden estar en fase de reversión."
                razonamiento_text = "Los números fríos tienden a compensar su baja frecuencia en ciclos largos. Apostar por ellos puede anticipar una reversión estadística."
            elif normales_ >= 3:
                tendencia_text = "El último sorteo fue equilibrado, con mayoría de números normales."
                recomendacion_text = "La estrategia balanceada o híbrida es la más sensata, ya que no hay una tendencia clara."
                razonamiento_text = "Cuando no hay predominio de calientes ni fríos, conviene diversificar y equilibrar el riesgo."
            else:
                tendencia_text = "El último sorteo fue mixto."
                recomendacion_text = "La estrategia balanceada es la más robusta, pero puedes probar también la serendipity para diversificar."
                razonamiento_text = "En escenarios mixtos, el equilibrio y la aleatoriedad controlada suelen ser óptimos."
            f.write(f"**Tendencia observada:** {tendencia_text}\n\n")
            f.write(f"**Recomendación:** {recomendacion_text}\n\n")
            f.write(f"**Razonamiento:** {razonamiento_text}\n\n")
            f.write("---\n\n")
        else:
            f.write("No se pudo analizar el último sorteo.\n\n")
            f.write("---\n\n")
        # Recomendaciones del Día
        f.write("## 🎲 Recomendaciones del Día\n\n")
        f.write(f"_Generadas el {today.strftime('%d/%m/%Y %H:%M')} con semilla aleatoria {seed}_\n\n")
        for idx, (nombre, func) in enumerate(estrategias, 1):
            f.write(f"**Estrategia {idx}: {nombre}**\n\n")
            for i in range(1, 6):
                sel = func()
                f.write(f"- Combinación {i}: {sel}\n")
            f.write("\n")
        f.write("## ⚠️ Disclaimer\n\n")
        f.write("Este análisis es meramente estadístico y no garantiza resultados. Juega responsablemente.\n")


def main():
    descargar_tris_csv()
    df = cargar_datos()
    counts, freq, desviacion, calor = analizar_tris(df)
    graficar_frecuencias(counts)
    generar_reporte(df, counts, freq, desviacion, calor)

if __name__ == "__main__":
    main()

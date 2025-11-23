import pandas as pd
from collections import Counter
from itertools import combinations
import random
from datetime import datetime
import os

# Cargar los tres archivos CSV
melate_df = pd.read_csv("Melate.csv")
revancha_df = pd.read_csv("Revancha.csv")
revanchita_df = pd.read_csv("Revanchita.csv")

# Obtener las fechas de última modificación de los archivos
melate_mtime = datetime.fromtimestamp(os.path.getmtime("Melate.csv"))
revancha_mtime = datetime.fromtimestamp(os.path.getmtime("Revancha.csv"))
revanchita_mtime = datetime.fromtimestamp(os.path.getmtime("Revanchita.csv"))

# Revanchita usa F1-F6, necesitamos renombrar a R1-R6
revanchita_df = revanchita_df.rename(columns={
    'F1': 'R1', 'F2': 'R2', 'F3': 'R3', 
    'F4': 'R4', 'F5': 'R5', 'F6': 'R6'
})

# Combinar todos los dataframes
df = pd.concat([melate_df, revancha_df, revanchita_df], ignore_index=True)

# Columnas de números
cols = ["R1","R2","R3","R4","R5","R6"]

# Obtener últimos resultados de cada sorteo con sus fechas
ultimo_melate = melate_df.iloc[0][cols].values.astype(int).tolist() if len(melate_df) > 0 else []
fecha_melate = melate_df.iloc[0]['FECHA'] if len(melate_df) > 0 else None

ultimo_revancha = revancha_df.iloc[0][cols].values.astype(int).tolist() if len(revancha_df) > 0 else []
fecha_revancha = revancha_df.iloc[0]['FECHA'] if len(revancha_df) > 0 else None

ultimo_revanchita = revanchita_df.iloc[0][cols].values.astype(int).tolist() if len(revanchita_df) > 0 else []
fecha_revanchita = revanchita_df.iloc[0]['FECHA'] if len(revanchita_df) > 0 else None

print(f"\n📊 Total de sorteos analizados: {len(df):,}")
print(f"   • Melate: {len(melate_df):,}")
print(f"   • Revancha: {len(revancha_df):,}")
print(f"   • Revanchita: {len(revanchita_df):,}")


# 1. Frecuencia de cada número
all_numbers = df[cols].values.flatten()
freq = Counter(all_numbers)

total_draws = len(df)
prob = {num: freq[num]/(total_draws*6) for num in freq}  # probabilidad empírica

# Mostrar ranking de los más frecuentes
ranking = sorted(prob.items(), key=lambda x: x[1], reverse=True)
expected_freq = total_draws * 6 / 56  # Frecuencia esperada si todos fueran equiprobables

# Función para clasificar número por temperatura
def clasificar_numero(num, freq, expected_freq):
    """Clasifica un número según su desviación de la frecuencia esperada"""
    deviation = ((freq[num] - expected_freq) / expected_freq) * 100
    
    if deviation > 10:
        return "🔥 Muy caliente", deviation
    elif deviation > 5:
        return "🌡️ Caliente", deviation
    elif deviation > -5:
        return "➡️ Normal", deviation
    elif deviation > -10:
        return "❄️ Frío", deviation
    else:
        return "🧊 Muy frío", deviation

# Clasificar últimos resultados
def analizar_ultimo_sorteo(numeros, nombre_sorteo, fecha_sorteo):
    """Analiza los números del último sorteo y los clasifica por temperatura"""
    if not numeros:
        return None
    
    resultados = []
    for num in numeros:
        estado, desv = clasificar_numero(num, freq, expected_freq)
        resultados.append({
            'numero': int(num),
            'frecuencia': freq[num],
            'desviacion': desv,
            'estado': estado
        })
    
    # Calcular estadísticas del sorteo
    muy_calientes = sum(1 for r in resultados if "Muy caliente" in r['estado'])
    calientes = sum(1 for r in resultados if "Caliente" in r['estado'] and "Muy caliente" not in r['estado'])
    normales = sum(1 for r in resultados if "Normal" in r['estado'])
    frios = sum(1 for r in resultados if "Frío" in r['estado'] and "Muy frío" not in r['estado'])
    muy_frios = sum(1 for r in resultados if "Muy frío" in r['estado'])
    
    # Normalizar/formatear la fecha para una presentación consistente
    fecha_formateada = None
    if fecha_sorteo is not None:
        try:
            # Intentar parsear con pandas para muchos formatos comunes
            fecha_dt = pd.to_datetime(fecha_sorteo, dayfirst=True, errors='coerce')
            if pd.notna(fecha_dt):
                fecha_formateada = fecha_dt.strftime('%d/%m/%Y')
            else:
                # Si no se pudo parsear, usar la representación tal cual
                fecha_formateada = str(fecha_sorteo)
        except Exception:
            fecha_formateada = str(fecha_sorteo)

    return {
        'nombre': nombre_sorteo,
        'fecha': fecha_formateada,
        'numeros': resultados,
        'muy_calientes': muy_calientes,
        'calientes': calientes,
        'normales': normales,
        'frios': frios,
        'muy_frios': muy_frios
    }

analisis_melate = analizar_ultimo_sorteo(ultimo_melate, "Melate", fecha_melate) if ultimo_melate else None
analisis_revancha = analizar_ultimo_sorteo(ultimo_revancha, "Revancha", fecha_revancha) if ultimo_revancha else None
analisis_revanchita = analizar_ultimo_sorteo(ultimo_revanchita, "Revanchita", fecha_revanchita) if ultimo_revanchita else None

print("=" * 85)
print("🎱 TOP 20 NÚMEROS MÁS FRECUENTES")
print("=" * 85)
print(f"{'Pos':>3} │ {'Núm':>3} │ {'Frec':>5} │ {'%Sorteos':>9} │ {'Desv':>7} │ {'Estado'}")
print("─" * 85)
for i, (num, p) in enumerate(ranking[:20], 1):
    pct_sorteos = (freq[num] / total_draws) * 100
    deviation = ((freq[num] - expected_freq) / expected_freq) * 100
    
    # Indicador de estado
    if deviation > 10:
        estado = "🔥 Muy caliente"
    elif deviation > 5:
        estado = "🌡️ Caliente"
    elif deviation > -5:
        estado = "➡️ Normal"
    elif deviation > -10:
        estado = "❄️ Frío"
    else:
        estado = "🧊 Muy frío"
    
    print(f"{i:3} │ {int(num):3} │ {freq[num]:5} │ {pct_sorteos:8.1f}% │ {deviation:+6.1f}% │ {estado}")

# 1.5 Números más fríos
print("\n" + "=" * 85)
print("🧊 TOP 20 NÚMEROS MÁS FRÍOS (MENOS FRECUENTES)")
print("=" * 85)
print(f"{'Pos':>3} │ {'Núm':>3} │ {'Frec':>5} │ {'%Sorteos':>9} │ {'Desv':>7} │ {'Estado'}")
print("─" * 85)
for i, (num, p) in enumerate(reversed(ranking[-20:]), 1):
    pct_sorteos = (freq[num] / total_draws) * 100
    deviation = ((freq[num] - expected_freq) / expected_freq) * 100
    
    # Indicador de estado
    if deviation > 10:
        estado = "🔥 Muy caliente"
    elif deviation > 5:
        estado = "🌡️ Caliente"
    elif deviation > -5:
        estado = "➡️ Normal"
    elif deviation > -10:
        estado = "❄️ Frío"
    else:
        estado = "🧊 Muy frío"
    
    print(f"{i:3} │ {int(num):3} │ {freq[num]:5} │ {pct_sorteos:8.1f}% │ {deviation:+6.1f}% │ {estado}")

# Mostrar indicador de calor de últimos sorteos
if analisis_melate or analisis_revancha or analisis_revanchita:
    print("\n" + "=" * 85)
    print("🌡️ INDICADOR DE CALOR - ÚLTIMOS RESULTADOS")
    print("=" * 85)
    
    for analisis in [analisis_melate, analisis_revancha, analisis_revanchita]:
        if analisis:
            print(f"\n{'─' * 85}")
            print(f"🎰 {analisis['nombre'].upper()} - 📅 Sorteo del {analisis['fecha']}")
            print(f"{'─' * 85}")
            print(f"{'Núm':>4} │ {'Frec':>5} │ {'Desv':>7} │ {'Estado':<20}")
            print("─" * 85)
            for res in analisis['numeros']:
                print(f"{res['numero']:4} │ {res['frecuencia']:5} │ {res['desviacion']:+6.1f}% │ {res['estado']}")
            
            print(f"\n📊 Resumen: {analisis['muy_calientes']}🔥 | {analisis['calientes']}🌡️ | "
                  f"{analisis['normales']}➡️ | {analisis['frios']}❄️ | {analisis['muy_frios']}🧊")

# 2. Pares más comunes
pairs = Counter()
for row in df[cols].values:
    for comb in combinations(sorted(row), 2):
        pairs[comb] += 1

print("\n" + "=" * 70)
print("👥 TOP 10 PARES MÁS COMUNES")
print("=" * 70)
for i, (comb, c) in enumerate(pairs.most_common(10), 1):
    print(f"{i:2}. ({int(comb[0]):2}, {int(comb[1]):2}) │ {c:3} veces")

# 3. Tríadas más comunes
triplets = Counter()
for row in df[cols].values:
    for comb in combinations(sorted(row), 3):
        triplets[comb] += 1

print("\n" + "=" * 70)
print("🎯 TOP 10 TRÍADAS MÁS COMUNES")
print("=" * 70)
for i, (comb, c) in enumerate(triplets.most_common(10), 1):
    print(f"{i:2}. ({int(comb[0]):2}, {int(comb[1]):2}, {int(comb[2]):2}) │ {c:2} veces")

# 3.5. Cuartetos más comunes
quartets = Counter()
for row in df[cols].values:
    for comb in combinations(sorted(row), 4):
        quartets[comb] += 1

print("\n" + "=" * 70)
print("🎪 TOP 10 CUARTETOS MÁS COMUNES")
print("=" * 70)
for i, (comb, c) in enumerate(quartets.most_common(10), 1):
    print(f"{i:2}. ({int(comb[0]):2}, {int(comb[1]):2}, {int(comb[2]):2}, {int(comb[3]):2}) │ {c:2} veces")

# 3.6. Quintetos más comunes
quintets = Counter()
for row in df[cols].values:
    for comb in combinations(sorted(row), 5):
        quintets[comb] += 1

print("\n" + "=" * 70)
print("🌟 TOP 10 QUINTETOS MÁS COMUNES")
print("=" * 70)
for i, (comb, c) in enumerate(quintets.most_common(10), 1):
    print(f"{i:2}. ({int(comb[0]):2}, {int(comb[1]):2}, {int(comb[2]):2}, {int(comb[3]):2}, {int(comb[4]):2}) │ {c:2} veces")

# 4. Permutaciones completas repetidas
full_combos = Counter()
for row in df[cols].values:
    full_combos[tuple(sorted(row))] += 1

print("\n" + "=" * 70)
print("🔄 COMBINACIONES COMPLETAS REPETIDAS")
print("=" * 70)
repeated = [(comb, c) for comb, c in full_combos.items() if c > 1]
if repeated:
    for comb, c in repeated:
        nums = ", ".join([f"{int(x):2}" for x in comb])
        print(f"({nums}) │ {c} veces")
else:
    print("No hay combinaciones completas repetidas")
print("=" * 70)

# 5. Recomendaciones basadas en análisis + fecha como factor aleatorio
today = datetime.now()
seed = int(today.strftime("%Y%m%d"))  # Formato: 20251115
random.seed(seed)

# Obtener los números más frecuentes y menos frecuentes
top_numbers = [int(num) for num, _ in ranking[:30]]  # Top 30 más frecuentes
cold_numbers = [int(num) for num, _ in reversed(ranking[-20:])]  # 20 más fríos
all_numbers_list = list(range(1, 57))  # Todos los números del 1 al 56

print("\n" + "=" * 85)
print(f"🎲 RECOMENDACIONES DEL DÍA ({today.strftime('%d/%m/%Y')})")
print("=" * 85)

# Estrategia 1: Personalizada (Híbrida)
print("\n📋 ESTRATEGIA 1: HÍBRIDA (4 calientes + 2 aleatorios)\n")
for i in range(1, 6):
    selected = random.sample(top_numbers, 4)
    remaining = [n for n in all_numbers_list if n not in selected]
    selected.extend(random.sample(remaining, 2))
    selected.sort()
    nums_str = " - ".join([f"{n:2}" for n in selected])
    print(f"  Combinación {i}: [{nums_str}]")

# Estrategia 2: Conservadora (solo calientes)
print("\n🔥 ESTRATEGIA 2: CONSERVADORA (solo números calientes)\n")
random.seed(seed + 1000)  # Diferente seed para variedad
for i in range(1, 6):
    selected = random.sample(top_numbers[:20], 6)  # Top 20 más calientes
    selected.sort()
    nums_str = " - ".join([f"{n:2}" for n in selected])
    print(f"  Combinación {i}: [{nums_str}]")

# Estrategia 3: Contrarian (solo fríos)
print("\n🧊 ESTRATEGIA 3: CONTRARIAN (números fríos - apuesta a reversión)\n")
random.seed(seed + 2000)
for i in range(1, 6):
    selected = random.sample(cold_numbers[:15], 6)  # 15 más fríos
    selected.sort()
    nums_str = " - ".join([f"{n:2}" for n in selected])
    print(f"  Combinación {i}: [{nums_str}]")

# Estrategia 4: Balanceada (3 calientes + 3 fríos)
print("\n⚖️ ESTRATEGIA 4: BALANCEADA (3 calientes + 3 fríos)\n")
random.seed(seed + 3000)
for i in range(1, 6):
    hot = random.sample(top_numbers[:15], 3)
    cold = random.sample(cold_numbers[:12], 3)
    selected = sorted(hot + cold)
    nums_str = " - ".join([f"{n:2}" for n in selected])
    print(f"  Combinación {i}: [{nums_str}]")

# Estrategia 5: Serendipity (mezcla de todas las estrategias)
print("\n✨ ESTRATEGIA 5: SERENDIPITY (mezcla aleatoria de todas las estrategias)\n")
random.seed(seed + 4000)
for i in range(1, 6):
    strategy_choice = random.randint(1, 4)
    
    if strategy_choice == 1:  # Híbrida
        selected = random.sample(top_numbers, 4)
        remaining = [n for n in all_numbers_list if n not in selected]
        selected.extend(random.sample(remaining, 2))
    elif strategy_choice == 2:  # Conservadora
        selected = random.sample(top_numbers[:20], 6)
    elif strategy_choice == 3:  # Contrarian
        selected = random.sample(cold_numbers[:15], 6)
    else:  # Balanceada
        hot = random.sample(top_numbers[:15], 3)
        cold = random.sample(cold_numbers[:12], 3)
        selected = hot + cold
    
    selected.sort()
    strategy_name = ["Híbrida", "Conservadora", "Contrarian", "Balanceada"][strategy_choice - 1]
    nums_str = " - ".join([f"{n:2}" for n in selected])
    print(f"  Combinación {i} ({strategy_name}): [{nums_str}]")

print("=" * 85)

# 6. Guardar resultados en archivo markdown
print("\n💾 Guardando resultados en ANALISIS.md...")

# Crear gráficas de distribución de temperatura para cada sorteo (si matplotlib disponible)
def plot_heat_distribution(analisis, out_dir="plots"):
    # Import matplotlib lazily to avoid hard dependency at module import time
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception:
        return None
    if analisis is None:
        return None

    # Usar los conteos ya calculados en analisis
    labels = ["Muy caliente", "Caliente", "Normal", "Frío", "Muy frío"]
    values = [
        analisis['muy_calientes'],
        analisis['calientes'],
        analisis['normales'],
        analisis['frios'],
        analisis['muy_frios']
    ]

    # Crear carpeta si no existe
    os.makedirs(out_dir, exist_ok=True)

    slug = analisis['nombre'].lower().replace(' ', '_')
    filename = os.path.join(out_dir, f"indicador_calor_{slug}.png")

    try:
        plt.figure(figsize=(10, 5), dpi=100)
        # Colores suaves/pastel para las categorías (menos brillantes)
        bar_colors = ['#e8a0a0', '#f5d5b8', '#e8e8e8', '#c5d9f1', '#b0b5d9']

        if sum(values) == 0:
            # No hay datos, crear una gráfica vacía
            plt.bar(range(len(labels)), [0]*len(labels), color=['#f0f0f0']*len(labels))
            plt.xticks(range(len(labels)), labels, rotation=45, ha='right', fontsize=9)
        else:
            # Mostrar TODAS las categorías, incluso las con valor 0
            bars = plt.bar(range(len(labels)), values, color=bar_colors)
            plt.xticks(range(len(labels)), labels, rotation=45, ha='right', fontsize=9)
            plt.ylabel('Cantidad', fontsize=10)
            plt.title(f"Distribución de temperatura - {analisis['nombre']}", fontsize=11, fontweight='bold')
            plt.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Añadir valores en las barras (solo si > 0)
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.savefig(filename, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        return filename
    except Exception:
        try:
            plt.close()
        except Exception:
            pass
        return None

# Generar gráficas para cada análisis de último sorteo
plot_files = {}
for a in [(analisis_melate, 'melate'), (analisis_revancha, 'revancha'), (analisis_revanchita, 'revanchita')]:
    if a[0]:
        p = plot_heat_distribution(a[0])
        if p:
            plot_files[a[1]] = p

# La funcionalidad de "campana" (histograma + ajuste normal) se ha removido
# para simplificar las visualizaciones. Solo se generan ahora los gráficos
# de pastel (indicador de calor) y se insertan en el documento.

with open("ANALISIS.md", "w", encoding="utf-8") as f:
    f.write("# 📊 Análisis de Lotería Melate\n\n")
    f.write(f"**Fecha del análisis**: {today.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
    f.write("📚 **[Leer Metodología y Fundamentos Estadísticos](https://mariotristan.github.io/melate/METODOLOGIA)** - Comprende los fundamentos teóricos, estrategias y limitaciones del análisis.\n\n")
    f.write("---\n\n")
    
    # Información de archivos de datos
    f.write("## 📂 Información de Archivos de Datos\n\n")
    f.write("| Archivo | Última Actualización | Sorteos |\n")
    f.write("|:-------:|:--------------------:|:-------:|\n")
    f.write(f"| 🎱 Melate.csv | {melate_mtime.strftime('%d/%m/%Y %H:%M:%S')} | {len(melate_df):,} |\n")
    f.write(f"| 🔄 Revancha.csv | {revancha_mtime.strftime('%d/%m/%Y %H:%M:%S')} | {len(revancha_df):,} |\n")
    f.write(f"| ⭐ Revanchita.csv | {revanchita_mtime.strftime('%d/%m/%Y %H:%M:%S')} | {len(revanchita_df):,} |\n\n")
    f.write("---\n\n")
    
    # Resumen
    f.write("## 📈 Resumen General\n\n")
    f.write(f"- **Total de sorteos analizados**: {len(df):,}\n")
    f.write(f"  - 🎱 Melate: {len(melate_df):,}\n")
    f.write(f"  - 🔄 Revancha: {len(revancha_df):,}\n")
    f.write(f"  - ⭐ Revanchita: {len(revanchita_df):,}\n\n")
    f.write("---\n\n")
    
    # Top números
    f.write("## 🎱 Top 20 Números Más Frecuentes\n\n")
    
    # Calcular estadísticas
    avg_freq = sum(freq.values()) / len(freq)
    expected_freq = total_draws * 6 / 56  # Frecuencia esperada si todos fueran equiprobables
    
    f.write("| Pos | Número | Frecuencia | % Sorteos | Desviación | Estado |\n")
    f.write("|:---:|:------:|:----------:|:---------:|:----------:|:------:|\n")
    for i, (num, p) in enumerate(ranking[:20], 1):
        pct_sorteos = (freq[num] / total_draws) * 100
        deviation = ((freq[num] - expected_freq) / expected_freq) * 100
        # Indicador de estado
        if deviation > 10:
            estado = "🔥 Muy caliente"
        elif deviation > 5:
            estado = "🌡️ Caliente"
        elif deviation > -5:
            estado = "➡️ Normal"
        elif deviation > -10:
            estado = "❄️ Frío"
        else:
            estado = "🧊 Muy frío"
        # Validar que todos los valores estén presentes y sean string
        fila = [str(i), f"**{int(num)}**", str(freq[num]), f"{pct_sorteos:.1f}%", f"{deviation:+.1f}%", estado]
        # Unir con separador de columna y asegurar longitud
        if len(fila) == 6:
            f.write("| " + " | ".join(fila) + " |\n")
        else:
            # Si por alguna razón la fila está incompleta, rellenar con vacío
            while len(fila) < 6:
                fila.append("")
            f.write("| " + " | ".join(fila) + " |\n")
    # --- Recomendación de estrategia según tendencia de calor ---
    f.write("---\n\n")
    f.write("## 🤔 Recomendación de Estrategia según Tendencia de Calor\n\n")
    # Analizar tendencia del último sorteo principal (Melate)
    if analisis_melate:
        total = sum([
            analisis_melate['muy_calientes'],
            analisis_melate['calientes'],
            analisis_melate['normales'],
            analisis_melate['frios'],
            analisis_melate['muy_frios']
        ])
        calientes = analisis_melate['muy_calientes'] + analisis_melate['calientes']
        frios = analisis_melate['muy_frios'] + analisis_melate['frios']
        normales = analisis_melate['normales']
        # Decisión
        if calientes >= 4:
            f.write("**Tendencia observada:** El último sorteo tuvo mayoría de números calientes.\n\n")
            f.write("**Recomendación:** Evita la estrategia conservadora (solo calientes), ya que es probable que los números calientes hayan sido sobreutilizados. Opta por la estrategia **balanceada** (3 calientes + 3 fríos) o la **contrarian** (fríos), buscando reversión estadística.\n\n")
            f.write("**Razonamiento:** Cuando los números calientes dominan, la probabilidad de que sigan saliendo disminuye por regresión a la media. Apostar por equilibrio o por fríos puede aprovechar ciclos de reversión.")
        elif frios >= 4:
            f.write("**Tendencia observada:** El último sorteo tuvo mayoría de números fríos.\n\n")
            f.write("**Recomendación:** La estrategia **contrarian** (fríos) o **balanceada** tiene más sentido, ya que los números fríos pueden estar en fase de reversión.\n\n")
            f.write("**Razonamiento:** Los números fríos tienden a compensar su baja frecuencia en ciclos largos. Apostar por ellos puede anticipar una reversión estadística.")
        elif normales >= 4:
            f.write("**Tendencia observada:** El último sorteo fue equilibrado, con mayoría de números normales.\n\n")
            f.write("**Recomendación:** La estrategia **balanceada** o **híbrida** es la más sensata, ya que no hay una tendencia clara.\n\n")
            f.write("**Razonamiento:** Cuando no hay predominio de calientes ni fríos, conviene diversificar y equilibrar el riesgo.")
        else:
            f.write("**Tendencia observada:** El último sorteo fue mixto.\n\n")
            f.write("**Recomendación:** La estrategia **balanceada** es la más robusta, pero puedes probar también la **serendipity** para diversificar.\n\n")
            f.write("**Razonamiento:** En escenarios mixtos, el equilibrio y la aleatoriedad controlada suelen ser óptimos.")
    else:
        f.write("No se pudo analizar la tendencia de calor del último sorteo.\n\n")
    f.write("---\n\n")
    f.write("## ⚠️ Disclaimer\n\n")
    f.write("> Este análisis es con fines educativos y estadísticos únicamente. ")
    f.write("Los sorteos de lotería son eventos aleatorios y los resultados pasados ")
    f.write("NO garantizan resultados futuros. Juega responsablemente.\n\n")
    f.write("---\n\n")
    f.write(f"*Generado automáticamente el {today.strftime('%d/%m/%Y a las %H:%M:%S')}*\n")
    
    # Indicador de calor de últimos sorteos
    if analisis_melate or analisis_revancha or analisis_revanchita:
        f.write("## 🌡️ Indicador de Calor - Últimos Resultados\n\n")
        f.write("Esta sección compara los números del último sorteo de cada lotería contra las categorías de temperatura (caliente/frío) basadas en su frecuencia histórica.\n\n")
        
        for analisis in [analisis_melate, analisis_revancha, analisis_revanchita]:
            if analisis:
                # Incluir la fecha del sorteo en el encabezado cuando esté disponible
                fecha_text = f" - Sorteo del {analisis['fecha']}" if analisis.get('fecha') else ""
                f.write(f"### 🎰 {analisis['nombre']}{fecha_text}\n\n")
                f.write("| Número | Frecuencia | Desviación | Estado |\n")
                f.write("|:------:|:----------:|:----------:|:------:|\n")
                for res in analisis['numeros']:
                    f.write(f"| **{res['numero']}** | {res['frecuencia']} | {res['desviacion']:+.1f}% | {res['estado']} |\n")

                f.write(f"\n**📊 Distribución de temperatura:**\n")
                f.write(f"- 🔥 Muy calientes: {analisis['muy_calientes']}\n")
                f.write(f"- 🌡️ Calientes: {analisis['calientes']}\n")
                f.write(f"- ➡️ Normales: {analisis['normales']}\n")
                f.write(f"- ❄️ Fríos: {analisis['frios']}\n")
                f.write(f"- 🧊 Muy fríos: {analisis['muy_frios']}\n\n")

                # Incrustar la gráfica si fue generada
                slug = analisis['nombre'].lower().replace(' ', '_')
                img_path = plot_files.get(slug)
                if img_path:
                    f.write(f"![Distribución de temperatura - {analisis['nombre']}]({img_path})\n\n")

                # La gráfica tipo 'campana' fue eliminada; solo mostramos el pastel de distribución.
        
        f.write("---\n\n")
    
    # Pares
    f.write("## 👥 Top 10 Pares Más Comunes\n\n")
    f.write("| Posición | Par | Frecuencia |\n")
    f.write("|:--------:|:---:|:----------:|\n")
    for i, (comb, c) in enumerate(pairs.most_common(10), 1):
        f.write(f"| {i} | ({int(comb[0])}, {int(comb[1])}) | {c} veces |\n")
    f.write("\n---\n\n")
    
    # Tríadas
    f.write("## 🎯 Top 10 Tríadas Más Comunes\n\n")
    f.write("| Posición | Tríada | Frecuencia |\n")
    f.write("|:--------:|:------:|:----------:|\n")
    for i, (comb, c) in enumerate(triplets.most_common(10), 1):
        f.write(f"| {i} | ({int(comb[0])}, {int(comb[1])}, {int(comb[2])}) | {c} veces |\n")
    f.write("\n---\n\n")
    
    # Cuartetos
    f.write("## 🎪 Top 10 Cuartetos Más Comunes\n\n")
    f.write("| Posición | Cuarteto | Frecuencia |\n")
    f.write("|:--------:|:--------:|:----------:|\n")
    for i, (comb, c) in enumerate(quartets.most_common(10), 1):
        f.write(f"| {i} | ({int(comb[0])}, {int(comb[1])}, {int(comb[2])}, {int(comb[3])}) | {c} veces |\n")
    f.write("\n---\n\n")
    
    # Quintetos
    f.write("## 🌟 Top 10 Quintetos Más Comunes\n\n")
    f.write("| Posición | Quinteto | Frecuencia |\n")
    f.write("|:--------:|:--------:|:----------:|\n")
    for i, (comb, c) in enumerate(quintets.most_common(10), 1):
        f.write(f"| {i} | ({int(comb[0])}, {int(comb[1])}, {int(comb[2])}, {int(comb[3])}, {int(comb[4])}) | {c} veces |\n")
    f.write("\n---\n\n")
    
    # Combinaciones repetidas
    f.write("## 🔄 Combinaciones Completas Repetidas\n\n")
    if repeated:
        f.write("| Combinación Completa | Frecuencia |\n")
        f.write("|:--------------------:|:----------:|\n")
        for comb, c in repeated:
            nums = ", ".join([f"{int(x)}" for x in comb])
            f.write(f"| ({nums}) | {c} veces |\n")
    else:
        f.write("No hay combinaciones completas que se hayan repetido.\n")
    f.write("\n---\n\n")
    
    # Recomendaciones
    f.write(f"## 🎲 Recomendaciones del Día ({today.strftime('%d/%m/%Y')})\n\n")
    f.write("### 📊 Cinco Estrategias Diferentes\n\n")
    f.write("Todas las recomendaciones usan la fecha actual como semilla para generar combinaciones consistentes y reproducibles.\n\n")
    
    # Estrategia 1: Híbrida
    f.write("#### 📋 Estrategia 1: HÍBRIDA (4 calientes + 2 aleatorios)\n\n")
    f.write("Combina números de alta frecuencia con selección aleatoria para diversificar el riesgo.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    random.seed(seed)
    for i in range(1, 6):
        selected = random.sample(top_numbers, 4)
        remaining = [n for n in all_numbers_list if n not in selected]
        selected.extend(random.sample(remaining, 2))
        selected.sort()
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")
    
    # Estrategia 2: Conservadora
    f.write("#### 🔥 Estrategia 2: CONSERVADORA (solo números calientes)\n\n")
    f.write("Apuesta exclusivamente por los números más frecuentes históricamente.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    random.seed(seed + 1000)
    for i in range(1, 6):
        selected = random.sample(top_numbers[:20], 6)
        selected.sort()
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")
    
    # Estrategia 3: Contrarian
    f.write("#### 🧊 Estrategia 3: CONTRARIAN (números fríos)\n\n")
    f.write("Apuesta a la reversión: números que han salido menos podrían \"compensar\" estadísticamente.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    random.seed(seed + 2000)
    for i in range(1, 6):
        selected = random.sample(cold_numbers[:15], 6)
        selected.sort()
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")
    
    # Estrategia 4: Balanceada
    f.write("#### ⚖️ Estrategia 4: BALANCEADA (3 calientes + 3 fríos)\n\n")
    f.write("Equilibrio perfecto entre números frecuentes y poco frecuentes.\n\n")
    f.write("| # | Combinación |\n")
    f.write("|:-:|:-----------|\n")
    random.seed(seed + 3000)
    for i in range(1, 6):
        hot = random.sample(top_numbers[:15], 3)
        cold = random.sample(cold_numbers[:12], 3)
        selected = sorted(hot + cold)
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | **{nums_str}** |\n")
    f.write("\n")
    
    # Estrategia 5: Serendipity
    f.write("#### ✨ Estrategia 5: SERENDIPITY (mezcla de todas)\n\n")
    f.write("Cada combinación usa aleatoriamente una de las 4 estrategias anteriores. ¡Deja que el destino elija!\n\n")
    f.write("| # | Estrategia | Combinación |\n")
    f.write("|:-:|:----------:|:-----------|\n")
    random.seed(seed + 4000)
    for i in range(1, 6):
        strategy_choice = random.randint(1, 4)
        
        if strategy_choice == 1:  # Híbrida
            selected = random.sample(top_numbers, 4)
            remaining = [n for n in all_numbers_list if n not in selected]
            selected.extend(random.sample(remaining, 2))
        elif strategy_choice == 2:  # Conservadora
            selected = random.sample(top_numbers[:20], 6)
        elif strategy_choice == 3:  # Contrarian
            selected = random.sample(cold_numbers[:15], 6)
        else:  # Balanceada
            hot = random.sample(top_numbers[:15], 3)
            cold = random.sample(cold_numbers[:12], 3)
            selected = hot + cold
        
        selected.sort()
        strategy_name = ["📋 Híbrida", "🔥 Conservadora", "🧊 Contrarian", "⚖️ Balanceada"][strategy_choice - 1]
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"| {i} | {strategy_name} | **{nums_str}** |\n")
    
    f.write("\n---\n\n")
    f.write("## ⚠️ Disclaimer\n\n")
    f.write("> Este análisis es con fines educativos y estadísticos únicamente. ")
    f.write("Los sorteos de lotería son eventos aleatorios y los resultados pasados ")
    f.write("NO garantizan resultados futuros. Juega responsablemente.\n\n")
    f.write("---\n\n")
    f.write(f"*Generado automáticamente el {today.strftime('%d/%m/%Y a las %H:%M:%S')}*\n")

print("✅ Resultados guardados exitosamente en ANALISIS.md")


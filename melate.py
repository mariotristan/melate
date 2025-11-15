import pandas as pd
from collections import Counter
from itertools import combinations
import random
from datetime import datetime

# Cargar los tres archivos CSV
melate_df = pd.read_csv("Melate.csv")
revancha_df = pd.read_csv("Revancha.csv")
revanchita_df = pd.read_csv("Revanchita.csv")

# Revanchita usa F1-F6, necesitamos renombrar a R1-R6
revanchita_df = revanchita_df.rename(columns={
    'F1': 'R1', 'F2': 'R2', 'F3': 'R3', 
    'F4': 'R4', 'F5': 'R5', 'F6': 'R6'
})

# Combinar todos los dataframes
df = pd.concat([melate_df, revancha_df, revanchita_df], ignore_index=True)

# Columnas de números
cols = ["R1","R2","R3","R4","R5","R6"]

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
print("=" * 70)
print("🎱 TOP 20 NÚMEROS MÁS FRECUENTES")
print("=" * 70)
for i, (num, p) in enumerate(ranking[:20], 1):
    bar = "█" * int(p * 500)
    print(f"{i:2}. Número {int(num):2} │ {freq[num]:3} veces │ {p:6.3%} {bar}")

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

# Obtener los números más frecuentes como base
top_numbers = [int(num) for num, _ in ranking[:30]]  # Top 30 más frecuentes
all_numbers_list = list(range(1, 56))  # Todos los números del 1 al 55

print("\n" + "=" * 70)
print(f"🎲 RECOMENDACIONES DEL DÍA ({today.strftime('%d/%m/%Y')})")
print("=" * 70)
print("Estrategia: Combinación de números frecuentes + aleatorización por fecha\n")

for i in range(1, 6):
    # Mezclar estrategia: 4 números de los top + 2 aleatorios
    selected = random.sample(top_numbers, 4)
    remaining = [n for n in all_numbers_list if n not in selected]
    selected.extend(random.sample(remaining, 2))
    selected.sort()
    
    nums_str = " - ".join([f"{n:2}" for n in selected])
    print(f"Combinación {i}: [{nums_str}]")

print("=" * 70)

# 6. Guardar resultados en archivo markdown
print("\n💾 Guardando resultados en ANALISIS.md...")

with open("ANALISIS.md", "w", encoding="utf-8") as f:
    f.write("# 📊 Análisis de Lotería Melate\n\n")
    f.write(f"**Fecha del análisis**: {today.strftime('%d/%m/%Y %H:%M:%S')}\n\n")
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
    f.write("| Posición | Número | Frecuencia | Probabilidad | Gráfica |\n")
    f.write("|:--------:|:------:|:----------:|:------------:|:--------|\n")
    for i, (num, p) in enumerate(ranking[:20], 1):
        bar = "🟦" * int(p * 500)
        f.write(f"| {i} | **{int(num)}** | {freq[num]} veces | {p:.3%} | {bar} |\n")
    f.write("\n---\n\n")
    
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
    f.write("### Estrategia\n\n")
    f.write("Estas recomendaciones combinan:\n")
    f.write("- 🔥 **4 números** de los 30 más frecuentes históricamente\n")
    f.write("- 🎲 **2 números** aleatorios del conjunto completo (1-55)\n")
    f.write("- 📅 Fecha actual como semilla aleatoria\n\n")
    f.write("### Combinaciones Recomendadas\n\n")
    
    # Regenerar las combinaciones con la misma semilla
    random.seed(seed)
    for i in range(1, 6):
        selected = random.sample(top_numbers, 4)
        remaining = [n for n in all_numbers_list if n not in selected]
        selected.extend(random.sample(remaining, 2))
        selected.sort()
        
        nums_str = " - ".join([f"{n:02d}" for n in selected])
        f.write(f"#### Combinación {i}\n")
        f.write(f"```\n{nums_str}\n```\n\n")
    
    f.write("---\n\n")
    f.write("## ⚠️ Disclaimer\n\n")
    f.write("> Este análisis es con fines educativos y estadísticos únicamente. ")
    f.write("Los sorteos de lotería son eventos aleatorios y los resultados pasados ")
    f.write("NO garantizan resultados futuros. Juega responsablemente.\n\n")
    f.write("---\n\n")
    f.write(f"*Generado automáticamente el {today.strftime('%d/%m/%Y a las %H:%M:%S')}*\n")

print("✅ Resultados guardados exitosamente en ANALISIS.md")


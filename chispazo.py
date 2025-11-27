import pandas as pd
from collections import Counter
from itertools import combinations
import random
from datetime import datetime
import os

def main():
    # Cargar archivo Chispazo.csv
    df = pd.read_csv("Chispazo.csv")
    cols = ["R1", "R2", "R3", "R4", "R5"]

    # Obtener fecha de última modificación
    chispazo_mtime = datetime.fromtimestamp(os.path.getmtime("Chispazo.csv"))

    # Último sorteo
    ultimo = df.iloc[0][cols].values.astype(int).tolist() if len(df) > 0 else []
    fecha_ultimo = df.iloc[0]['FECHA'] if len(df) > 0 else None

    print(f"\n📊 Total de sorteos analizados: {len(df):,}")

    # Frecuencia de cada número
    all_numbers = df[cols].values.flatten()
    freq = Counter(all_numbers)
    total_draws = len(df)
    prob = {num: freq[num]/(total_draws*5) for num in freq}
    ranking = sorted(prob.items(), key=lambda x: x[1], reverse=True)
    expected_freq = total_draws * 5 / 28  # Chispazo: 28 números

    def clasificar_numero(num, freq, expected_freq):
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

    def analizar_ultimo_sorteo(numeros, fecha_sorteo):
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
        return resultados

    analisis_ultimo = analizar_ultimo_sorteo(ultimo, fecha_ultimo)

    print("=" * 70)
    print("🎱 TOP 10 NÚMEROS MÁS FRECUENTES")
    print("=" * 70)
    print(f"{'Pos':>3} │ {'Núm':>3} │ {'Frec':>5} │ {'%Sorteos':>9} │ {'Desv':>7} │ {'Estado'}")
    print("─" * 70)
    for i, (num, p) in enumerate(ranking[:10], 1):
        pct_sorteos = (freq[num] / total_draws) * 100
        deviation = ((freq[num] - expected_freq) / expected_freq) * 100
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

    print("\n" + "=" * 70)
    print("🧊 TOP 10 NÚMEROS MÁS FRÍOS (MENOS FRECUENTES)")
    print("=" * 70)
    print(f"{'Pos':>3} │ {'Núm':>3} │ {'Frec':>5} │ {'%Sorteos':>9} │ {'Desv':>7} │ {'Estado'}")
    print("─" * 70)
    for i, (num, p) in enumerate(reversed(ranking[-10:]), 1):
        pct_sorteos = (freq[num] / total_draws) * 100
        deviation = ((freq[num] - expected_freq) / expected_freq) * 100
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

    # Pares, tríos, cuartetos más comunes
    for k, label in [(2, "PARES"), (3, "TRÍOS"), (4, "CUARTETOS")]:
        combos = Counter()
        for row in df[cols].values:
            for comb in combinations(sorted(row), k):
                combos[comb] += 1
        print("\n" + "=" * 50)
        print(f"👥 TOP 5 {label} MÁS COMUNES")
        print("=" * 50)
        for i, (comb, c) in enumerate(combos.most_common(5), 1):
            nums = ", ".join([str(x) for x in comb])
            print(f"{i:2}. ({nums}) │ {c:3} veces")

    # Recomendaciones
    today = datetime.now()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    top_numbers = [int(num) for num, _ in ranking[:15]]
    cold_numbers = [int(num) for num, _ in reversed(ranking[-10:])]
    all_numbers_list = list(range(1, 29))

    print("\n" + "=" * 70)
    print(f"🎲 RECOMENDACIONES DEL DÍA ({today.strftime('%d/%m/%Y')})")
    print("=" * 70)
    print("Estrategia 1: 3 calientes + 2 aleatorios")
    for i in range(1, 6):
        selected = random.sample(top_numbers, 3)
        remaining = [n for n in all_numbers_list if n not in selected]
        selected.extend(random.sample(remaining, 2))
        selected.sort()
        nums_str = " - ".join([f"{n:2}" for n in selected])
        print(f"  Combinación {i}: [{nums_str}]")
    print("Estrategia 2: Solo calientes")
    random.seed(seed + 1000)
    for i in range(1, 6):
        selected = random.sample(top_numbers, 5)
        selected.sort()
        nums_str = " - ".join([f"{n:2}" for n in selected])
        print(f"  Combinación {i}: [{nums_str}]")
    print("Estrategia 3: Solo fríos")
    random.seed(seed + 2000)
    for i in range(1, 6):
        selected = random.sample(cold_numbers, 5)
        selected.sort()
        nums_str = " - ".join([f"{n:2}" for n in selected])
        print(f"  Combinación {i}: [{nums_str}]")
    print("Estrategia 4: 2 calientes + 3 fríos")
    random.seed(seed + 3000)
    for i in range(1, 6):
        hot = random.sample(top_numbers, 2)
        cold = random.sample(cold_numbers, 3)
        selected = sorted(hot + cold)
        nums_str = " - ".join([f"{n:2}" for n in selected])
        print(f"  Combinación {i}: [{nums_str}]")
    print("Estrategia 5: Serendipity")
    random.seed(seed + 4000)
    for i in range(1, 6):
        strategy_choice = random.randint(1, 4)
        if strategy_choice == 1:
            selected = random.sample(top_numbers, 3)
            remaining = [n for n in all_numbers_list if n not in selected]
            selected.extend(random.sample(remaining, 2))
        elif strategy_choice == 2:
            selected = random.sample(top_numbers, 5)
        elif strategy_choice == 3:
            selected = random.sample(cold_numbers, 5)
        else:
            hot = random.sample(top_numbers, 2)
            cold = random.sample(cold_numbers, 3)
            selected = hot + cold
        selected.sort()
        nums_str = " - ".join([f"{n:2}" for n in selected])
        print(f"  Combinación {i}: [{nums_str}]")

    # Guardar resultados en ANALISIS_CHISPAZO.md
    with open("ANALISIS_CHISPAZO.md", "w", encoding="utf-8") as f:
        f.write("# Análisis Chispazo\n\n")
        f.write(f"**Total de sorteos analizados:** {len(df):,}\n\n")
        f.write("## Top 10 números más frecuentes\n\n")
        f.write("| Pos | Núm | Frec | %Sorteos | Desv | Estado |\n")
        f.write("|-----|-----|------|----------|------|--------|\n")
        for i, (num, p) in enumerate(ranking[:10], 1):
            pct_sorteos = (freq[num] / total_draws) * 100
            deviation = ((freq[num] - expected_freq) / expected_freq) * 100
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
            f.write(f"| {i:3} | {int(num):3} | {freq[num]:5} | {pct_sorteos:8.1f}% | {deviation:+6.1f}% | {estado} |\n")
        f.write("\n## Top 10 números más fríos\n\n")
        f.write("| Pos | Núm | Frec | %Sorteos | Desv | Estado |\n")
        f.write("|-----|-----|------|----------|------|--------|\n")
        for i, (num, p) in enumerate(reversed(ranking[-10:]), 1):
            pct_sorteos = (freq[num] / total_draws) * 100
            deviation = ((freq[num] - expected_freq) / expected_freq) * 100
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
            f.write(f"| {i:3} | {int(num):3} | {freq[num]:5} | {pct_sorteos:8.1f}% | {deviation:+6.1f}% | {estado} |\n")
        # Pares, tríos, cuartetos
        for k, label in [(2, "PARES"), (3, "TRÍOS"), (4, "CUARTETOS")]:
            combos = Counter()
            for row in df[cols].values:
                for comb in combinations(sorted(row), k):
                    combos[comb] += 1
            f.write(f"\n### Top 5 {label} más comunes\n\n")
            for i, (comb, c) in enumerate(combos.most_common(5), 1):
                nums = ", ".join([str(x) for x in comb])
                f.write(f"{i:2}. ({nums}) │ {c:3} veces\n")
        # Recomendaciones
        f.write(f"\n## Recomendaciones del día ({today.strftime('%d/%m/%Y')})\n\n")
        f.write("| Estrategia | Combinación | Números |\n")
        f.write("|------------|-------------|---------|\n")
        # Estrategia 1
        for i in range(1, 6):
            selected = random.sample(top_numbers, 3)
            remaining = [n for n in all_numbers_list if n not in selected]
            selected.extend(random.sample(remaining, 2))
            selected.sort()
            nums_str = ", ".join(str(n) for n in selected)
            f.write(f"| 3 calientes + 2 aleatorios | {i} | {nums_str} |\n")
        # Estrategia 2
        random.seed(seed + 1000)
        for i in range(1, 6):
            selected = random.sample(top_numbers, 5)
            selected.sort()
            nums_str = ", ".join(str(n) for n in selected)
            f.write(f"| Solo calientes | {i} | {nums_str} |\n")
        # Estrategia 3
        random.seed(seed + 2000)
        for i in range(1, 6):
            selected = random.sample(cold_numbers, 5)
            selected.sort()
            nums_str = ", ".join(str(n) for n in selected)
            f.write(f"| Solo fríos | {i} | {nums_str} |\n")
        # Estrategia 4
        random.seed(seed + 3000)
        for i in range(1, 6):
            hot = random.sample(top_numbers, 2)
            cold = random.sample(cold_numbers, 3)
            selected = sorted(hot + cold)
            nums_str = ", ".join(str(n) for n in selected)
            f.write(f"| 2 calientes + 3 fríos | {i} | {nums_str} |\n")
        # Estrategia 5
        random.seed(seed + 4000)
        for i in range(1, 6):
            strategy_choice = random.randint(1, 4)
            if strategy_choice == 1:
                selected = random.sample(top_numbers, 3)
                remaining = [n for n in all_numbers_list if n not in selected]
                selected.extend(random.sample(remaining, 2))
                label = "3 calientes + 2 aleatorios"
            elif strategy_choice == 2:
                selected = random.sample(top_numbers, 5)
                label = "Solo calientes"
            elif strategy_choice == 3:
                selected = random.sample(cold_numbers, 5)
                label = "Solo fríos"
            else:
                hot = random.sample(top_numbers, 2)
                cold = random.sample(cold_numbers, 3)
                selected = hot + cold
                label = "2 calientes + 3 fríos"
            selected.sort()
            nums_str = ", ".join(str(n) for n in selected)
            f.write(f"| Serendipity ({label}) | {i} | {nums_str} |\n")

if __name__ == "__main__":
    main()

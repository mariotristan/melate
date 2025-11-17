# 🎲 Melate Lottery Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Required-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

[![Daily Analysis](https://github.com/mariotristan/melate/actions/workflows/daily-analysis.yml/badge.svg)](https://github.com/mariotristan/melate/actions/workflows/daily-analysis.yml)
[![Publish Pages](https://github.com/mariotristan/melate/actions/workflows/publish-pages.yml/badge.svg)](https://github.com/mariotristan/melate/actions/workflows/publish-pages.yml)

**Análisis estadístico avanzado de sorteos de lotería mexicana** 🇲🇽

**📊 [Ver Análisis en Vivo](https://mariotristan.github.io/melate/)** | **🔗 [GitHub](https://github.com/mariotristan/melate)**

</div>

**🕐 Última ejecución: 17/11/2025 a las 00:22:42 UTC**

---

## 🎰 ¿Qué hace este proyecto?

Este script realiza un análisis completo de los datos históricos de **tres loterías mexicanas**:

| Lotería | Descripción | Emoji |
|---------|-------------|-------|
| 🎱 **Melate** | Sorteo principal | 💰 |
| 🔄 **Revancha** | Sorteo complementario | 💵 |
| ⭐ **Revanchita** | Sorteo adicional | 💸 |

---

## ✨ Características Principales

### 📊 Análisis Estadísticos

| # | Análisis | Descripción |
|---|----------|-------------|
| 1️⃣ | **Frecuencia Individual** | Top 20 números más sorteados con probabilidades |
| 2️⃣ | **Pares Comunes** | Combinaciones de 2 números que aparecen juntas |
| 3️⃣ | **Tríadas Comunes** | Combinaciones de 3 números |
| 4️⃣ | **Cuartetos Comunes** | Combinaciones de 4 números |
| 5️⃣ | **Quintetos Comunes** | Combinaciones de 5 números |
| 6️⃣ | **Repeticiones Exactas** | Sorteos completos que se han repetido |
| 7️⃣ | **Recomendaciones Diarias** | 5 combinaciones inteligentes basadas en estadística + fecha |

---

## 🚀 Instalación y Uso

### 📦 Requisitos Previos

```bash
# Instalar pandas
pip install pandas
```

### ▶️ Ejecutar el Análisis

```bash
python3 melate.py
```

---

## 📁 Estructura de Archivos

```
melate/
├── 📄 melate.py          # Script principal
├── 📊 Melate.csv         # Datos históricos Melate
├── 📊 Revancha.csv       # Datos históricos Revancha
├── 📊 Revanchita.csv     # Datos históricos Revanchita
├── 📖 README.md          # Este archivo
└── 🚫 .gitignore         # Archivos ignorados por Git
```

### 📋 Formato de Datos CSV

#### Melate y Revancha
```csv
NPRODUCTO,CONCURSO,R1,R2,R3,R4,R5,R6,BOLSA,FECHA
40,4135,1,11,25,31,54,55,183900000,14/11/2025
```

#### Revanchita
```csv
NPRODUCTO,CONCURSO,F1,F2,F3,F4,F5,F6,BOLSA,FECHA
34,4135,3,6,13,37,50,54,108100000,14/11/2025
```

---

## 📈 Ejemplo de Salida

### 📊 Resumen General
```
📊 Total de sorteos analizados: 9,027
   • Melate: 4,135
   • Revancha: 3,127
   • Revanchita: 1,765
```

### 🎱 Números Más Frecuentes
```
======================================================================
🎱 TOP 20 NÚMEROS MÁS FRECUENTES
======================================================================
 1. Número 24 │ 1120 veces │ 2.068% ██████████
 2. Número 32 │ 1097 veces │ 2.025% ██████████
 3. Número  5 │ 1089 veces │ 2.011% ██████████
```

### 🎲 Recomendaciones del Día
```
======================================================================
🎲 RECOMENDACIONES DEL DÍA (15/11/2025)
======================================================================
Estrategia: Combinación de números frecuentes + aleatorización por fecha

Combinación 1: [13 - 15 - 18 - 19 - 28 - 30]
Combinación 2: [15 - 33 - 36 - 37 - 39 - 40]
Combinación 3: [ 7 - 12 - 16 - 24 - 37 - 45]
```

---

## 🎯 Estrategia de Recomendaciones

<div align="center">

| Componente | Cantidad | Origen |
|------------|----------|--------|
| 🔥 **Números Calientes** | 4 números | Top 30 más frecuentes |
| 🎲 **Números Aleatorios** | 2 números | Conjunto completo (1-55) |
| 📅 **Semilla Aleatoria** | Fecha actual | Garantiza unicidad diaria |

</div>

### 🧮 Metodología

1. **Análisis histórico**: Se analizan más de 9,000 sorteos
2. **Identificación de patrones**: Se detectan números y combinaciones frecuentes
3. **Balanceo inteligente**: Mezcla de estadística y aleatoriedad
4. **Unicidad diaria**: Las recomendaciones cambian cada día

---

## ⚠️ Importante - Disclaimer

> ⚡ **Este análisis es con fines educativos y estadísticos únicamente.**

- 🎲 Los sorteos de lotería son **eventos aleatorios**
- 📊 Los resultados pasados **NO garantizan** resultados futuros
- 🎰 Cada sorteo es **independiente** del anterior
- 💰 Juega **responsablemente** y dentro de tus posibilidades

---

## 📊 Estadísticas del Proyecto

- 🔢 **Total de sorteos analizados**: ~9,000+
- 📅 **Período de datos**: Histórico hasta noviembre 2025
- 🎯 **Precisión estadística**: Basada en frecuencias empíricas
- 🔄 **Actualización**: Manual con nuevos datos CSV

---

## 🛠️ Tecnologías Utilizadas

- 🐍 **Python 3.7+**
- 🐼 **Pandas** - Análisis de datos
- 🔢 **Collections** - Contadores y estructuras
- 🎲 **Random** - Generación de recomendaciones
- 📅 **Datetime** - Semilla basada en fecha

---

## 📝 Licencia

📜 **Uso libre** para análisis personal y educativo.

---

<div align="center">

### 🌟 ¡Buena suerte! 🍀

**Made with ❤️ and 📊 Data Analysis**

</div>

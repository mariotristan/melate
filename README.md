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

**🕐 Última ejecución: 23/11/2025 a las 08:23:04 UTC**

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
### 📊 Análisis Melate

- Analiza todos los sorteos históricos de Melate (más de 4,000).
- Calcula la frecuencia absoluta de cada número (1-56).
- Genera gráficos de frecuencias y visualizaciones de combinaciones frecuentes (pares, tríadas, cuartetos, quintetos).
- Identifica repeticiones exactas de sorteos y patrones estadísticos.
- Clasifica cada número por “calor” (muy caliente, caliente, normal, frío, muy frío) según su desviación porcentual.
- Recomienda estrategias basadas en la tendencia de calor y patrones históricos.
- Ofrece cinco tipos de combinaciones diarias: híbrida, conservadora, contrarian, balanceada y serendipity, todas reproducibles y basadas en la fecha.
### 📊 Análisis Melate Retro

- Analiza todos los sorteos históricos de Melate Retro (más de 1,500).
- Calcula la frecuencia absoluta de cada número (1-39).
- Genera gráficos de frecuencias y mapas de calor para visualizar tendencias.
- Clasifica cada número por “calor” (muy caliente, caliente, normal, frío, muy frío) según su desviación porcentual.
- Recomienda estrategias basadas en la tendencia de calor del último sorteo.
- Ofrece cinco tipos de combinaciones diarias: híbrida, conservadora, contrarian, balanceada y serendipity, todas reproducibles y basadas en la fecha.

### 📊 Análisis Tris

- Analiza todos los sorteos históricos de Tris (más de 160,000).
- Calcula la frecuencia y desviación porcentual de cada dígito (0-9).
- Genera gráficos y tablas de calor para los últimos resultados.
- Clasifica cada dígito por “calor” y muestra la distribución en el último sorteo.
- Recomienda estrategias según la tendencia de calor: híbrida, conservadora, contrarian, balanceada y serendipity.
- Todas las combinaciones son válidas y reproducibles, con lógica de respaldo si faltan dígitos calientes o fríos.

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

[▶ Instalación y dependencias](./INSTALACION.md)

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
├── 📄 melate.py            # Script principal Melate
├── 📄 tris.py              # Script principal Tris
├── 📄 melate_retro.py      # Script principal Melate Retro
├── 📊 Melate.csv           # Datos históricos Melate
├── 📊 Revancha.csv         # Datos históricos Revancha
├── 📊 Revanchita.csv       # Datos históricos Revanchita
├── 📊 Tris.csv             # Datos históricos Tris
├── 📊 MelateRetro.csv      # Datos históricos Melate Retro
├── 📖 README.md            # Este archivo
├── 📄 ANALISIS.md          # Reporte de análisis Melate
├── 📄 ANALISIS_RETRO.md    # Reporte de análisis Melate Retro
├── 📄 ANALISIS_TRIS.md     # Reporte de análisis Tris
├── 📄 METODOLOGIA.md       # Documentación de metodología
├── 📄 requirements.txt     # Dependencias Python
├── 📄 tris_frecuencias.png # Gráfica de frecuencias Tris
├── 📄 retro_frecuencias.png# Gráfica de frecuencias Melate Retro
├── 📄 retro_heatmap.png    # Mapa de calor Melate Retro
├── 📄 plots/               # Gráficas adicionales
├── 🚫 .gitignore           # Archivos ignorados por Git
└── .github/workflows/      # Workflows de CI/CD (daily-analysis.yml, publish-pages.yml, tris-analysis.yml)
```

### 📥 Obtención de Datos CSV


Los archivos CSV se descargan automáticamente cada día a través del workflow de GitHub Actions (`daily-analysis.yml`).

---

### Descarga de datos para ejecuciones locales

Para descargar los archivos de datos de loterías mexicanas localmente, ejecuta el script:

```sh
bash descargar_datos.sh
```

Este script utiliza las mismas URLs que los pipelines automáticos y guarda los archivos en la raíz del proyecto.

#### Melate, Revancha y Revanchita
- [🎱 **Melate**](https://www.loterianacional.gob.mx/Home/Historicos?ARHP=TQBlAGwAYQB0AGUA)
- [🔄 **Revancha**](https://www.loterianacional.gob.mx/Home/Historicos?ARHP=UgBlAHYAYQBuAGMAaABhAA==)
- [⭐ **Revanchita**](https://www.loterianacional.gob.mx/Home/Historicos?ARHP=UgBlAHYAYQBuAGMAaABpAHQAYQA=)

#### Melate Retro
- [🔙 **Melate Retro**](https://www.loterianacional.gob.mx/Home/Historicos?ARHP=TQBlAGwAYQB0AGUAcgBlAHQAcgBvAA==)
- El archivo se descarga y procesa automáticamente por `melate_retro.py` y el workflow correspondiente.

#### Tris
- [🎲 **Tris**](https://www.loterianacional.gob.mx/Home/Historicos?ARHP=VAByAGkAcwA=)
- El archivo se descarga y procesa automáticamente por `tris.py` y el workflow correspondiente.

**Nota**: Todos los archivos se actualizan automáticamente y se procesan para análisis y generación de reportes.

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

#### Melate Retro
```csv
NPRODUCTO,CONCURSO,N1,N2,N3,N4,N5,N6,BOLSA,FECHA
41,1583,4,7,13,17,21,26,5000000,18/11/2025
```

#### Tris
```csv
CONCURSO,N1,N2,N3,N4,N5,FECHA
160000,2,6,2,9,8,21/11/2025
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

Las recomendaciones diarias para Melate, Melate Retro y Tris se generan usando cinco estrategias avanzadas:

| Estrategia      | Lógica principal |
|-----------------|-----------------|
| Híbrida         | Mezcla de números calientes y aleatorios |
| Conservadora    | Solo números calientes |
| Contrarian      | Solo números fríos |
| Balanceada      | Calientes, fríos y normales |
| Serendipity     | Combinación aleatoria de las anteriores |

**Características clave:**
- Todas las combinaciones son válidas y completas, con lógica de respaldo si no hay suficientes calientes o fríos.
- La semilla aleatoria basada en la fecha garantiza unicidad diaria y reproducibilidad.
- El análisis de calor (muy caliente, caliente, normal, frío, muy frío) guía la selección de estrategias recomendadas según la tendencia del último sorteo.

### 🧮 Metodología

1. **Análisis histórico**: Miles de sorteos analizados
2. **Identificación de patrones y calor**: Frecuencias y desviaciones
3. **Recomendaciones inteligentes**: Estrategias y balanceo
4. **Automatización diaria**: Resultados y reportes actualizados automáticamente

---

## ⚠️ Importante - Disclaimer

> ⚡ **Este análisis es con fines educativos y estadísticos únicamente.**

- 🎲 Los sorteos de lotería son **eventos aleatorios**
- 📊 Los resultados pasados **NO garantizan** resultados futuros
- 🎰 Cada sorteo es **independiente** del anterior
- 💰 Juega **responsablemente** y dentro de tus posibilidades

---

## 📊 Estadísticas del Proyecto

 - 🔢 **Total de sorteos analizados**: ~9,000+ (Melate, Revancha, Revanchita) + miles de Tris
 - 📅 **Período de datos**: Histórico hasta noviembre 2025
 - 🎯 **Precisión estadística**: Basada en frecuencias empíricas y calor
 - 🔄 **Actualización**: Automática diaria vía GitHub Actions

---

## 🛠️ Tecnologías Utilizadas

- 🐍 **Python 3.7+**
- 🐼 **Pandas** - Análisis de datos
- 🔢 **Collections** - Contadores y estructuras
- 🎲 **Random** - Generación de recomendaciones
- 📅 **Datetime** - Semilla basada en fecha

---

## 📝 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - consulta el archivo [LICENSE](LICENSE) para más detalles.

**Resumen:**
- ✅ Uso comercial permitido
- ✅ Modificación permitida
- ✅ Distribución permitida
- ✅ Uso privado permitido
- ⚠️ Sin garantía

---

<div align="center">

### 🌟 ¡Buena suerte! 🍀

**Made with ❤️,  📊 Data Analysis and AI 🤖 **

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>



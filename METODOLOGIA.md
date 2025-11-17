# 📚 Metodología y Fundamentos Estadísticos del Análisis de Lotería

## 📖 Índice

1. [Introducción](#introducción)
2. [Fundamentos Teóricos](#fundamentos-teóricos)
3. [Metodología de Análisis](#metodología-de-análisis)
4. [Estrategias de Selección](#estrategias-de-selección)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Limitaciones y Consideraciones Éticas](#limitaciones-y-consideraciones-éticas)
7. [Referencias y Lecturas Recomendadas](#referencias-y-lecturas-recomendadas)

---

## 🎯 Introducción

Este documento describe la metodología estadística empleada en el análisis de los sorteos de lotería mexicana (Melate, Revancha y Revanchita). El objetivo es proporcionar una comprensión profunda de los métodos analíticos utilizados y las bases teóricas que sustentan cada estrategia de selección.

### Objetivos del Análisis

- **Descriptivo**: Caracterizar la distribución histórica de números sorteados
- **Exploratorio**: Identificar patrones y tendencias en los datos históricos
- **Predictivo**: Generar combinaciones basadas en diferentes hipótesis estadísticas
- **Educativo**: Demostrar conceptos de probabilidad y estadística aplicada

---

## 📊 Fundamentos Teóricos

### 1. Teoría de Probabilidad Básica

#### Espacio Muestral y Eventos

En un sorteo de lotería tipo Melate:
- **[Espacio muestral](https://es.wikipedia.org/wiki/Espacio_muestral) (Ω)**: Conjunto de todos los números posibles (1-56)
- **[Evento](https://es.wikipedia.org/wiki/Suceso_(probabilidad))**: Selección de 6 números sin reemplazo
- **[Cardinalidad](https://es.wikipedia.org/wiki/Cardinal_(matem%C3%A1ticas))**: [C(56,6)](https://es.wikipedia.org/wiki/Coeficiente_binomial) = 32,468,436 combinaciones posibles

La probabilidad de acertar una combinación específica es:

```
P(acertar) = 1 / C(56,6) ≈ 3.08 × 10⁻⁸
```

#### Distribución Uniforme Teórica

En un sistema de lotería perfectamente aleatorio, cada número debería tener la misma [**probabilidad**](https://es.wikipedia.org/wiki/Probabilidad) de ser seleccionado según una [**distribución uniforme discreta**](https://es.wikipedia.org/wiki/Distribuci%C3%B3n_uniforme_discreta):

```
P(número i) = 1/56 ≈ 1.786% por sorteo
```

### 2. Frecuencia Empírica vs. Probabilidad Teórica

#### Ley de los Grandes Números

La [**Ley de los Grandes Números**](https://es.wikipedia.org/wiki/Ley_de_los_grandes_n%C3%BAmeros) establece que cuando el número de experimentos (sorteos) tiende a infinito, la [frecuencia relativa](https://es.wikipedia.org/wiki/Frecuencia_estad%C3%ADstica) observada converge a la probabilidad teórica:

```
lim(n→∞) [f(x)/n] = P(x)
```

Donde:
- `f(x)` = frecuencia absoluta del número x
- `n` = número total de sorteos
- `P(x)` = probabilidad teórica (1/56)

#### Frecuencia Esperada

Para un conjunto de `n` sorteos con 6 números cada uno:

```
Frecuencia esperada = (n × 6) / 56
```

Con 9,027 sorteos:
```
Frecuencia esperada ≈ 967.43 apariciones por número
```

### 3. Desviación Estadística

#### Cálculo de Desviación

La [desviación](https://es.wikipedia.org/wiki/Desviaci%C3%B3n_(estad%C3%ADstica)) porcentual indica cuánto se aleja la frecuencia observada de la esperada:

```
Desviación (%) = [(Frecuencia observada - Frecuencia esperada) / Frecuencia esperada] × 100
```

#### Interpretación de la Desviación

- **Desviación > +10%**: Número "muy caliente" (🔥) - aparece significativamente más de lo esperado
- **Desviación +5% a +10%**: Número "caliente" (🌡️) - aparece moderadamente más
- **Desviación -5% a +5%**: Número "normal" (➡️) - se comporta según lo esperado
- **Desviación -10% a -5%**: Número "frío" (❄️) - aparece menos de lo esperado
- **Desviación < -10%**: Número "muy frío" (🧊) - aparece significativamente menos

---

## 🔬 Metodología de Análisis

### 1. Recolección y Preparación de Datos

#### Fuentes de Datos

- **Melate**: 4,135 sorteos históricos
- **Revancha**: 3,127 sorteos históricos
- **Revanchita**: 1,765 sorteos históricos
- **Total**: 9,027 sorteos analizados

#### Procesamiento de Datos

1. **Normalización**: Unificación de formatos de columnas (R1-R6)
2. **Validación**: Verificación de integridad (números en rango 1-56)
3. **Agregación**: Combinación de las tres fuentes en un dataset unificado
4. **Metadatos**: Extracción de timestamps de última actualización

### 2. Análisis de Frecuencias

#### Frecuencia Univariada

Conteo de apariciones individuales de cada número del 1 al 56:

```python
frecuencia[i] = Σ(apariciones del número i en todos los sorteos)
```

#### Frecuencia Bivariada (Pares)

Análisis de [co-ocurrencia](https://es.wikipedia.org/wiki/Matriz_de_coocurrencia) de pares de números usando [combinaciones](https://es.wikipedia.org/wiki/Combinaci%C3%B3n):

```python
para cada sorteo:
    para cada combinación de 2 números:
        incrementar contador[par]
```

Total de pares posibles por sorteo: C(6,2) = 15

#### Frecuencia Multivariada

Extensión del análisis a:
- **Tríadas**: C(6,3) = 20 combinaciones por sorteo
- **Cuartetos**: C(6,4) = 15 combinaciones por sorteo
- **Quintetos**: C(6,5) = 6 combinaciones por sorteo
- **Combinaciones completas**: 1 por sorteo

### 3. Análisis de Patrones

#### Detección de Repeticiones

Identificación de combinaciones completas que se han repetido exactamente:

```python
combinaciones_repetidas = {comb: frecuencia | frecuencia > 1}
```

Significado estadístico: En un sistema verdaderamente aleatorio, la probabilidad de repetir una combinación exacta es extremadamente baja (≈3.08×10⁻⁸).

#### Análisis de Distribución

Examen de la distribución espacial de números:
- **Rango bajo** (1-18): ¿Proporción adecuada?
- **Rango medio** (19-37): ¿Comportamiento esperado?
- **Rango alto** (38-56): ¿Subrepresentación significativa?

---

## 🎯 Estrategias de Selección

### 1. Estrategia Híbrida (📋)

#### Fundamento Teórico

Combina dos enfoques complementarios:

1. **Explotación de sesgos potenciales**: Selecciona números frecuentes que podrían indicar sesgos mecánicos
2. **Cobertura aleatoria**: Incluye números aleatorios para evitar [sobreajuste](https://es.wikipedia.org/wiki/Sobreajuste) a patrones espurios

#### Algoritmo

```text
PARA cada combinación:
    seleccionar 4 números de los 30 más frecuentes
    seleccionar 2 números aleatorios del conjunto completo
    ordenar y retornar combinación
```

#### Justificación

Esta estrategia representa un **compromiso pragmático** entre dos escenarios:
- **Si existe sesgo real**: Los 4 números frecuentes capturan parte de esa ventaja
- **Si el sistema es aleatorio**: Los 2 números aleatorios proporcionan diversificación

Es una aproximación de [**teoría de carteras**](https://es.wikipedia.org/wiki/Teor%C3%ADa_de_carteras) aplicada a la incertidumbre epistémica: no sabemos con certeza si hay sesgo, por lo que diversificamos nuestra apuesta.

### 2. Estrategia Conservadora (🔥)

#### Fundamento Teórico

Basada en la **hipótesis de [sesgo sistemático](https://es.wikipedia.org/wiki/Sesgo_estad%C3%ADstico)**: Si las frecuencias observadas muestran desviaciones consistentes, esto podría indicar sesgos mecánicos o físicos en el sistema de sorteo, no mera variación aleatoria.

#### Algoritmo

```
PARA cada combinación:
    seleccionar 6 números de los 20 más frecuentes
    ordenar y retornar combinación
```

#### Justificación Estadística

Aunque la teoría de probabilidad indica [independencia entre sorteos](https://es.wikipedia.org/wiki/Sucesos_independientes), en la práctica los sistemas físicos pueden presentar:
- **Sesgos de fabricación**: Bolas con densidades o tamaños ligeramente diferentes
- **Desgaste diferencial**: Deterioro no uniforme del equipo a lo largo del tiempo
- **Factores ambientales**: Temperatura, humedad que afectan ciertos materiales

Esta estrategia **no asume** que el pasado predice el futuro en un sentido causal, sino que **detecta y explota** posibles sesgos persistentes del mecanismo físico. Si el sistema fuera perfectamente aleatorio, esta estrategia no tendría ventaja sobre selección aleatoria.

### 3. Estrategia Contrarian (🧊)

#### Fundamento Teórico

Basada en la [**Regresión a la media**](https://es.wikipedia.org/wiki/Regresi%C3%B3n_a_la_media) (Regression to the Mean):

```
lim(n→∞) [X̄ₙ] = μ
```

Donde X̄ₙ es la [media muestral](https://es.wikipedia.org/wiki/Media_aritm%C3%A9tica) y μ es la [media poblacional](https://es.wikipedia.org/wiki/Esperanza_matem%C3%A1tica).

#### Algoritmo

```
PARA cada combinación:
    seleccionar 6 números de los 15 menos frecuentes
    ordenar y retornar combinación
```

#### Justificación

Si el sistema es verdaderamente aleatorio, los números "fríos" eventualmente deben converger a la frecuencia esperada. Esta estrategia apuesta a la compensación estadística.

#### Advertencia

Esta estrategia asume que:
1. El sistema es perfectamente aleatorio (no hay sesgo persistente)
2. Hay tiempo suficiente para la reversión
3. Los sesgos observados son puramente [estocásticos](https://es.wikipedia.org/wiki/Proceso_estoc%C3%A1stico)

### 4. Estrategia Balanceada (⚖️)

#### Fundamento Teórico

Diversificación de riesgo mediante **[teoría de carteras](https://es.wikipedia.org/wiki/Teor%C3%ADa_de_carteras)** (portfolio theory):

```
Riesgo_total = w₁·Riesgo_calientes + w₂·Riesgo_fríos
```

Donde w₁ = w₂ = 0.5 (ponderación igual)

#### Algoritmo

```
PARA cada combinación:
    seleccionar 3 números de los 15 más frecuentes
    seleccionar 3 números de los 12 menos frecuentes
    ordenar y retornar combinación
```

#### Justificación

Esta estrategia no asume ninguna hipótesis específica, sino que distribuye la probabilidad entre ambas teorías (persistencia y reversión).

### 5. Estrategia Serendipity (✨)

#### Fundamento Teórico

Basada en **diversificación de estrategias** y **[teoría de decisiones](https://es.wikipedia.org/wiki/Teor%C3%ADa_de_la_decisi%C3%B3n) bajo [incertidumbre](https://es.wikipedia.org/wiki/Incertidumbre)**.

#### Algoritmo

```
PARA cada combinación:
    estrategia = selección_aleatoria([Híbrida, Conservadora, Contrarian, Balanceada])
    aplicar estrategia seleccionada
    ordenar y retornar combinación con etiqueta de estrategia
```

#### Justificación Epistemológica

Dado que no podemos conocer con certeza qué hipótesis es correcta ([epistemología](https://es.wikipedia.org/wiki/Epistemolog%C3%ADa)):

1. ¿El sistema tiene sesgo? → Conservadora
2. ¿El sistema es aleatorio? → Contrarian
3. ¿No sabemos? → Híbrida o Balanceada

La estrategia Serendipity implementa un **meta-enfoque** que cubre todas las posibilidades simultáneamente.

#### El Meta-Enfoque Explicado

Un **meta-enfoque** (estrategia sobre estrategias) se basa en los siguientes principios:

1. **[Incertidumbre del modelo](https://es.wikipedia.org/wiki/Incertidumbre_del_modelo)**: No sabemos cuál modelo del mundo es correcto
   - Modelo A: El sistema tiene sesgo persistente (favorece Conservadora)
   - Modelo B: El sistema es aleatorio y se regresará a la media (favorece Contrarian)
   - Modelo C: Incertidumbre total (favorece Híbrida/Balanceada)

2. **[Promedio de modelos](https://en.wikipedia.org/wiki/Ensemble_learning) (Model Averaging)**: En lugar de apostar todo a un solo modelo, distribuimos probabilidad entre varios
   ```
   P(éxito) = Σ P(éxito | Modelo_i) × P(Modelo_i)
   ```
   
   Donde P(Modelo_i) es nuestra confianza en cada modelo.

3. **Robustez ante errores de especificación**: 
   - Si elegimos la estrategia incorrecta, perdemos completamente
   - Con meta-enfoque, siempre tenemos exposición parcial a la estrategia correcta
   - Reduce el [riesgo de modelo](https://es.wikipedia.org/wiki/Riesgo_de_modelo)

4. **Analogía con [aprendizaje por ensamble](https://es.wikipedia.org/wiki/M%C3%A9todos_de_conjunto)**:
   - En machine learning, combinar múltiples modelos (ensemble) supera a modelos individuales
   - Random Forest combina múltiples árboles de decisión
   - Serendipity combina múltiples estrategias de selección

5. **Exploración continua**:
   - Cada ejecución explora diferentes regiones del espacio de soluciones
   - Evita el [sesgo de confirmación](https://es.wikipedia.org/wiki/Sesgo_de_confirmaci%C3%B3n) hacia una sola hipótesis
   - Mantiene diversidad en el portfolio de combinaciones

#### Ejemplo Numérico

Si generamos 5 combinaciones con Serendipity y la distribución aleatoria resulta:
- 2 combinaciones → Híbrida (40%)
- 1 combinación → Conservadora (20%)
- 1 combinación → Contrarian (20%)
- 1 combinación → Balanceada (20%)

Entonces estamos **distribuyendo nuestro riesgo** proporcionalmente entre todas las hipótesis, sin comprometer todo nuestro capital intelectual en una sola teoría del sistema.

#### Fundamento en Teoría de Decisiones

Este enfoque se relaciona con el **[Criterio de Laplace](https://es.wikipedia.org/wiki/Criterio_de_Laplace)** (principio de razón insuficiente): cuando no tenemos información para preferir una hipótesis sobre otra, debemos asignar probabilidades iguales a todas las posibilidades.

---

## 📈 Interpretación de Resultados

### 1. Significancia Estadística

#### Prueba de Hipótesis Implícita

**[Hipótesis nula](https://es.wikipedia.org/wiki/Hip%C3%B3tesis_nula) (H₀)**: La lotería es perfectamente aleatoria
```
H₀: P(número i) = 1/56 para todo i ∈ [1,56]
```

**Hipótesis alternativa (H₁)**: Existe sesgo en la distribución
```
H₁: ∃i tal que P(número i) ≠ 1/56
```

#### Criterio de Decisión

Con un [nivel de confianza](https://es.wikipedia.org/wiki/Nivel_de_confianza) del 95%, usamos desviaciones >±10% como indicador de posible sesgo significativo.

### 2. Limitaciones del Análisis Frecuentista

#### Falacia del Jugador (Gambler's Fallacy)

La [**Falacia del jugador**](https://es.wikipedia.org/wiki/Falacia_del_jugador) (Gambler's Fallacy) es un **error conceptual**: Creer que eventos pasados influyen en eventos futuros independientes.

**Ejemplo**: "El número 24 ha salido mucho, debe dejar de salir pronto" (INCORRECTO)

**Realidad**: Si el sistema es verdaderamente aleatorio:
```
P(número 24 en sorteo n+1) = 1/56
```
independientemente de su frecuencia histórica.

#### Independencia de Eventos

En teoría de probabilidad, cada sorteo constituye un **evento independiente**. Dos eventos A y B son independientes si y solo si:

```
P(A ∩ B) = P(A) · P(B)
```

**Referencias académicas:**

- Ross, S. (2014). *A first course in probability* (9th ed., pp. 110-125). Pearson Education. Define formalmente: "Events E and F are said to be independent if P(E ∩ F) = P(E)P(F)."

- Feller, W. (1968). *An introduction to probability theory and its applications* (Vol. 1, 3rd ed., pp. 114-148). John Wiley & Sons. Texto clásico que establece: "Events are independent if the occurrence of one does not affect the probability of the other."

- Kolmogorov, A. N. (1950). *Foundations of the theory of probability* (N. Morrison, Trans.). Chelsea Publishing Company. (Trabajo original publicado en 1933). Define axiomáticamente la independencia como condición fundamental de la teoría moderna de probabilidad.

**Implicación práctica:** En un sistema de lotería verdaderamente aleatorio, la historia **NO predice el futuro**. El resultado del sorteo n no influye en el sorteo n+1. Esta es la razón fundamental por la cual la [Falacia del jugador](https://es.wikipedia.org/wiki/Falacia_del_jugador) es un error lógico.

### 3. ¿Cuándo el Análisis Es Válido?

El análisis histórico solo es predictivo si:

1. **Existe sesgo mecánico persistente**
   - Bolas con peso diferente
   - Mecanismo de selección imperfecto
   - Deterioro no uniforme del equipo

2. **El sesgo es estable en el tiempo**
   - No se reemplazan las bolas
   - No se cambia el mecanismo
   - Condiciones ambientales constantes

3. **El tamaño de muestra es suficiente**
   - 9,027 sorteos × 6 números = 54,162 observaciones
   - Con 56 números: ~967 observaciones por número (suficiente)

---

## ⚠️ Limitaciones y Consideraciones Éticas

### Limitaciones Metodológicas

#### 1. Sesgo de Confirmación

El [**sesgo de confirmación**](https://es.wikipedia.org/wiki/Sesgo_de_confirmaci%C3%B3n): Los humanos tendemos a recordar los aciertos y olvidar los fallos, generando una percepción distorsionada de la efectividad de estrategias.

#### 2. Data Snooping Bias

Al analizar datos históricos para crear estrategias, existe riesgo de **[sobreajuste](https://es.wikipedia.org/wiki/Sobreajuste)** (overfitting): las estrategias funcionan en datos históricos pero fallan en datos futuros.

#### 3. Cambios en el Sistema

Si la lotería cambia su equipo o procedimientos, todo el análisis histórico pierde validez.

### Consideraciones Éticas

#### Juego Responsable

1. **Establecer límites**: Nunca gastar más de lo que se puede permitir perder
2. **Reconocer probabilidades**: Entender que ganar es extremadamente improbable
3. **Propósito educativo**: Este análisis es principalmente una herramienta de aprendizaje estadístico

#### Transparencia

```
⚠️ ADVERTENCIA IMPORTANTE:
```

> Este análisis NO garantiza ganancias. La lotería es un juego de azar con probabilidades extremadamente bajas de ganar. Las estrategias presentadas son ejercicios académicos de estadística aplicada y NO deben interpretarse como sistemas garantizados de ganancia.

#### Valores Esperados

El **[valor esperado](https://es.wikipedia.org/wiki/Valor_esperado)** de jugar a la lotería es típicamente negativo:

```
E[Valor] = P(ganar) × Premio - Costo_boleto
```

Para Melate:
```
E[Valor] ≈ (1/32,468,436) × $100,000,000 - $13 ≈ -$9.92
```

**Conclusión**: En promedio, se pierden ~$10 por boleto.

---

## 📚 Referencias y Lecturas Recomendadas

### Libros de Texto

Ross, S. (2014). *A first course in probability* (9th ed.). Pearson Education.
- Capítulos 1-3: Fundamentos de probabilidad
- Capítulo 3: "Conditional Probability and Independence" (pp. 110-125)
- Capítulo 8: Ley de grandes números

Feller, W. (1968). *An introduction to probability theory and its applications* (Vol. 1, 3rd ed.). John Wiley & Sons.
- Capítulo V: "Conditional Probability. Stochastic Independence" (pp. 114-148)
- Texto clásico y fundamental en teoría de probabilidad

Kolmogorov, A. N. (1950). *Foundations of the theory of probability* (N. Morrison, Trans.). Chelsea Publishing Company. (Trabajo original publicado en 1933)
- Obra fundacional que establece los axiomas modernos de la probabilidad
- Definición axiomática de independencia

Hogg, R. V., Tanis, E. A., & Zimmerman, D. L. (2015). *Probability and statistical inference* (9th ed.). Pearson Education.
- Capítulo 4: Distribuciones discretas
- Capítulo 7: Estimación puntual

Wasserman, L. (2004). *All of statistics: A concise course in statistical inference*. Springer.
- Capítulo 3: Inferencia estadística
- Capítulo 11: Análisis de datos exploratorios

### Artículos y Libros de Divulgación

Nahin, P. J. (2000). *Duelling idiots and other probability puzzlers*. Princeton University Press.
- Discusión sobre falacias probabilísticas comunes

Mlodinow, L. (2008). *The drunkard's walk: How randomness rules our lives*. Pantheon Books.
- Percepción humana de la aleatoriedad

Taleb, N. N. (2007). *The black swan: The impact of the highly improbable*. Random House.
- Eventos raros y predicción estadística

### Recursos en Línea

Khan Academy. (s.f.). *Probability and statistics*. Khan Academy. Recuperado de https://www.khanacademy.org/math/statistics-probability

MIT OpenCourseWare. (s.f.). *Introduction to probability and statistics*. Massachusetts Institute of Technology. Recuperado de https://ocw.mit.edu/courses/mathematics/

Hájek, A. (2019). Interpretations of probability. En E. N. Zalta (Ed.), *The Stanford encyclopedia of philosophy* (Fall 2019 ed.). Stanford University. https://plato.stanford.edu/entries/probability-interpret/

### Conceptos Clave para Estudio Adicional

- **[Teorema de Bayes](https://es.wikipedia.org/wiki/Teorema_de_Bayes)**: Actualización de probabilidades con nueva información
- **[Distribución binomial](https://es.wikipedia.org/wiki/Distribuci%C3%B3n_binomial)**: Modelo para eventos de éxito/fracaso
- **[Test χ² (chi-cuadrado)](https://es.wikipedia.org/wiki/Prueba_%CF%87%C2%B2)**: Prueba de bondad de ajuste para distribuciones
- **[Simulación Monte Carlo](https://es.wikipedia.org/wiki/M%C3%A9todo_de_Montecarlo)**: Método computacional para estimación probabilística
- **[Teorema del límite central](https://es.wikipedia.org/wiki/Teorema_del_l%C3%ADmite_central)**: Distribución de medias muestrales
- **[Proceso estocástico](https://es.wikipedia.org/wiki/Proceso_estoc%C3%A1stico)**: Secuencias de eventos aleatorios
- **[Entropía](https://es.wikipedia.org/wiki/Entrop%C3%ADa_(informaci%C3%B3n))**: Medida de incertidumbre en sistemas aleatorios
- **[Regresión a la media](https://es.wikipedia.org/wiki/Regresi%C3%B3n_a_la_media)**: Fenómeno estadístico natural

---

## 🔍 Glosario de Términos

| Término | Definición |
|:--------|:-----------|
| **[Espacio muestral](https://es.wikipedia.org/wiki/Espacio_muestral) (Ω)** | Conjunto de todos los resultados posibles de un experimento |
| **[Evento](https://es.wikipedia.org/wiki/Suceso_(probabilidad))** | Subconjunto del espacio muestral |
| **Probabilidad empírica** | Frecuencia relativa observada en experimentos |
| **Probabilidad teórica** | Probabilidad calculada bajo supuestos matemáticos |
| **[Independencia](https://es.wikipedia.org/wiki/Sucesos_independientes)** | Dos eventos son independientes si P(A∩B) = P(A)·P(B) |
| **[Valor esperado](https://es.wikipedia.org/wiki/Valor_esperado)** | Media ponderada de todos los resultados posibles |
| **[Desviación estándar](https://es.wikipedia.org/wiki/Desviaci%C3%B3n_t%C3%ADpica)** | Medida de dispersión respecto a la media |
| **[Sesgo](https://es.wikipedia.org/wiki/Sesgo_estad%C3%ADstico)** | Desviación sistemática de un valor esperado |
| **[Aleatorio](https://es.wikipedia.org/wiki/Aleatoriedad)** | Proceso sin patrón predecible |
| **[Sobreajuste](https://es.wikipedia.org/wiki/Sobreajuste)** (Overfitting) | Modelo que se ajusta demasiado a datos históricos |

---

## 📞 Contacto y Contribuciones

Este análisis es un proyecto de código abierto. Se aceptan contribuciones, sugerencias y correcciones:

- **Repositorio**: [github.com/mariotristan/melate](https://github.com/mariotristan/melate)
- **Issues**: Para reportar errores o sugerir mejoras
- **Pull Requests**: Para contribuir con código o documentación

---

## 📄 Licencia y Uso Académico

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

**Resumen de permisos:**
- ✅ Uso comercial
- ✅ Modificación
- ✅ Distribución
- ✅ Uso privado

**Condiciones:**
- Incluir aviso de copyright y licencia en copias
- Sin garantía: el software se proporciona "tal cual"

**Uso académico:** Se permite y fomenta el uso en contextos educativos. Al citar este trabajo, incluye:

```
Tristan, M. (2025). Análisis estadístico de lotería Melate [Software]. 
GitHub. https://github.com/mariotristan/melate
```

**Última actualización**: Noviembre 2025

---

> **Nota Final**: La estadística es una herramienta poderosa para comprender el mundo, pero debe usarse con responsabilidad y comprensión de sus limitaciones. Este análisis es un ejercicio educativo en estadística aplicada, no una estrategia de inversión o un sistema de ganancias garantizadas.

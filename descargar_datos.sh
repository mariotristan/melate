#!/bin/bash
# Descarga todos los archivos de datos de loterías mexicanas
# Ejecuta este script desde la raíz del proyecto

set -e

## URLs extraídas de los pipelines (workflows YAML)
MELATE_URL="https://www.loterianacional.gob.mx/Home/Historicos?ARHP=TQBlAGwAYQB0AGUA"
REVANCHA_URL="https://www.loterianacional.gob.mx/Home/Historicos?ARHP=UgBlAHYAYQBuAGMAaABhAA=="
REVANCHITA_URL="https://www.loterianacional.gob.mx/Home/Historicos?ARHP=UgBlAHYAYQBuAGMAaABpAHQAYQA="
RETRO_URL="https://www.loterianacional.gob.mx/Home/Historicos?ARHP=TQBlAGwAYQB0AGUALQBSAGUAdAByAG8A"
TRIS_URL="https://www.loterianacional.gob.mx/Home/Historicos?ARHP=VAByAGkAcwA="

# Descarga cada archivo
curl -k -L "$MELATE_URL" -o Melate.csv
curl -k -L "$REVANCHA_URL" -o Revancha.csv
curl -k -L "$REVANCHITA_URL" -o Revanchita.csv
curl -k -L "$RETRO_URL" -o MelateRetro.csv
curl -k -L "$TRIS_URL" -o Tris.csv

echo "Descarga completa. Archivos guardados en la raíz del proyecto."

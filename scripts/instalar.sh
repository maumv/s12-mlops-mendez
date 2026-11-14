#!/usr/bin/env bash
# Instala el entorno de producción: las versiones exactas con que se entrenó el modelo
# (modelo/requirements.txt, exportado desde Colab) más las librerías de la app.
cd "$(dirname "$0")/.."
if [ ! -f modelo/requirements.txt ]; then
  echo "⚠  No existe modelo/requirements.txt."
  echo "   Suba la carpeta 'modelo' al repositorio (Parte 4 del notebook) y ejecute: bash scripts/instalar.sh"
  exit 0
fi
pip install --no-cache-dir -r modelo/requirements.txt -r requirements.txt
echo "✔ Entorno de producción instalado. Inicie la app con: python app.py"

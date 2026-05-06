#!/usr/bin/env sh

# Crea un entorno virtual en .venv usando python3 (o python si no existe)
if command -v python3 >/dev/null 2>&1; then
  python3 -m venv .venv
else
  python -m venv .venv
fi

# Activa el entorno dentro del script e instala las dependencias
# Nota: activar dentro del script solo afecta al proceso del script; el entorno quedará creado y las librerías instaladas.
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Entorno virtual creado en .venv. Para activarlo en tu shell ejecuta: source .venv/bin/activate"

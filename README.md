# recon-sniffer

Toolkit de reconocimiento y captura de paquetes (Scapy). Diseñado para ejercicios controlados, análisis y pruebas en entornos autorizados.

Objetivo
- Proveer scripts y artefactos reproducibles para capturas y análisis de red con un enfoque educativo/práctico.

Quickstart (3 pasos)
1. Clona el repo y sitúate en la raíz del proyecto:
   - git clone https://github.com/Jerimy2021/recon-sniffer.git
   - cd recon-sniffer
2. Crea el entorno virtual e instala dependencias:
   - sh setup_venv.sh
   - source .venv/bin/activate
3. Ejecuta el script principal de reconocimiento (requiere permisos de captura):
   - sudo python 01_Reconnaissance/recon_advanced.py

Estructura (alto nivel)
```README.md#L1-20
recon-sniffer/
├─ 01_Reconnaissance/
│  ├─ recon_advanced.py
│  └─ capturas_pantalla/
├─ 02_Exploitation/
├─ 03_Report/
├─ simulador_grupo1.py
├─ requirements.txt
├─ setup_venv.sh
├─ .gitignore
└─ .github/branch_protection.json
```

Desarrollo (GitFlow - resumen ejecutivo)
- Branches principales:
  - `develop` — rama por defecto para integración diaria.
  - `main` — rama protegida; solo recibe releases vía PR.
- Branches de trabajo:
  - `feature/<name>`: crear desde `develop`; abrir PR contra `develop`.
  - `release/<version>`: preparar release; abrir PR a `main`.
  - `hotfix/<name>`: ramas creadas desde `main` para correcciones críticas; PR a `main` y luego a `develop`.
- Reglas recomendadas: no push directo a `main`; PRs con 1+ reviews; CI checks required antes de mergear a `main`.

Protección y configuración
- La configuración de protección de rama se almacena en `.github/branch_protection.json` (mejor práctica: no dejar metadatos de repo en la raíz).
- Para aplicar/actualizar la protección puedes usar `gh api` o la API REST de GitHub con un token con permisos adecuados.

Contribución (mínimo):
- Crear `feature/<name>` desde `develop`.
- Realizar cambios y push a la rama remota.
- Abrir PR contra `develop`, describir el cambio y asignar revisores.

Seguridad / notas operativas
- Capturar tráfico requiere permisos (p. ej. `sudo`).
- No usar las herramientas en redes sin autorización expresa.
- Evitar incluir credenciales o tokens en el repositorio.

Licencia
- MIT

---

Cambios en esta rama
- README.md reducido y centrado en un resumen ejecutivo, corregidas rutas y ejemplo de uso para `01_Reconnaissance/recon_advanced.py`.

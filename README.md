# recon-sniffer

Repositorio para un pequeño conjunto de herramientas de reconocimiento y captura de paquetes basadas en Scapy.

Este proyecto sigue un flujo de trabajo basado en GitFlow: la rama por defecto es `develop` (trabajo diario), `main` está protegida y recibe solo cambios mediante Pull Requests y releases.

Tabla de contenidos
- [Visión general](#visión-general)
- [Arquitectura y estructura de carpetas](#arquitectura-y-estructura-de-carpetas)
- [Instalación y entorno](#instalación-y-entorno)
- [Uso](#uso)
- [Flujo de trabajo (GitFlow)](#flujo-de-trabajo-gitflow)
- [Cambios incluidos en esta feature](#cambios-incluidos-en-esta-feature)
- [Seguridad y permisos](#seguridad-y-permisos)
- [Contribución](#contribución)
- [Licencia](#licencia)

Visión general
-----------

`recon-sniffer` es un repo didáctico y práctico para capturas de red y actividades de reconocimiento con `scapy`. Incluye un ejemplo de sniffer (`recon_advanced.py`), utilidades para gestionar el entorno virtual y un README con guía de arquitectura y GitFlow.

Arquitectura y estructura de carpetas
-----------------------------------

La organización del proyecto está pensada para equipos y ejercicios por fases:

- `01_Reconnaissance/` — Scripts y artefactos para reconocimiento y captura.
- `02_Exploitation/` — Herramientas y exploits (si aplica).
- `03_Report/` — Templates y salidas de reporte.
- Archivos en la raíz:
  - `simulador_grupo1.py` — script de simulación (ejemplo).
  - `requirements.txt` — dependencias del proyecto.
  - `setup_venv.sh` — script para crear el entorno virtual e instalar dependencias.
  - `.gitignore` — reglas para ignorar artefactos locales.
  - `protection.json` — (metadatos) configuración aplicada para protección de rama `main`.

Ejemplo de árbol:

```README.md#L1-25
recon-sniffer/
├─ 01_Reconnaissance/
├─ 02_Exploitation/
├─ 03_Report/
├─ simulador_grupo1.py
├─ requirements.txt
├─ setup_venv.sh
├─ .gitignore
└─ README.md
```

Instalación y entorno
---------------------

Prerequisitos:
- Python 3.8+
- pip
- (Linux) `libpcap` y headers (p. ej. `libpcap-dev`) para soporte Npcap/libpcap si instalas scapy desde fuentes.

Forma recomendada (script automatizado):

```/dev/null/usage.sh#L1-4
cd /path/to/recon-sniffer
sh setup_venv.sh
source .venv/bin/activate
```

Si quieres hacerlo manualmente:

```/dev/null/usage_manual.sh#L1-4
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Uso
---

Ejecutar el sniffer de ejemplo (requiere permisos de captura - normalmente `sudo` en macOS/Linux):

```/dev/null/run_sniffer.sh#L1-2
source .venv/bin/activate
sudo python recon_sniffer.py
```

El sniffer imprime un resumen simple por paquete IP/TCP y muestra parte del `payload` si existe.

Flujo de trabajo (GitFlow)
-------------------------

Política de ramas y convenciones (resumen):
- `develop` — rama por defecto; aquí se integran feature branches.
- `feature/*` — ramas de trabajo originadas desde `develop`. Ejemplo: `feature/update-readme-architecture`.
- `release/*` — preparan una release a `main` (versionado, pruebas, CI).
- `hotfix/*` — correcciones urgentes directamente desde `main` y luego se mergean a `develop`.
- `main` — rama protegida. Solo se actualiza mediante PRs y releases aprobados.

Comandos típicos (ejemplos):

Crear y trabajar en una feature branch:

```/dev/null/git-feature.sh#L1-6
git fetch origin
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
# trabajar, añadir cambios
git add .
git commit -m "feat: descripción corta"
git push -u origin feature/my-feature
# abrir PR contra develop (usa gh o la UI)
gh pr create --base develop --head feature/my-feature --title "feat: descripción" --body "Detalles..."
```

Preparar una release (merge a `main` vía PR):

```/dev/null/git-release.sh#L1-6
git checkout develop
git pull origin develop
git checkout -b release/1.0.0
# Ajustes, bump de versión, tests
git push -u origin release/1.0.0
gh pr create --base main --head release/1.0.0 --title "release: 1.0.0" --body "Notas de release"
# Una vez aprobado, mergear y taggear
```

Notas:
- `main` está protegida: requiere al menos 1 aprobación y no permite force-push ni delete.
- Recomendado: tener checks de CI (GitHub Actions) que sean required_status_checks antes de mergear a `main`.

Cambios incluidos en esta feature
---------------------------------

- Actualización/expansión del `README.md` para documentar arquitectura y flujo de trabajo.
- Documentación del layout de carpetas y comandos recomendados.
- Registro de los artefactos ya añadidos al repo: `recon_sniffer.py`, `setup_venv.sh`, `requirements.txt`, `.gitignore`, `protection.json`.

Seguridad y permisos
--------------------

- El sniffing de paquetes requiere permisos de administrador (p. ej. `sudo`).
- No ejecutes sniffers en redes donde no tengas autorización explícita.
- Evita almacenar tokens/credenciales en texto plano en el repo. Usa `gh auth login` o variables de entorno para CI.

Contribución
------------

1. Crea una `feature/<nombre>` desde `develop`.
2. Haz cambios y push a tu rama.
3. Abre un Pull Request contra `develop` y pide revisión.
4. Tras la revisión y aprobación, el PR se puede mergear a `develop`.
5. Para publicar en `main`, crea una rama `release/*` desde `develop` y abre PR a `main`.

Licencia
--------

MIT

---

Si quieres, en esta misma feature puedo:
- Añadir un template de Pull Request y/o un workflow básico de GitHub Actions (lint y tests) y configurarlo para que sea un `required_status_check` en la protección de `main`.
- Crear la PR desde esta rama hacia `develop` (ya lo hice automáticamente).


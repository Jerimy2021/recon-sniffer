# recon-sniffer

Repositorio para un pequeño conjunto de herramientas de reconocimiento y captura de paquetes basadas en Scapy.

Este proyecto sigue un flujo de trabajo basado en GitFlow: la rama por defecto es `develop` (trabajo diario), `main` está protegida y recibe solo cambios mediante Pull Requests y releases.

Tabla de contenidos
- [Visión general](#visión-general)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación y entorno](#instalación-y-entorno)
- [Uso](#uso)
- [Flujo de trabajo (GitFlow) - Estándar](#flujo-de-trabajo-gitflow---estándar)
- [Protección de ramas y configuración](#protección-de-ramas-y-configuración)
- [Contribución](#contribución)
- [Licencia](#licencia)

Visión general
--------------

`recon-sniffer` es un repositorio didáctico y práctico para captures de red y actividades de reconocimiento con `scapy`. Incluye ejemplos de sniffers, utilidades para gestionar el entorno virtual y material de apoyo para ejercicios.

Estructura del proyecto
-----------------------

La organización del proyecto está pensada para ejercicios por fases y para facilitar el trabajo en equipo siguiendo GitFlow.

- `01_Reconnaissance/` — Scripts y artefactos de reconocimiento.
  - `recon_advanced.py` — script avanzado de reconocimiento y captura.
  - `capturas_pantalla/` — capturas de ejemplo usadas en las prácticas.
- `02_Exploitation/` — Herramientas y pruebas relacionadas con explotación (si aplica).
- `03_Report/` — Plantillas y salidas para informes.

Archivos en la raíz:
- `recon_sniffer.py` — sniffer mínimo con Scapy (ejemplo rápido en la raíz).
- `simulador_grupo1.py` — script de simulación (ejemplo).
- `requirements.txt` — dependencias del proyecto.
- `setup_venv.sh` — script para crear el entorno virtual e instalar dependencias.
- `.gitignore` — reglas para ignorar artefactos locales.
- `.github/branch_protection.json` — configuración almacenada de protección (se movió desde la raíz a `.github/` por buenas prácticas).

Ejemplo de árbol:

```README.md#L1-30
recon-sniffer/
├─ 01_Reconnaissance/
│  ├─ recon_advanced.py
│  └─ capturas_pantalla/
├─ 02_Exploitation/
├─ 03_Report/
├─ recon_sniffer.py
├─ simulador_grupo1.py
├─ requirements.txt
├─ setup_venv.sh
├─ .gitignore
└─ .github/branch_protection.json
```

Instalación y entorno
---------------------

Prerequisitos:
- Python 3.8+
- pip
- (Linux) `libpcap` y headers (p. ej. `libpcap-dev`) para soporte si es necesario.

Forma recomendada (script automatizado):

```README.md#L31-35
cd /path/to/recon-sniffer
sh setup_venv.sh
source .venv/bin/activate
```

Si quieres hacerlo manualmente:

```README.md#L36-40
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Uso
---

Ejecutar el sniffer de ejemplo (requiere permisos de captura - normalmente `sudo` en macOS/Linux):

```README.md#L41-44
source .venv/bin/activate
sudo python recon_sniffer.py
```

Para ejecutar el script avanzado de la carpeta `01_Reconnaissance`:

```README.md#L45-47
source .venv/bin/activate
sudo python 01_Reconnaissance/recon_advanced.py
```

Flujo de trabajo (GitFlow) - Estándar
------------------------------------

Ramas principales:
- `main` — rama de producción (protegida). Solo se actualiza mediante Pull Requests tras pasar las revisiones y checks.
- `develop` — rama de integración y desarrollo; rama por defecto del repositorio.

Ramas de soporte:
- `feature/<nombre>` — nuevas funcionalidades. Se crean desde `develop` y se mergean de vuelta a `develop`.
- `release/<version>` — preparación de una versión para `main`. Se crean desde `develop`, tras pruebas se hace PR a `main` y luego se mergea a `develop`.
- `hotfix/<nombre>` — corrección urgente en `main`. Se crean desde `main`, se mergean a `main` y `develop`.
- `bugfix/<nombre>` — correcciones menores (opcionalmente puede usarse `feature/` en su lugar).

Convenciones y pasos típicos:

- Crear una feature:

```README.md#L48-58
git fetch origin
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
# trabajar en la feature
git add .
git commit -m "feat: descripción corta"
git push -u origin feature/my-feature
# abrir PR contra develop (usar la UI o `gh`)
gh pr create --base develop --head feature/my-feature --title "feat: ..." --body "Detalles..."
```

- Preparar una release:

```README.md#L59-66
git checkout develop
git pull origin develop
git checkout -b release/1.0.0
# ajustar versiones, pruebas, documentación
git push -u origin release/1.0.0
# abrir PR a main, revisar y mergear; luego taggear y mergear a develop si es necesario
```

- Hotfix (urgente):

```README.md#L67-73
git checkout main
git pull origin main
git checkout -b hotfix/1.0.1
# corregir bug
git commit -am "fix: corrección urgente"
git push -u origin hotfix/1.0.1
# abrir PR a main; una vez mergeado, mergear a develop
```

Políticas recomendadas:
- No hacer push directo a `main`.
- Requerir al menos 1 aprobación en PRs hacia `main`.
- Tener checks de CI (GitHub Actions) que sean `required_status_checks` antes de mergear a `main`.
- Usar revisiones de código y etiquetas de PR para trackear calidad.

Protección de ramas y configuración
-----------------------------------

Buenas prácticas para archivos de configuración de repositorio:
- Archivos de configuración del repositorio (como plantillas, acciones de GitHub o metadatos de protección) deben almacenarse en `.github/` o en `docs/` en lugar de la raíz para mantener la raíz limpia.
- En este repositorio, `branch_protection.json` contiene la configuración usada para aplicar políticas a `main`. Se ha movido desde la raíz a `.github/branch_protection.json`.

Para (re)aplicar la configuración de protección de rama descrita en `.github/branch_protection.json` se puede usar la API de GitHub o `gh api`:

```README.md#L74-86
# Usando gh (ejecutar en tu máquina con gh autenticado):
gh api --method PUT /repos/$OWNER/$REPO/branches/main/protection --input .github/branch_protection.json -H "Accept: application/vnd.github+json"

# Usando curl (requiere GITHUB_TOKEN con permisos repo):
# export GITHUB_TOKEN=...
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d @.github/branch_protection.json
```

Contribución
------------

1. Crea una rama `feature/<nombre>` desde `develop`.
2. Haz cambios y push a tu rama.
3. Abre un Pull Request contra `develop` y solicita revisión.
4. Tras la revisión y aprobación, mergea a `develop`.
5. Para publicar en `main`, crea una rama `release/*` desde `develop` y abre PR a `main`.

Licencia
--------

MIT

---

Cambios incluidos en esta feature
- Corrección de rutas y referencias: `recon_advanced.py` se encuentra en `01_Reconnaissance/` y `capturas_pantalla/` contiene las capturas.
- Movida la configuración de protección de `protection.json` (raíz) a `.github/branch_protection.json` por buenas prácticas.
- Aclaraciones y estandarización del flujo GitFlow en el README.

# Recon Sniffer

Pequeño repositorio para un script de captura/recon usando Scapy.

Este repo contiene:

- `recon_sniffer.py`: script de ejemplo que captura paquetes con Scapy.
- `requirements.txt`: dependencias (Scapy y utilidades).
- `setup_venv.sh`: script para crear el entorno virtual e instalar dependencias.
- `.gitignore`

Estrategia de ramas y buenas prácticas

- `main`: rama protegida — solo contiene este `README.md` y documentación del proyecto.
- `develop`: rama de trabajo donde se añadirán y modificaran los scripts y código. Nada de código se pushea directamente a `main`.

Instalación rápida

Desde la raíz del repo:

1. Crear y activar entorno virtual:

   ```sh
   sh setup_venv.sh
   source .venv/bin/activate
   ```

2. Ejecutar el script (nota: se suelen necesitar permisos de administrador para capturar paquetes):

   ```sh
   sudo python recon_sniffer.py
   ```

Notas sobre seguridad y permisos

- El sniffing de red puede requerir permisos elevados (`sudo`). Ten cuidado con los permisos y con ejecutar código en entornos de producción.
- Usa este proyecto únicamente con autorización para capturar tráfico en la red objetivo.

Licencia

- MIT

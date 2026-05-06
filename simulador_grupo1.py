import time

import requests

print("Simulador Grupo 1 (Blue Team)")
print("[*] Simulador de Raspberry Pi (Tier 2) iniciado...")
print("[*] Lector de huellas Aegis activo. Simulando lecturas cada 5 segundos...\n")

# El lector consulta un endpoint interno (API) del servidor, no la web administrativa
url_falsa_backend = "http://127.0.0.1:5000/api/validate_access"

while True:
    try:
        # El hardware solo manda quién es él (sensor_id) y qué huella leyó (template_id)
        datos = {"sensor_id": "Aegis_Front_Door", "template_id": "42"}

        print(
            f"[*] Alguien puso el dedo. Enviando petición HTTP POST a {url_falsa_backend}..."
        )

        # Timeout corto porque el servidor real no existe en esta prueba
        response = requests.post(url_falsa_backend, data=datos, timeout=2)
        print(f"[*] Respuesta del servidor: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(
            "[!] El servidor central no responde (o no existe), pero el paquete ya viajó por la red."
        )

    time.sleep(5)

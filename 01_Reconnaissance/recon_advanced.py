#!/usr/bin/env python3
import argparse
import logging
import re
import sys
from dataclasses import dataclass
from typing import Callable, List, Optional

# Importaciones reales de red
from scapy.all import IP, TCP, Raw, sniff

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("NetworkRecon")


@dataclass
class TargetInfo:
    """Encapsula la información validada del objetivo descubierto."""

    ip_src: str
    ip_dst: str
    method: str
    path: str
    host: str
    body: str


class NetworkSniffer:
    """Maneja exclusivamente la captura de red, filtros BPF y delegación de eventos."""

    def __init__(
        self,
        interface: Optional[str],
        ports: List[int],
        on_target_found: Callable[[TargetInfo], None],
    ):
        self.interface = interface
        self.ports = ports
        self.on_target_found = on_target_found
        self._stop_sniffing = False
        self.buffer_http = ""
        self.temp_src = ""
        self.temp_dst = ""

    def _build_bpf_filter(self) -> str:
        """Construye un filtro BPF optimizado a nivel de kernel."""
        port_conditions = " or ".join([f"port {p}" for p in self.ports])
        return f"tcp and ({port_conditions})"

    def _packet_handler(self, packet):
        """Procesa el paquete de red. Extrae datos y delega mediante callback."""
        if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
            try:
                payload = packet[Raw].load.decode("utf-8", errors="ignore")

                # Si vemos tráfico web o nuestra huella, lo metemos a la memoria (buffer)
                if "HTTP/" in payload or "template_id" in payload:
                    # Guardamos las IPs del primer paquete
                    if "HTTP/" in payload:
                        self.temp_src = packet[IP].src
                        self.temp_dst = packet[IP].dst

                    self.buffer_http += payload

                    # ¿Ya llegó la parte de la huella? Si es así, terminamos el trabajo.
                    if "template_id" in self.buffer_http:
                        # Extraemos detalles del paquete YA ENSAMBLADO
                        method_match = re.search(
                            r"^(GET|POST)\s+([^\s]+)", self.buffer_http
                        )
                        host_match = re.search(
                            r"[Hh]ost:\s+([^\r\n]+)", self.buffer_http
                        )

                        method = method_match.group(1) if method_match else "UNKNOWN"
                        path = method_match.group(2) if method_match else "/"
                        host = host_match.group(1) if host_match else "UNKNOWN"

                        # Construimos el DTO con el paquete completo
                        target = TargetInfo(
                            ip_src=self.temp_src,
                            ip_dst=self.temp_dst,
                            method=method,
                            path=path,
                            host=host,
                            body=self.buffer_http,
                        )

                        # Delegamos al controlador para pasar a Fase II
                        self.on_target_found(target)

            except Exception as e:
                logger.debug(f"Error procesando paquete: {e}")

    def _should_stop(self, packet) -> bool:
        return self._stop_sniffing

    def stop(self):
        self._stop_sniffing = True

    def start(self, timeout: int):
        bpf_filter = self._build_bpf_filter()
        logger.info(
            f"Iniciando interfaz: {self.interface or 'Default'} | BPF: {bpf_filter}"
        )

        try:
            sniff(
                iface=self.interface,
                filter=bpf_filter,
                prn=self._packet_handler,
                store=0,
                stop_filter=self._should_stop,
                timeout=timeout,
            )
        except PermissionError:
            logger.critical(
                "Privilegios insuficientes. Ejecute como administrador/sudo."
            )
            sys.exit(1)
        except Exception as e:
            logger.critical(f"Fallo crítico en el adaptador de red: {e}")
            sys.exit(1)


class ReconController:
    """Orquesta las fases del ataque y gestiona el estado de los objetivos."""

    def __init__(self):
        self.sniffer: Optional[NetworkSniffer] = None
        self.target_acquired: Optional[TargetInfo] = None

    def handle_discovered_target(self, target: TargetInfo):
        logger.info(
            f"¡Objetivo detectado!: {target.ip_src} -> {target.ip_dst} | {target.method} {target.path}"
        )
        logger.warning(
            f"[*] ¡PAQUETE HTTP INTERCEPTADO EN TEXTO PLANO!:\n{target.body}"
        )
        self.target_acquired = target

        if self.sniffer:
            self.sniffer.stop()

    def execute_phase_two(self):
        if not self.target_acquired:
            logger.error("Se intentó iniciar la Fase II sin un objetivo válido.")
            return

        logger.info(
            f"Iniciando Fase II (Auth Bypass) contra la IP objetivo: {self.target_acquired.ip_dst}"
        )
        # AQUÍ PROGRAMARÁS LA INYECCIÓN SQL MÁS ADELANTE


def main():
    parser = argparse.ArgumentParser(description="Framework de Reconocimiento")
    parser.add_argument("-i", "--interface", help="Adaptador de red", default=None)
    parser.add_argument("-p", "--ports", help="Puertos", default="80,8080,5000")
    parser.add_argument("-t", "--timeout", help="Timeout", type=int, default=300)

    args = parser.parse_args()
    port_list = [int(p.strip()) for p in args.ports.split(",")]

    controller = ReconController()
    sniffer = NetworkSniffer(
        interface=args.interface,
        ports=port_list,
        on_target_found=controller.handle_discovered_target,
    )
    controller.sniffer = sniffer

    try:
        logger.info("--- Iniciando Fase I (Sniffing) ---")
        # NOTA PARA LA SIMULACIÓN LOCAL: Para que Scapy escuche paquetes enviados
        # en tu propia PC (localhost), en Windows a veces hay que pasarle la interfaz de loopback.
        # Si estás en Windows, pruébalo sin argumentos primero.
        sniffer.start(timeout=args.timeout)

        if controller.target_acquired:
            logger.info("--- Transición Exitosa ---")
            controller.execute_phase_two()
        else:
            logger.warning("No se detectó tráfico en el tiempo límite.")

    except KeyboardInterrupt:
        logger.info("Interrupción manual. Finalizando.")
        sys.exit(0)


if __name__ == "__main__":
    main()

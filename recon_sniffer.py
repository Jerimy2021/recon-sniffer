#!/usr/bin/env python3
"""
recon_sniffer.py
Ejemplo mínimo de sniffer usando scapy.

IMPORTANTE: Ejecutar con permisos adecuados (ej. sudo) si se capturan paquetes en interfaces del sistema.
"""

from scapy.all import sniff, IP, TCP, Raw


def packet_callback(pkt):
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        summary = f"{src} -> {dst} proto={pkt[IP].proto}"
        if TCP in pkt:
            summary += f" sport={pkt[TCP].sport} dport={pkt[TCP].dport}"
            if Raw in pkt:
                payload = bytes(pkt[Raw])
                summary += f" payload={payload[:200].hex()}"
        print(summary)


if __name__ == "__main__":
    print("Iniciando sniffer (CTRL-C para detener).")
    sniff(prn=packet_callback, store=False)

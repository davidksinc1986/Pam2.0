"""Sincronización programada de leads desde Meta Graph API.

Este script no simula resultados: si faltan credenciales o endpoint implementado,
falla explícitamente con instrucciones de configuración.
"""

from datetime import datetime
import os
import sys


def main() -> None:
    app_id = os.getenv("META_APP_ID", "").strip()
    app_secret = os.getenv("META_APP_SECRET", "").strip()
    access_token = os.getenv("META_ACCESS_TOKEN", "").strip()
    if not app_id or not app_secret or not access_token:
        print(
            f"[{datetime.utcnow().isoformat()}] ERROR: faltan META_APP_ID, META_APP_SECRET o META_ACCESS_TOKEN. "
            "Configura credenciales reales para sincronizar leads."
        )
        raise SystemExit(1)
    print(
        f"[{datetime.utcnow().isoformat()}] Credenciales Meta detectadas. "
        "Implementa la integración Graph API en este script antes de ejecutarlo en producción."
    )
    raise SystemExit(2)


if __name__ == "__main__":
    main()

"""
CEREBRO HEALTH
Sistema de diagnóstico de módulos.
"""

import time
import traceback


def check_module(module):
    """
    Comprueba un módulo sin detener CEREBRO.
    """

    result = {
        "name": module.name,
        "status": "UNKNOWN",
        "message": "",
        "time": time.time()
    }

    try:

        if not module.enabled:
            result["status"] = "DISABLED"
            result["message"] = "Módulo desactivado."
            return result

        if module.function is None:
            result["status"] = "READY"
            result["message"] = "Módulo registrado; esperando conexión."
            return result

        result["status"] = "ONLINE"
        result["message"] = "Módulo funcionando."

    except Exception as error:

        result["status"] = "ERROR"
        result["message"] = str(error)
        result["traceback"] = traceback.format_exc()

    return result


def scan_registry(registry):

    results = []

    for module in registry.modules.values():

        try:
            results.append(check_module(module))

        except Exception as error:

            results.append({
                "name": getattr(module, "name", "unknown"),
                "status": "ERROR",
                "message": str(error)
            })

    return results


def summary(registry):

    results = scan_registry(registry)

    online = sum(
        1 for r in results
        if r["status"] in ("ONLINE", "READY")
    )

    errors = sum(
        1 for r in results
        if r["status"] == "ERROR"
    )

    disabled = sum(
        1 for r in results
        if r["status"] == "DISABLED"
    )

    return {
        "total": len(results),
        "online": online,
        "errors": errors,
        "disabled": disabled,
        "details": results
    }

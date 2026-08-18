# modules/memory.py
# ============================================================
# CEREBRO OMEGA
# MÓDULO 01 — MEMORIA PERSISTENTE
# ============================================================

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


class MemoryEngine:
    """
    Motor de memoria persistente de CEREBRO OMEGA.

    Funciones:
        - Crear almacenamiento automáticamente
        - Guardar información
        - Leer memoria
        - Buscar información
        - Eliminar elementos
        - Contar recuerdos
        - Crear diagnóstico
        - Manejar errores sin romper el programa
    """

    NAME = "memory"
    VERSION = "1.0.0"

    def __init__(self, storage_path: str = "data/memory.json"):
        self.storage_path = Path(storage_path)

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize_storage()

    # ========================================================
    # UTILIDADES INTERNAS
    # ========================================================

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _initialize_storage(self) -> None:

        if not self.storage_path.exists():

            self._write({
                "version": self.VERSION,
                "created": self._now(),
                "memories": []
            })

    def _read(self) -> dict:

        try:

            with self.storage_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    "La memoria tiene formato inválido."
                )

            if "memories" not in data:
                data["memories"] = []

            return data

        except (json.JSONDecodeError, OSError, ValueError):

            # Recuperación automática
            data = {
                "version": self.VERSION,
                "created": self._now(),
                "memories": []
            }

            self._write(data)

            return data

    def _write(self, data: dict) -> bool:

        temporary = self.storage_path.with_suffix(
            ".tmp"
        )

        try:

            with temporary.open(
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            temporary.replace(self.storage_path)

            return True

        except OSError:

            if temporary.exists():
                temporary.unlink()

            return False

    # ========================================================
    # GUARDAR
    # ========================================================

    def remember(
        self,
        content: Any,
        category: str = "general",
        importance: int = 1
    ) -> dict:

        if content is None:
            return {
                "ok": False,
                "error": "No se puede guardar información vacía."
            }

        importance = max(
            1,
            min(int(importance), 10)
        )

        data = self._read()

        memory_id = len(data["memories"]) + 1

        memory = {
            "id": memory_id,
            "timestamp": self._now(),
            "category": category,
            "importance": importance,
            "content": content
        }

        data["memories"].append(memory)

        if not self._write(data):

            return {
                "ok": False,
                "error": "No se pudo escribir la memoria."
            }

        return {
            "ok": True,
            "memory": memory
        }

    # ========================================================
    # LEER TODA LA MEMORIA
    # ========================================================

    def recall(self) -> list:

        data = self._read()

        return data["memories"]

    # ========================================================
    # BUSCAR
    # ========================================================

    def search(self, query: str) -> list:

        if not query:
            return []

        query = query.lower()

        memories = self.recall()

        results = []

        for memory in memories:

            text = str(
                memory.get("content", "")
            ).lower()

            category = str(
                memory.get("category", "")
            ).lower()

            if (
                query in text
                or query in category
            ):
                results.append(memory)

        return results

    # ========================================================
    # OBTENER POR ID
    # ========================================================

    def get(self, memory_id: int):

        memories = self.recall()

        for memory in memories:

            if memory.get("id") == memory_id:
                return memory

        return None

    # ========================================================
    # ELIMINAR
    # ========================================================

    def forget(self, memory_id: int) -> dict:

        data = self._read()

        original = len(data["memories"])

        data["memories"] = [
            memory
            for memory in data["memories"]
            if memory.get("id") != memory_id
        ]

        if len(data["memories"]) == original:

            return {
                "ok": False,
                "error": "Memoria no encontrada."
            }

        if not self._write(data):

            return {
                "ok": False,
                "error": "No se pudo actualizar la memoria."
            }

        return {
            "ok": True,
            "deleted": memory_id
        }

    # ========================================================
    # CONTAR
    # ========================================================

    def count(self) -> int:

        return len(self.recall())

    # ========================================================
    # DIAGNÓSTICO
    # ========================================================

    def diagnostics(self) -> dict:

        return {
            "module": self.NAME,
            "version": self.VERSION,
            "storage": str(self.storage_path),
            "storage_exists": self.storage_path.exists(),
            "memories": self.count(),
            "status": "ONLINE"
        }


# ============================================================
# PRUEBA DEL MÓDULO
# ============================================================

def main():

    print()
    print("=" * 60)
    print(" CEREBRO OMEGA — MÓDULO DE MEMORIA")
    print("=" * 60)

    memory = MemoryEngine()

    print()
    print("MÓDULO:", memory.NAME)
    print("VERSIÓN:", memory.VERSION)

    # --------------------------------------------------------
    # GUARDAR PRUEBA
    # --------------------------------------------------------

    result = memory.remember(
        "CEREBRO OMEGA inició correctamente.",
        category="system",
        importance=10
    )

    print()
    print("GUARDAR:")
    print(result)

    # --------------------------------------------------------
    # LEER
    # --------------------------------------------------------

    print()
    print("MEMORIAS:")

    for item in memory.recall():

        print(
            f"[{item['id']}] "
            f"{item['category']} → "
            f"{item['content']}"
        )

    # --------------------------------------------------------
    # BUSCAR
    # --------------------------------------------------------

    print()
    print("BÚSQUEDA:")

    results = memory.search("OMEGA")

    for item in results:
        print(item)

    # --------------------------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------------------------

    print()
    print("DIAGNÓSTICO:")
    print(memory.diagnostics())

    print()
    print("=" * 60)
    print(" MÓDULO FUNCIONANDO")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()

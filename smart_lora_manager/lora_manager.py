import os
from dataclasses import dataclass
import json
from typing import Dict, Optional

try:
    from safetensors.torch import safe_open
except Exception:  # pragma: no cover - safetensors optional
    safe_open = None

@dataclass

class LoRAMetadata:
    path: str
    name: str
    category: str | None = None


class LoadLoRAs:
    """Carga archivos LoRA desde un directorio."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"directory": ("STRING", {"default": "loras"})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("loras",)
    FUNCTION = "load"
    CATEGORY = "SmartLoRA"

    def _read_metadata(self, path: str) -> LoRAMetadata:
        base, ext = os.path.splitext(path)
        category: Optional[str] = None

        if ext == ".safetensors" and safe_open is not None:
            try:
                with safe_open(path, framework="pt") as f:
                    meta = f.metadata() or {}
                    category = meta.get("category")
            except Exception:
                pass

        sidecar = f"{base}.json"
        if category is None and os.path.isfile(sidecar):
            try:
                with open(sidecar, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    category = data.get("category")
            except Exception:
                pass

        return LoRAMetadata(path=path, name=os.path.basename(base), category=category)

    def load(self, directory):
        metadata: Dict[str, Optional[str]] = {}
        if os.path.isdir(directory):
            for name in os.listdir(directory):
                if name.endswith((".safetensors", ".ckpt")):
                    path = os.path.join(directory, name)
                    meta = self._read_metadata(path)
                    metadata[path] = meta.category
        return (json.dumps(metadata),)


class SmartLoRASelector:
    """Selecciona LoRAs en base a palabras clave en el prompt."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "loras": ("STRING", {}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("weights",)
    FUNCTION = "select"
    CATEGORY = "SmartLoRA"

    def select(self, loras, prompt):
        weights = []
        try:
            mapping: Dict[str, Optional[str]] = json.loads(loras)
        except json.JSONDecodeError:
            mapping = {p: None for p in loras.splitlines() if p}

        for path in mapping.keys():
            name = os.path.splitext(os.path.basename(path))[0].lower()
            if name in prompt.lower():
                weights.append(f"{path}:1.0")

        return ("\n".join(weights),)

import os
from dataclasses import dataclass
import json
import re
from typing import Dict, Optional, List

import yaml
from .preset_manager import PresetManager

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
    """Selecciona LoRAs en base a palabras clave o sinónimos en el prompt,
    utilizando límites de palabra para evitar coincidencias parciales."""

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

    def _load_synonyms(self) -> Dict[str, List[str]]:
        """Carga el diccionario de sinónimos desde 'synonyms.yaml'."""
        path = os.path.join(os.path.dirname(__file__), "synonyms.yaml")
        synonyms: Dict[str, List[str]] = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh) or {}
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, list):
                                synonyms[key.lower()] = [str(v).lower() for v in value]
            except Exception:
                pass
        return synonyms

    def select(self, loras, prompt):
        weights = []
        synonyms = self._load_synonyms()
        try:
            mapping: Dict[str, Optional[str]] = json.loads(loras)
        except json.JSONDecodeError:
            mapping = {p: None for p in loras.splitlines() if p}

        for path in mapping.keys():
            name = os.path.splitext(os.path.basename(path))[0].lower()
            patterns = [name] + synonyms.get(name, [])
            for term in patterns:
                if re.search(rf"\b{re.escape(term)}\b", prompt, re.IGNORECASE):
                    weights.append(f"{path}:1.0")
                    break

        return ("\n".join(weights),)


class LoRAWeightSlider:
    """Aplica un peso personalizado a los LoRAs seleccionados."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "weights": ("STRING", {}),
                "weight": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 2.0,
                        "step": 0.05,
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("weights",)
    FUNCTION = "apply"
    CATEGORY = "SmartLoRA"

    def apply(self, weights: str, weight: float):
        result = []
        for line in weights.splitlines():
            if not line:
                continue
            if ":" in line:
                path, _ = line.split(":", 1)
            else:
                path = line
            result.append(f"{path}:{weight}")
        return ("\n".join(result),)



class SaveLoRAPreset:
    """Guarda la lista de LoRAs y pesos en un archivo JSON."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "weights": ("STRING", {}),
                "path": ("STRING", {"default": "preset.json"}),
                "preview": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    FUNCTION = "save"
    CATEGORY = "SmartLoRA"

    def save(self, weights: str, path: str, preview: bool = False):
        manager = PresetManager(path)
        manager.save(weights)
        if preview:
            manager.preview(weights)
        return (path,)


class LoadLoRAPreset:
    """Carga un preset de LoRAs y devuelve el listado de pesos."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "preset.json"}),
                "preview": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("weights",)
    FUNCTION = "load"
    CATEGORY = "SmartLoRA"

    def load(self, path: str, preview: bool = False):
        manager = PresetManager(path)
        weights = manager.load()
        if preview:
            manager.preview(weights)
        return (weights,)

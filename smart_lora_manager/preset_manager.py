import json
import os
from typing import List, Dict, Any

try:
    import requests
except Exception:  # pragma: no cover - requests optional
    requests = None


class PresetManager:
    """Utility class to persist and preview LoRA weight presets."""

    def __init__(self, path: str):
        self.path = path

    def _serialize(self, weights: str) -> List[Dict[str, Any]]:
        data: List[Dict[str, Any]] = []
        for line in weights.splitlines():
            if not line:
                continue
            if ":" in line:
                path, weight = line.split(":", 1)
            else:
                path, weight = line, "1.0"
            try:
                weight_f = float(weight)
            except ValueError:
                weight_f = 1.0
            data.append({"path": path, "weight": weight_f})
        return data

    def _deserialize(self, data: Any) -> str:
        lines = []
        if isinstance(data, list):
            for item in data:
                try:
                    lines.append(f"{item['path']}:{item['weight']}")
                except Exception:
                    pass
        elif isinstance(data, dict):
            for path, weight in data.items():
                lines.append(f"{path}:{weight}")
        return "\n".join(lines)

    def save(self, weights: str) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self._serialize(weights), fh, indent=2)

    def load(self) -> str:
        if not os.path.isfile(self.path):
            return ""
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            return ""
        return self._deserialize(data)

    def preview(self, weights: str) -> None:
        """Invoke ComfyUI's preview API if available."""
        if requests is None:
            return
        try:
            requests.post("http://127.0.0.1:8188/preview", json={"weights": weights})
        except Exception:
            pass

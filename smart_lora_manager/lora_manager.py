import os

class LoadLoRAs:
    """Carga archivos LoRA desde un directorio."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"directory": ("STRING", {"default": "loras"})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("loras",)
    FUNCTION = "load"
    CATEGORY = "SmartLoRA"

    def load(self, directory):
        files = []
        if os.path.isdir(directory):
            for name in os.listdir(directory):
                if name.endswith((".safetensors", ".ckpt")):
                    files.append(os.path.join(directory, name))
        return ("\n".join(files),)


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
        for path in loras.splitlines():
            name = os.path.splitext(os.path.basename(path))[0].lower()
            if name in prompt.lower():
                weights.append(f"{path}:1.0")
        return ("\n".join(weights),)

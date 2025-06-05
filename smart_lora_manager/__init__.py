from .lora_manager import LoadLoRAs, SmartLoRASelector

NODE_CLASS_MAPPINGS = {
    "LoadLoRAs": LoadLoRAs,
    "SmartLoRASelector": SmartLoRASelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadLoRAs": "Load LoRAs",
    "SmartLoRASelector": "Smart LoRA Selector",
}

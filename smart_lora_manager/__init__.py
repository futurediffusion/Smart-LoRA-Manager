from .lora_manager import LoadLoRAs, SmartLoRASelector, LoRAWeightSlider, SaveLoRAPreset, LoadLoRAPreset

NODE_CLASS_MAPPINGS = {
    "LoadLoRAs": LoadLoRAs,
    "SmartLoRASelector": SmartLoRASelector,
    "LoRAWeightSlider": LoRAWeightSlider,
    "SaveLoRAPreset": SaveLoRAPreset,
    "LoadLoRAPreset": LoadLoRAPreset,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadLoRAs": "Load LoRAs",
    "SmartLoRASelector": "Smart LoRA Selector",
    "LoRAWeightSlider": "LoRA Weight Slider",
    "SaveLoRAPreset": "Save LoRA Preset",
    "LoadLoRAPreset": "Load LoRA Preset",
}

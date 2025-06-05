from .lora_manager import LoadLoRAs, SmartLoRASelector, LoRAWeightSlider

NODE_CLASS_MAPPINGS = {
    "LoadLoRAs": LoadLoRAs,
    "SmartLoRASelector": SmartLoRASelector,
    "LoRAWeightSlider": LoRAWeightSlider,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadLoRAs": "Load LoRAs",
    "SmartLoRASelector": "Smart LoRA Selector",
    "LoRAWeightSlider": "LoRA Weight Slider",
}

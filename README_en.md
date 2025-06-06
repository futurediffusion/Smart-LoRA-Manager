# Smart LoRA Manager

Smart LoRA Manager is an experimental node for **ComfyUI** focused on simplifying work with multiple LoRAs. The idea came about after noticing how tedious it can be to manually tweak the weight of each model when generating images with different styles or characters.

## What does it offer?

- **LoRA loader** with metadata and grouping by categories (characters, styles, poses, etc.).
- **Prompt analysis** to suggest automatic weights based on keywords.
- **Interface controls** to toggle LoRAs on the fly and adjust their weights using sliders.
- **Quick previews** to test combinations before doing a final render.
- **Configuration history** or reusable presets with the option to export them to a file.

## Project status

This repository is still an initial draft. The intention is to implement each module in a modular way so it can be easily integrated with the ComfyUI ecosystem.

If you have suggestions or want to collaborate, you are welcome!

## Installation

1. Copy the `smart_lora_manager` folder inside `ComfyUI/custom_nodes/`.
2. After restarting ComfyUI you should see the **Load LoRAs**, **Smart LoRA Selector** and **LoRA Weight Slider** nodes under the *SmartLoRA* category.

## Plugin structure

- `smart_lora_manager/__init__.py` registers the nodes for ComfyUI.
- `smart_lora_manager/lora_manager.py` contains the basic node implementations.

These nodes are a starting point for managing multiple LoRAs easily. **Load LoRAs** searches for `.safetensors` or `.ckpt` files in a directory and returns them as a list of paths. **Smart LoRA Selector** detects keywords or synonyms in the prompt to automatically activate the corresponding models. **LoRA Weight Slider** lets you adjust the weight applied to the selected models via a slider. The synonym dictionary is defined in `smart_lora_manager/synonyms.yaml` and can be modified as desired.

## Using categories

Each LoRA may include a `category` field in its metadata. `Load LoRAs` reads that information (from the `.safetensors` file itself or a JSON with the same name) and returns a JSON mapping where the key is the file path and the value is its category. This allows you to group models by character, style or any other classification you want.

If a file has no category defined, it is left empty. Future nodes will be able to use this data to filter or display LoRAs in an organized way.

## Adjusting weights

The **LoRA Weight Slider** node takes the output from **Smart LoRA Selector** and lets you modify the weight applied to all selected models using a slider. Simply connect the detected weight list to this node and choose the desired value to replace the weights with the one indicated.

## Saving and loading presets

With **Save LoRA Preset** you can store the list of active LoRAs and their weights in a JSON file:

```text
weights = "path/to/lora1.safetensors:1.0\npath/to/lora2.safetensors:0.8"
```

Connecting that string to the node and choosing a path generates `preset.json`. Later **Load LoRA Preset** reads that file and returns the weight format so you can reuse it in any workflow.

## Running tests

To run the unit test suite make sure `pytest` is installed and then execute:

```bash
pytest
```

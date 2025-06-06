# Smart LoRA Manager

[English version available here](README_en.md)

Smart LoRA Manager es un nodo experimental para **ComfyUI** enfocado en simplificar el trabajo con múltiples LoRAs. La idea surgió al notar lo tedioso que puede resultar ajustar manualmente los pesos de cada modelo al generar imágenes con distintos estilos o personajes.

## ¿Qué busca ofrecer?

- **Cargador de LoRAs** con metadatos y agrupación por categorías (personajes, estilos, poses, etc.).
- **Análisis de prompts** para sugerir pesos automáticos basados en palabras clave.
- **Controles en la interfaz** para activar o desactivar LoRAs al vuelo y ajustar sus pesos mediante *sliders*.
- **Previsualizaciones rápidas** que permitan comprobar combinaciones antes de hacer el render final.
- **Historial de configuraciones** o presets reutilizables, con opción de exportarlos a un archivo.

## Estado del proyecto

Este repositorio es todavía un borrador inicial. La intención es ir implementando cada módulo de forma modular para integrarse fácilmente con el ecosistema de ComfyUI.

Si tienes sugerencias o quieres colaborar, ¡eres bienvenido!

## Instalación

1. Copia la carpeta `smart_lora_manager` dentro de `ComfyUI/custom_nodes/`.
2. Al reiniciar ComfyUI deberían aparecer los nodos **Load LoRAs**, **Smart LoRA Selector** y **LoRA Weight Slider** en la categoría *SmartLoRA*.
3. Instala las dependencias (PyYAML, requests y safetensors) con `pip install -r requirements.txt`.

## Estructura del plugin

- `smart_lora_manager/__init__.py` registra los nodos para ComfyUI.
- `smart_lora_manager/lora_manager.py` contiene la implementación básica de los nodos.

Estos nodos son un punto de partida para gestionar múltiples LoRAs de forma sencilla. El de **Load LoRAs** busca archivos `.safetensors` o `.ckpt` en un directorio y los devuelve como una lista de rutas. **Smart LoRA Selector** detecta palabras clave o sinónimos en el prompt para activar automáticamente los modelos correspondientes. **LoRA Weight Slider** permite ajustar el peso aplicado a los modelos seleccionados mediante un control deslizante. El diccionario de sinónimos se define en `smart_lora_manager/synonyms.yaml` y puede modificarse a gusto.

## Uso de categorías

Cada LoRA puede incluir un campo `category` en sus metadatos. `Load LoRAs` lee esa información (desde el propio archivo `.safetensors` o un JSON con el mismo nombre) y devuelve un mapeo en formato JSON donde la clave es la ruta del archivo y el valor su categoría. Esto permite agrupar modelos por personaje, estilo u otra clasificación que desees.

Si un archivo no tiene categoría definida, simplemente se deja vacío. Los nodos futuros podrán aprovechar este dato para filtrar o mostrar los LoRAs de forma ordenada.

## Ajuste de pesos

El nodo **LoRA Weight Slider** toma la salida de **Smart LoRA Selector** y permite modificar el peso aplicado a todos los modelos seleccionados usando un deslizador. Basta conectar la lista de pesos detectados a este nodo y escoger el valor deseado para que se reemplacen los pesos por el indicado.

## Guardar y cargar presets

Con **Save LoRA Preset** puedes almacenar la lista de LoRAs activos y sus pesos en un archivo JSON:

```text
weights = "path/to/lora1.safetensors:1.0\npath/to/lora2.safetensors:0.8"
```

Conectando esa cadena al nodo y eligiendo una ruta se genera `preset.json`. Luego **Load LoRA Preset** lee dicho archivo y devuelve el formato de pesos para reutilizarlo en cualquier flujo.


## Ejecutar pruebas

Para correr la suite de tests unitarios asegúrate de tener instalado `pytest` y ejecútala desde la raíz del repositorio con:

```bash
pytest
```


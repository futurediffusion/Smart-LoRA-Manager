# Smart LoRA Manager

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
2. Al reiniciar ComfyUI deberían aparecer los nodos **Load LoRAs** y **Smart LoRA Selector** en la categoría *SmartLoRA*.

## Estructura del plugin

- `smart_lora_manager/__init__.py` registra los nodos para ComfyUI.
- `smart_lora_manager/lora_manager.py` contiene la implementación básica de los nodos.

Estos nodos son un punto de partida para gestionar múltiples LoRAs de forma sencilla. El de **Load LoRAs** busca archivos `.safetensors` o `.ckpt` en un directorio y los devuelve como una lista de rutas. **Smart LoRA Selector** activa automáticamente aquellos LoRAs mencionados en el prompt.

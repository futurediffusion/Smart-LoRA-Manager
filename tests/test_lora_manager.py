import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import json
import os

from smart_lora_manager.lora_manager import (
    LoadLoRAs,
    SmartLoRASelector,
    LoRAMetadata,
    LoRAWeightSlider,
    SaveLoRAPreset,
    LoadLoRAPreset,
)
from smart_lora_manager import preset_manager


def test_load_loras_load(tmp_path, monkeypatch):
    file1 = tmp_path / "model1.safetensors"
    file1.write_text("")
    file2 = tmp_path / "model2.ckpt"
    file2.write_text("")
    other = tmp_path / "notes.txt"
    other.write_text("irrelevant")

    categories = {
        "model1.safetensors": "char",
        "model2.ckpt": None,
    }

    def fake_read_metadata(self, path):
        name = os.path.basename(path)
        return LoRAMetadata(path=path, name=os.path.splitext(name)[0], category=categories[name])

    monkeypatch.setattr(LoadLoRAs, "_read_metadata", fake_read_metadata)

    loader = LoadLoRAs()
    result_json, = loader.load(str(tmp_path))
    mapping = json.loads(result_json)

    assert mapping == {str(file1): "char", str(file2): None}


def test_smart_lora_selector_select(monkeypatch):
    selector = SmartLoRASelector()

    synonyms = {"catgirl": ["nekomimi"], "warrior": ["fighter"]}
    monkeypatch.setattr(SmartLoRASelector, "_load_synonyms", lambda self: synonyms)

    mapping = {
        "/tmp/catgirl.safetensors": None,
        "/tmp/warrior.safetensors": None,
    }
    loras = json.dumps(mapping)

    result, = selector.select(loras, "A brave nekomimi appears")
    assert result == "/tmp/catgirl.safetensors:1.0"

    result_empty, = selector.select(loras, "fighterplane approaching")
    assert result_empty == ""


def test_lora_weight_slider_apply():
    slider = LoRAWeightSlider()
    weights = "a.safetensors:1.0\nb.ckpt:0.8\nc.safetensors"
    result, = slider.apply(weights, 0.5)
    assert result == "a.safetensors:0.5\nb.ckpt:0.5\nc.safetensors:0.5"


def test_save_and_load_lora_preset(tmp_path, monkeypatch):
    path = tmp_path / "preset.json"
    weights = "a.safetensors:1.0\nb.safetensors:0.7"

    calls = []

    def fake_preview(self, w):
        calls.append(w)

    monkeypatch.setattr(preset_manager.PresetManager, "preview", fake_preview)

    saver = SaveLoRAPreset()
    out_path, = saver.save(weights, str(path), preview=True)
    assert out_path == str(path)

    loader = LoadLoRAPreset()
    loaded, = loader.load(str(path), preview=True)

    assert loaded == weights
    assert calls == [weights, weights]


def test_preset_manager_preview(monkeypatch):
    manager = preset_manager.PresetManager("dummy")

    called = {}

    def fake_post(url, json):
        called["url"] = url
        called["json"] = json

    monkeypatch.setattr(
        preset_manager,
        "requests",
        type("Req", (), {"post": staticmethod(fake_post)}),
    )

    manager.preview("testweights")

    assert called == {
        "url": "http://127.0.0.1:8188/preview",
        "json": {"weights": "testweights"},
    }


def test_preset_manager_preview_no_requests(monkeypatch):
    manager = preset_manager.PresetManager("dummy")
    monkeypatch.setattr(preset_manager, "requests", None)
    # Should simply return without error
    manager.preview("ignored")

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import json
import os

from smart_lora_manager.lora_manager import LoadLoRAs, SmartLoRASelector, LoRAMetadata


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

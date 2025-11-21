# import pytest

# from app.schemas.promt import DefaultLayer, LayerType, LayerWithOptions
# from app.utils.prompt_parser import parse_prompt

# from pathlib import Path

# @pytest.fixture
# def read_prompt_file():
#     for name in ("prompt.txt", "prompt.md"):
#         path = Path(__file__).parent.parent / "app" / "data" / "prompts" / name
#         if path.exists():
#             return path.read_text(encoding="utf-8")

#     raise FileNotFoundError("prompt.txt или prompt.md не найден")
        

# def test_prompt_parser(read_prompt_file):
#     text = read_prompt_file
    
#     layers = parse_prompt(text)

#     assert isinstance(layers, list)
#     assert len(layers) > 0

#     seen_names = set()

#     for layer in layers:
#         assert isinstance(layer, (DefaultLayer, LayerWithOptions))

#         assert isinstance(layer.name, str)
#         assert layer.name.strip() != ""
#         assert layer.name not in seen_names
#         seen_names.add(layer.name)

#         if isinstance(layer, DefaultLayer):
#             assert layer.type == LayerType.Default
#             assert isinstance(layer.prompt, list)
#             assert len(layer.prompt) > 0
#             for item in layer.prompt:
#                 assert isinstance(item, str)

#         if isinstance(layer, LayerWithOptions):
#             assert layer.type == LayerType.Selectable
#             assert isinstance(layer.options, list)
#             assert len(layer.options) > 0

#             option_names = set()

#             for opt in layer.options:
#                 assert isinstance(opt.name, str)
#                 assert opt.name.strip() != ""
#                 assert opt.name not in option_names
#                 option_names.add(opt.name)

#                 assert isinstance(opt.prompt, list)
#                 assert len(opt.prompt) > 0
#                 for item in opt.prompt:
#                     assert isinstance(item, str)
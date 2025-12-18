import type { DefaultPromptLayer, PromptLayer, SelectablePromptLayer } from "@/types/Prompt";

export function isDefaultLayer(layer: PromptLayer): layer is DefaultPromptLayer {
  return "prompt" in layer && typeof layer.prompt === "string";
}

export function isSelectableLayer(layer: PromptLayer): layer is SelectablePromptLayer {
  return "options" in layer && Array.isArray(layer.options);
}
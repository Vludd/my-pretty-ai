export interface DefaultPromptLayer {
  id?: string
  type: string
  name: string
  description?: string
  prompt: string
  enabled: boolean
}

export interface PromptLayerOption {
  id?: string
  name: string
  description?: string
  prompt: string
  selected: boolean
}

export interface SelectablePromptLayer {
  type: string
  name: string
  multiple: boolean
  additional?: string
  options: PromptLayerOption[]
  enabled: boolean
}

export type PromptLayer = DefaultPromptLayer | SelectablePromptLayer;

export interface PromptModel {
  id: string
  name: string
  layers: PromptLayer[]
  isDefault: boolean
  createdAt: string
  updatedAt: string
}

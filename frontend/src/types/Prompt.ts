export interface PromptLayer {
  id: string
  name: string
  description?: string
  accentPrompt?: string
  prompt?: string
  prompts?: PromptLayerComplexPrompt[]
  options?: PromptLayerOption[]
  editable: boolean
  enabled: boolean
}

export interface PromptLayerComplexPrompt {
  name: string
  prompt: string
}

export interface PromptLayerOption {
  id: string
  name: string
  description?: string
  prompt: string
  editable: boolean
  selected: boolean
}
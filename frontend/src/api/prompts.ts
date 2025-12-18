import { fetchWithRetry } from "@/api/base";
import type { PromptModel } from "@/types/Prompt";

interface RawPrompt {
  public_id: string;
  name: string;
  layers?: string;
  is_default?: boolean;
  created_at: string;
  updated_at: string;
}

export async function getUserPrompts(userId: string): Promise<PromptModel[]> {

  const response = await fetchWithRetry(
    `/api/v1/llm/prompts?user_id=${userId}`,
    { method: "GET", headers: { "Content-Type": "application/json" } },
  );

  const raw = await response.json();
  
  const prompts: PromptModel[] = raw
    .map((item: RawPrompt) => ({
      id: item.public_id,
      name: item.name,
      layers: item.layers || [],
      isDefault: item.is_default || false,
      createdAt: item.created_at,
      updatedAt: item.updated_at,
    }))
    .sort((a: PromptModel, b: PromptModel) => {
    if (a.isDefault && !b.isDefault) return -1;
    if (!a.isDefault && b.isDefault) return 1;

    return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
  });

  return prompts;
}

export async function getUserPrompt(userId: string, promptId: string): Promise<PromptModel> {

  const response = await fetchWithRetry(
    `/api/v1/llm/prompt?user_id=${userId}&prompt_id=${promptId}`,
    { method: "GET", headers: { "Content-Type": "application/json" } },
  );

  const raw = await response.json();
  
  const prompts: PromptModel = {
    id: raw.public_id,
    name: raw.name,
    layers: raw.layers || [],
    isDefault: raw.is_default || false,
    createdAt: raw.created_at,
    updatedAt: raw.updated_at,
  }

  return prompts;
}
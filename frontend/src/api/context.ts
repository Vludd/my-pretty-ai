import { API_BASE_URL, fetchWithRetry } from "@/api/base";

const BASE_URL = `${API_BASE_URL}/llm/context`;

export async function loadContext(
  userId: string,
  conversationId: string
) {

  const response = await fetchWithRetry(
    `${BASE_URL}/load?user_id=${userId}&conversation_id=${conversationId}`,
    { method: "POST", headers: { "Content-Type": "application/json" } },
  );

  return response.json() as Promise<{ response: string }>;
}
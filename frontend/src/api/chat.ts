
export interface Message {
  public_id: string;
  sender_type: "ai" | "user";
  content: string;
  created_at: string;
  updated_at: string;
}

export async function getConversation(user_id: string) {
  const response = await fetch(`/api/v1/conversations?user_id=${user_id}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) throw new Error("Failed to fetch conversations");
  return response.json() as Promise<{ messages: string }>;
}

export async function loadContext(userId: string, conversationId: string) {
  const response = await fetch(`/api/v1/llm/load/conversation?user_id=${userId}&conversation_id=${conversationId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) throw new Error("Failed to load conversation context");
  return response.json() as Promise<{ response: string }>;
}

export async function loadConversation(userId: string, conversationId: string): Promise<Message[]> {
  await loadContext(userId, conversationId);

  const response = await fetch(`/api/v1/conversations/messages?user_id=${userId}&conversation_id=${conversationId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) throw new Error("Failed to fetch conversations");

  return response.json() as Promise<Message[]>;
}

export async function sendMessage(
  userId: string,
  conversationId: string,
  message: string
) {
  const response = await fetch(
    `/api/v1/llm/completion?user_id=${userId}&conversation_id=${conversationId}&text=${message}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!response.ok) throw new Error("Failed to send message");

  return response.json() as Promise<{ reply: string; usage?: unknown }>;
}

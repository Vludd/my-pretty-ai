import type { Message } from "@/types/Message";
import { fetchWithRetry } from "@/api/base";
import { loadContext } from "@/api/context";

const API_ROUTE = "/messages";

export async function getConversationMessages(
  userId: string,
  conversationId?: string,
): Promise<Message[]> {

  const response = await fetchWithRetry(
    `/api/v1/conversation/messages?user_id=${userId}&conversation_id=${conversationId}`,
    { method: "GET", headers: { "Content-Type": "application/json" } },
  );
  
  const messages = response.json() as Promise<Message[]>;
    
  try {
    if (conversationId) await loadContext(userId, conversationId);
  } catch (error) {
    console.log(error)
  }

  return messages;
}

export async function getLastMessage(
  userId: string,
  conversationId: string
): Promise<Message> {

  const response = await fetch(`/api/v1/conversations${API_ROUTE}/last?user_id=${userId}&conversation_id=${conversationId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  
  if (!response.ok) throw new Error("Failed to fetch last message");

  const raw = await response.json();

  const lastMessage: Message = {
    public_id: raw.public_id,
    sender_type: raw.title,
    content: raw.content,
    created_at: raw.created_at,
    updated_at: raw.updated_at
  };

  return lastMessage;
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

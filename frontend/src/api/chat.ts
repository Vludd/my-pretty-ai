import type { Chat } from "@/types/Chat";

export interface Message {
  public_id: string;
  sender_type: "ai" | "user";
  content: string;
  created_at: string;
  updated_at: string;
}

export async function getConversations(userId: string): Promise<Chat[]> {
  const response = await fetch(`/api/v1/conversations?user_id=${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) throw new Error("Failed to fetch conversations");

  const raw = await response.json();

  const chats: Chat[] = raw.map((item: any) => ({
    id: item.public_id,
    title: item.title,
    lastMessage: item.last_message || "",
    updatedAt: item.updated_at,
  }));

  return chats;
}

export async function getLastMessage(userId: string, conversationId: string): Promise<Message> {
  const response = await fetch(`/api/v1/conversations/messages/last?user_id=${userId}&conversation_id=${conversationId}`, {
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

export async function loadContext(userId: string, conversationId: string) {
  const response = await fetch(`/api/v1/llm/load/conversation?user_id=${userId}&conversation_id=${conversationId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) throw new Error("Failed to load conversation context");
  return response.json() as Promise<{ response: string }>;
}

export async function loadConversation(userId: string, conversationId?: string): Promise<Message[]> {
  if (conversationId) await loadContext(userId, conversationId);

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

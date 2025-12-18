import type { Chat } from "@/types/Chat";

import { API_BASE_URL, fetchWithRetry } from "@/api/base";

const BASE_URL = `${API_BASE_URL}/conversation`;

export async function getConversations(
  userId: string
): Promise<Chat[]> {

  const response = await fetchWithRetry(
    `${BASE_URL}/all?user_id=${userId}`, 
    { method: "GET", headers: { "Content-Type": "application/json" } }
  );

  if (!response.ok) throw new Error("Failed to fetch conversations");

  const raw = await response.json();

  const chats: Chat[] = raw
    .map((item: any) => ({
      id: item.public_id,
      title: item.title,
      lastMessage: item.last_message || "",
      updatedAt: item.updated_at,
    }))
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());

  return chats;
}

export async function createConversation(
  userId: string,
  message: string,
  title: string
) {
  
  const createChatResponse = await fetchWithRetry(
    `${BASE_URL}/create?user_id=${userId}&title=${title}`,
    { method: "POST", headers: { "Content-Type": "application/json" } }
  );

  if (!createChatResponse.ok) throw new Error("Failed to create chat");

  const chatData = (await createChatResponse.json()) as { public_id: string };
  const conversationId = chatData.public_id;

  const sendMessageResponse = await fetch(
    `/api/v1/llm/completion?user_id=${userId}&conversation_id=${conversationId}&text=${message}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!sendMessageResponse.ok) throw new Error("Failed to send message");

  const messageData = (await sendMessageResponse.json()) as { reply: string; usage?: unknown };

  return {
    conversationId,
    reply: messageData.reply,
    usage: messageData.usage,
  };
}

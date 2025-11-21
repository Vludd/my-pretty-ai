import type { Chat } from "@/types/Chat";

export interface Message {
  public_id: string;
  sender_type: "ai" | "user";
  content: string;
  created_at: string;
  updated_at: string;
}

async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  retries = 3,
  delay = 500,
  timeout = 5000
): Promise<Response> {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {

      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timer);

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      return response;
    } catch (error) {
      const isLast = attempt === retries;

      const isAbort = error instanceof DOMException && error.name === "AbortError";

      if (isLast) {
        throw new Error(
          isAbort
            ? `Request timeout after ${retries} attempts`
            : `Request failed after ${retries} attempts: ${String(error)}`
        );
      }

      await new Promise((res) => setTimeout(res, delay));
    }
  }

  throw new Error("Unreachable");
}

export async function getConversations(
  userId: string
): Promise<Chat[]> {
  const response = await fetch(`/api/v1/conversation/all?user_id=${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

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

export async function getLastMessage(
  userId: string,
  conversationId: string
): Promise<Message> {

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

export async function loadContext(
  userId: string,
  conversationId: string
) {

  const response = await fetchWithRetry(
    `/api/v1/llm/context/load?user_id=${userId}&conversation_id=${conversationId}`,
    { method: "POST", headers: { "Content-Type": "application/json" } },
  );

  return response.json() as Promise<{ response: string }>;
}

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

export async function createChatWithMessage(
  userId: string,
  message: string,
  title: string
) {
  
  const createChatResponse = await fetch(
    `/api/v1/conversation/create?user_id=${userId}&title=${title}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }
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

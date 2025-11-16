import { useEffect, useRef, useState } from "react";
import type { ChatModel } from "./ChatSidebar";
import { loadConversation, type Message } from "@/api/chat";
import { ChatMessage } from "./ChatMessage";

function formatTime(iso: string) {
  return new Date(iso).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  }); // "2025-10-23T23:43:09.711555Z" -> "11:43 PM"
}

interface ChatProviderProps {
  userId: string;
  conversationId: string;
}

export default function ChatProvider({ userId, conversationId }: ChatProviderProps) {
  const [chats, setChats] = useState<ChatModel[]>([
      { id: "1", title: "Первый чат", updatedAt: new Date().toISOString() },
      { id: "2", title: "Тестовый диалог", updatedAt: new Date().toISOString(), lastMessage: "тестовый текст внутри чата, который скроется..." },
  ]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversation(userId, conversationId)
      .then((res) => {
        const sorted = res.sort(
          (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        );
        setMessages(sorted);
      })
      .finally(() => setLoading(false));
  }, [conversationId, userId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (loading) return <div className="p-4 text-center">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      {messages.map((msg) => (
        <ChatMessage
          key={msg.public_id}
          text={msg.content}
          time={formatTime(msg.created_at)}
          isUser={msg.sender_type === "user"}
        />
      ))}
      <div ref={bottomRef} />
    </div>
  )
}

import { ChatMessage } from "@/components/chat/ChatMessage";
import { useEffect, useRef, useState } from "react";
import { loadConversation, type Message } from "@/api/chat";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";

interface ChatPageProps {
  conversationId: string;
  userId: string;
}

export default function ChatPage({ userId, conversationId }: ChatPageProps) {
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

  if (loading) return <div className="p-4 text-center">Загрузка...</div>;

  return (
      <div className="flex flex-col h-screen">
        <Header />
        <main className="flex-1 p-4 overflow-y-auto">
          <div className="max-w-3xl mx-auto space-y-4">
            {messages.map((msg) => (
              <ChatMessage
                key={msg.public_id}
                text={msg.content}
                time={formatTime(msg.created_at)}
                isUser={msg.sender_type === "user"}
              />
            ))}
          </div>
        <div ref={bottomRef} />
        </main>
        <Footer userId={userId} conversationId={conversationId} setMessages={setMessages} />
      </div>
  );
}

// Вспомогательная функция: "2025-10-23T23:43:09.711555Z" → "11:43 PM"
function formatTime(iso: string) {
  return new Date(iso).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

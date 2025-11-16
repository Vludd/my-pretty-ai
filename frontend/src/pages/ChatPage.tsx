import { ChatMessage } from "@/components/chat/ChatMessage";
import { useEffect, useRef, useState } from "react";
import { loadConversation, type Message } from "@/api/chat";
import { ChatFooter } from "@/components/layout/ChatFooter";
import { ChatHeader } from "@/components/layout/ChatHeader";
import ModelSelector from "@/components/ModelSelector";
import type { AIModel } from "@/types/AiModel";
import { Link, useParams } from "react-router-dom";
import { useUser } from "@/context/useUser";
import { formatTime } from "@/utils/formatTime";

const models: AIModel[] = [
  { title: "Qwen3-4B", modelName: "Qwen3-4B model", downloaded: true },
  { title: "Llama2-7B", modelName: "Llama2-7B model", downloaded: false },
  { title: "GPT-4-All", modelName: "GPT-4-All model", downloaded: true },
];

export default function ChatPage() {
  const { userId } = useUser();

  const { conversationId } = useParams();

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
    
    <div className="flex h-screen overflow-hidden">
      <div className="flex flex-col flex-1">
        <ChatHeader>
          <div className="flex items-center justify-between w-full">
            <Link to="/dashboard" className="text-sm text-muted-foreground ">
              &larr; Back to AI Menu
            </Link>
            
            <ModelSelector models={models} />
          </div>
        </ChatHeader>
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
            <div ref={bottomRef} />
          </div>
        </main>
        <ChatFooter userId={userId} conversationId={conversationId} setMessages={setMessages} />
      </div>
    </div>
  );
}

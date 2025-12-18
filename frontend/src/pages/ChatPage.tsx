import { ChatMessage } from "@/components/ai/ChatMessage";
import { useEffect, useRef, useState } from "react";
import { ChatInput } from "@/components/ai/ChatInput";
import ModelSelector from "@/components/ModelSelector";
import type { AIModel } from "@/types/AiModel";
import { Link, useParams } from "react-router-dom";
import { useUser } from "@/context/useUser";
import { formatTime } from "@/utils/formatTime";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { ChevronLeft } from "lucide-react";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { Spinner } from "@/components/ui/spinner";
import PromptSelector from "@/components/PromptSelector";
import type { Message } from "@/types/Message";
import { getUserPrompts } from "@/api/prompts";
import type { PromptModel } from "@/types/Prompt";
import { getConversationMessages } from "@/api/messages";

const models: AIModel[] = [
  { title: "Qwen3-4B", modelName: "Qwen3-4B model", downloaded: true },
  { title: "Llama2-7B", modelName: "Llama2-7B model", downloaded: false },
  { title: "GPT-4-All", modelName: "GPT-4-All model", downloaded: true },
];

export default function ChatPage() {
  const { userId } = useUser();
  const { conversationId } = useParams();

  const [messages, setMessages] = useState<Message[]>([]);
  const [prompts, setPrompts] = useState<PromptModel[]>([]);

  const [messagesFetching, setMessagesFetching] = useState(true);
  const [promptsFetching, setPromptsFetching] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getConversationMessages(userId, conversationId)
      .then((res) => {
        const sorted = res.sort(
          (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        );
        setMessages(sorted);
      })
      .finally(() => setMessagesFetching(false));
  }, [conversationId, userId]);

  useEffect(() => {
    getUserPrompts(userId)
    .then((res) => {
      setPrompts(res);
    })
    .finally(() => setPromptsFetching(false));
  }, [userId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex h-screen ">
      <div className="flex flex-col flex-1 ">
        <Header>
          <div className="flex">
            <SidebarTrigger />
            <Link 
              to="/" 
              className="text-sm text-muted-foreground flex items-center whitespace-nowrap"
            >
              <ChevronLeft className="w-5 h-5 shrink-0" strokeWidth={2.5} />
              <span className="">Back to AI</span>
            </Link>
          </div>
          <PromptSelector prompts={prompts} loading={promptsFetching} />
          <ModelSelector models={models} loading={promptsFetching} />
        </Header>
          {!messagesFetching
            ? (
              <div className="flex-1 overflow-y-auto pb-8 px-4">
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
              </div>
            )
            : (
              <div className="flex flex-col items-center w-full justify-center h-screen">
                <Spinner className="w-10 h-10" />
              </div>
            )
          }
        
        <Footer className="bg-background shadow-md z-1 px-4">
          <ChatInput userId={userId} conversationId={conversationId} setMessages={setMessages} />
        </Footer>
      </div>
    </div>
  )
}

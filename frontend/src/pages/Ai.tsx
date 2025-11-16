import { getConversations as getConversations, getLastMessage } from "@/api/chat";
import AIChatList from "@/components/ai/ChatList";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useUser } from "@/context/useUser";
import type { Chat } from "@/types/Chat";
import { Plus, SendHorizontalIcon } from "lucide-react";
import { useEffect, useRef, useState } from "react";

export default function AIPage() {
  const { userId } = useUser();
  
  const [loading, setLoading] = useState(true);
  const [chats, setChats] = useState<Chat[]>([]);

  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleInput = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    setText(textarea.value);
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  const handleSend = async () => {
    const trimmed = text.trim();
    if (!trimmed) return;

    // const userMessage: Message = {
    //   public_id: uuidv4(),
    //   sender_type: "user",
    //   content: trimmed,
    //   created_at: new Date().toISOString(),
    //   updated_at: new Date().toISOString(),
    // };

    // setMessages((prev) => [...prev, userMessage]);
    setText("");
    if (textareaRef.current) textareaRef.current.value = "";

    // try {
    //   const res = await sendMessage(userId, conversationId, trimmed);

    //   const aiMessage: Message = {
    //     public_id: uuidv4(),
    //     sender_type: "ai",
    //     content: res.reply,
    //     created_at: new Date().toISOString(),
    //     updated_at: new Date().toISOString(),
    //   };
    //   setMessages((prev) => [...prev, aiMessage]);
    // } catch (err) {
    //   console.error("Error sending message:", err);
    // }

    handleInput();
  };

  useEffect(() => {
    let isMounted = true;

    async function loadChats() {
      try {
        const list = await getConversations(userId);

        const chatsWithLastMessage = await Promise.all(
          list.map(async (chat) => {
            try {
              const last = await getLastMessage(userId, chat.id); 
              return {
                ...chat,
                lastMessage: last.content,
                updatedAt: last.updated_at
              };
            } catch {
              return { ...chat, lastMessage: "" };
            }
          })
        );

        if (isMounted) setChats(chatsWithLastMessage);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadChats();

    return () => {
      isMounted = false;
    };
  }, [userId]);

  return (
    <div className="flex flex-col justify-center h-screen">
      <div className="bg-background p-2">
        <div className="max-w-3xl mx-auto flex items-end gap-1 rounded-3xl border bg-muted/50 p-2 shadow-sm">
          <Button 
            variant="ghost"
            size="icon" 
            className={`rounded-full cursor-not-allowed opacity-50`}
            title="Вложить файл (В разработке)"
          >
            <Plus />
          </Button>

          <Textarea
            ref={textareaRef}
            rows={1}
            placeholder="Do you want to chat? :3"
            className="flex-1 resize-none border-none min-h-[10px] max-h-[200px] !bg-transparent p-2 focus-visible:ring-0"
            onInput={handleInput}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />

          <Button 
            variant="default"
            onClick={handleSend}
            size="icon"
            disabled={text.trim() === ""}
            className={`rounded-full `}
            title={text.trim() === "" ? "Отправить голосовое сообщение (В разработке)" : "Отправить сообщение"}
          >
            <SendHorizontalIcon />
          </Button>
        </div>
      </div>
      <AIChatList chats={chats}/>
    </div>
  );
}
import { sendMessage, type Message } from "@/api/chat";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Mic, Plus, SendHorizontalIcon } from "lucide-react";
import { useRef, useState } from "react";

interface FooterProps {
  userId: string;
  conversationId: string;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

export const Footer = ({ userId, conversationId, setMessages }: FooterProps) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [text, setText] = useState("");

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

    const userMessage: Message = {
      public_id: crypto.randomUUID(),
      sender_type: "user",
      content: trimmed,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setText(""); // ✅ очищаем состояние
    if (textareaRef.current) textareaRef.current.value = "";

    try {
      const res = await sendMessage(userId, conversationId, trimmed);

      const aiMessage: Message = {
        public_id: crypto.randomUUID(),
        sender_type: "ai",
        content: res.reply,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error("Error sending message:", err);
    }

    handleInput();
  };

  return (
    <footer className="border-t bg-background p-2">
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
          placeholder="You want to chat? ;)"
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
          className={`rounded-full ${text.trim() === "" ? "cursor-not-allowed opacity-50" : "cursor-pointer"}`}
          title={text.trim() === "" ? "Отправить голосовое сообщение (В разработке)" : "Отправить сообщение"}
        >
          {text.trim() === "" ? <Mic /> : <SendHorizontalIcon />}
        </Button>
      </div>
      <p className="text-muted-foreground text-xs text-center mt-2">
        MyPrettyAI v{__APP_VERSION__}
      </p>
    </footer>
  );
};
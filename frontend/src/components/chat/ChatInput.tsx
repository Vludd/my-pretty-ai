import { sendMessage, type Message } from "@/api/chat";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Mic, Plus, SendHorizontalIcon } from "lucide-react";
import { useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { Spinner } from "../ui/spinner";

interface FooterProps {
  userId: string;
  conversationId?: string;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

export const ChatInput = ({ userId, conversationId, setMessages }: FooterProps) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [text, setText] = useState("");
  const [responding, setResponding] = useState(false);

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
      public_id: uuidv4(),
      sender_type: "user",
      content: trimmed,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setText("");
    if (textareaRef.current) textareaRef.current.value = "";

    try {
      if (!conversationId) throw new Error("Conversation ID is required to send a message");
      setResponding(true);
      const res = await sendMessage(userId, conversationId, trimmed);

      const aiMessage: Message = {
        public_id: uuidv4(),
        sender_type: "ai",
        content: res.reply,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error("Error sending message:", err);
    } finally {
      setResponding(false);
    }

    handleInput();
  };

  return (
    <div className="relative pt-4 pb-10">
      <div className="absolute left-0 right-0 bottom-2">
        <div className="max-w-3xl mx-auto flex items-end gap-1 rounded-3xl border bg-muted p-2 shadow-sm">
          <Button 
            variant="ghost"
            size="icon"
            disabled
            className={`rounded-full`}
            title="Attach a file"
          >
            <Plus />
          </Button>

          <Textarea
            ref={textareaRef}
            rows={1}
            disabled={responding}
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
            disabled={text.trim() === "" || responding}
            className={`rounded-full`}
            title={text.trim() === "" ? "Send a voice message (In Dev)" : "Send a message"}
          >
            {responding ? <Spinner /> : text.trim() === "" ? <Mic /> : <SendHorizontalIcon />}
          </Button>
        </div>
        <p className="text-muted-foreground text-xs text-center mt-2">
          Vludd.exe &copy; 2025. All rights reserved.
        </p>
      </div>
    </div>
  )
}

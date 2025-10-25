import { Card } from "@/components/ui/card";
import { MessageActions } from "./MessageActions";

interface ChatMessageProps {
  text: string;
  time: string;
  isUser?: boolean;
}

export const ChatMessage = ({ text, time, isUser }: ChatMessageProps) => (
  <div className={`flex ${isUser ? "justify-end" : "justify-start"} group relative`}>
    <Card
      className={`relative border-none p-3 pb-6 max-w-[80%] rounded-2xl
        ${isUser ? "bg-primary rounded-br-none" : "bg-muted rounded-bl-none"}`}
    >
      <MessageActions text={text} isUser={isUser} />
      <p className={`text-sm leading-snug
        ${isUser ? "text-primary-foreground": ""}`}>{text}</p>
      <span className={`absolute bottom-1 right-3 text-[10px] opacity-70
        ${isUser ? "text-primary-foreground": ""}`}>{time}</span>
    </Card>
  </div>
);
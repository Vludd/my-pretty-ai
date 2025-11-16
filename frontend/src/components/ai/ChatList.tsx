import type { Chat } from "@/types/Chat";
import { ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../ui/button";

interface Props {
  chats: Chat[]
}

export default function AIChatList({ chats }: Props) {
  const maxChatsToShow = 5;

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <div className="flex flex-col gap-2 max-w-3xl mx-auto w-full">
        {chats.slice(0, maxChatsToShow).map((chat) => (
          <div>
            <Link
              key={chat.id}
              to={`/chat/${chat.id}`}
              className="block p-3 rounded-lg bg-muted/50 text-muted-foreground hover:bg-muted hover:text-primary transition-colors"
            >
              <div className="flex items-center gap-2">
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{chat.title}</p>
                  <p className="text-xs text-muted-foreground truncate">{chat.lastMessage || ""}</p>
                </div>
                <ChevronRight className="size-4 flex-shrink-0" />
              </div>
            </Link>
          </div>
        ))}
      </div>
      {chats.length > maxChatsToShow && (
        <Button variant="outline">All Chats</Button>
      )}
    </div>
  );
}
import type { Chat } from "@/types/Chat";
import { ChevronRight } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../ui/button";

interface Props {
  chats: Chat[]
  chatsCount: number
}

export default function AIChatList({ chats, chatsCount }: Props) {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center gap-2 w-full">
      <div className="flex flex-col gap-2 w-full min-w-0">
        {chats.slice(0, chatsCount).map((chat) => (
          <div className="w-full min-w-0">
            <Link
              key={chat.id}
              to={`/c/${chat.id}`}
              className="block p-3 rounded-lg bg-muted/50 text-muted-foreground hover:bg-muted hover:text-primary transition-colors"
            >
              <div className="flex items-center gap-2 min-w-0">
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
      {chats.length > chatsCount && (
        <Button 
          variant="outline"
          onClick={() => {navigate(`/chats`);}}
        >
          All Chats
        </Button>
      )}
    </div>
  )
}
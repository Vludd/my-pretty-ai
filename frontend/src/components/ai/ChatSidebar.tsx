import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Chat } from "@/types/Chat";

interface ChatSidebarProps {
  chats: Chat[];
  currentChatId?: string;
  onSelect: (chatId: string) => void;
  onNewChat: () => void;
}

export const ChatSidebar = ({
  chats,
  currentChatId,
  onSelect,
  onNewChat,
}: ChatSidebarProps) => {
  return (
    <aside className="hidden md:flex md:flex-col w-64 border-r bg-muted/30 h-full">
      <div className="p-3 flex justify-between items-center border-b shrink-0">
        <h2 className="text-sm font-semibold text-muted-foreground"></h2>
        <Button
          variant="outline"
          size="icon"
          className="cursor-pointer"
          onClick={onNewChat}
        >
          <Plus size={16} />
        </Button>
      </div>

      <ScrollArea className="flex-1">
        <div className="flex flex-col">
          {chats.map((chat) => (
            <Button
              key={chat.id}
              variant={chat.id === currentChatId ? "secondary" : "ghost"}
              className={cn(
                "border-b rounded-none flex flex-col items-start text-left px-3 py-2 h-[60px]",
                "overflow-hidden"
              )}
              onClick={() => onSelect(chat.id)}
            >
              <p className="font-medium text-sm truncate w-full">{chat.title}</p>
              {chat.lastMessage && (
                <p className="text-xs text-muted-foreground w-full truncate">
                  {chat.lastMessage}
                </p>
              )}
            </Button>
          ))}
        </div>
      </ScrollArea>

      <div className="p-3 text-xs text-center text-muted-foreground border-t shrink-0">
        MyPrettyAI v{__APP_VERSION__}
      </div>
    </aside>
  );
};

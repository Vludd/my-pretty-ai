import { getConversations, getLastMessage } from "@/api/chat";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useUser } from "@/context/useUser";
import type { Chat } from "@/types/Chat";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export const ConversationsPage = () => {
  const { userId } = useUser();

  const [chats, setChats] = useState<Chat[]>([]);
  const [fetching, setFetching] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const showLastMessage = false;

  useEffect(() => {
    let isMounted = true;

    async function loadChats() {
      try {
        setFetching(true);
        const list = await getConversations(userId);

        const chatsWithLastMessage = await Promise.all(
          list.map(async (chat) => {
            if (!showLastMessage) return { ...chat, lastMessage: "" };

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
      } catch {
        setErrorMsg("Error retrieving chat list")
      } finally {
        if (isMounted) setFetching(false);
      }
    }

    loadChats();

    return () => {
      isMounted = false;
    };
  }, [showLastMessage, userId]);
  
  return (
    <div>
      <Header className="justify-start">
        <SidebarTrigger />
        <Link 
          to="/"
          className="text-sm text-muted-foreground flex items-center whitespace-nowrap"
        >
          <ChevronLeft className="w-5 h-5 shrink-0" strokeWidth={2.5} />
          <span className="">Back to AI</span>
        </Link>
      </Header>
      <div className="flex flex-col w-full items-center p-4">
        <div className="flex flex-col gap-2 max-w-3xl min-w-0 w-full">
          {chats.map((chat) => (
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
      </div>
      <Footer>

      </Footer>
    </div>
  );
};
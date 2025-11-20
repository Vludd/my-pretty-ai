import { createChatWithMessage, getConversations as getConversations, getLastMessage } from "@/api/chat";
import AIChatList from "@/components/ai/ChatList";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { Button } from "@/components/ui/button";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";
import { useUser } from "@/context/useUser";
import type { Chat } from "@/types/Chat";
import { AlertOctagon, Plus, SendHorizontal } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { generateChatTitle } from "@/utils/generateChatTitle";

export default function AIPage() {
  const navigate = useNavigate();
  const { userId } = useUser();
  const [errorMsg, setErrorMsg] = useState("");
  
  const [creatingConversation, setCreatingConversation] = useState(false);
  const [fetchingChats, setFetchingChats] = useState(true);
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

    setText("");
    if (textareaRef.current) textareaRef.current.value = "";

    try {
      setCreatingConversation(true);

      const title = generateChatTitle(trimmed);

      const res = await createChatWithMessage(userId, trimmed, title);

      navigate(`/c/${res.conversationId}`);
    } catch (err) {
      console.error("Error creating chat:", err);
    } finally {
      setCreatingConversation(false); 
    }
  };

  const showLastMessage = false;

  useEffect(() => {
    let isMounted = true;

    async function loadChats() {
      try {
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
        if (isMounted) setFetchingChats(false);
      }
    }

    loadChats();

    return () => {
      isMounted = false;
    };
  }, [showLastMessage, userId]);

  return (
    <div className="flex flex-col h-screen justify-between w-full">

      <Header>
        <SidebarTrigger />
      </Header>

      {!errorMsg 
      ? (
        <div className="flex flex-col justify-center h-screen min-w-0 w-full items-center p-2 gap-4">
          {!fetchingChats && (
            <div className="w-full max-w-3xl flex items-end gap-1 rounded-3xl border bg-muted/50 p-2 shadow-sm">
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
                disabled={creatingConversation}
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
                disabled={text.trim() === "" || creatingConversation }
                className={`rounded-full `}
                title={text.trim() === "" ? "Send a voice message" : "Send message"}
              >
                {creatingConversation
                  ? <Spinner /> 
                  : <SendHorizontal />
                }
              </Button>
            </div>
          )}

          <div className="flex flex-col items-center gap-2 w-full max-w-3xl">
            {fetchingChats 
              ? (
                <div className="flex flex-col space-y-2 w-full">
                    <Skeleton className="h-14 rounded-3xl" />
                    <Skeleton className="h-12 " />
                    <Skeleton className="h-12 " />
                    <Skeleton className="h-12 " />
                    <Skeleton className="h-12 " />
                    <Skeleton className="h-12 " />
                </div>
              ) : <AIChatList chats={chats} chatsCount={3} /> 
            }
          </div>
        </div>
      ) : (
        <div className="flex flex-col justify-center w-full h-screen items-center p-2">
          <Alert variant="destructive" className="max-w-3xl">
            <AlertOctagon />
            <AlertTitle>Error retrieving chat list</AlertTitle>
            <AlertDescription>
              <p>Please make sure the server is available and try again.</p>
              <ul className="list-inside list-disc text-sm">
                <li>Check if the backend service is running on 8000 port</li>
                <li>Verify that PostgreSQL is working and authenticated</li>
              </ul>
            </AlertDescription>
          </Alert>
        </div>
      )}

      <Footer>
      </Footer>
    </div>
  );
}
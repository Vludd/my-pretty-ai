import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { SidebarProvider } from "@/components/ui/sidebar";
import Dashboard from "@/pages/Dashboard";
import Settings from "@/pages/Settings";
import AppSidebar from "@/components/AppSidebar";
import ChatPage from "@/pages/ChatPage";
import AIPage from "@/pages/Ai";

import { UserProvider } from "@/context/UserProvider";
import { ConversationsPage } from "@/pages/Conversations";

export default function AppLayout() {
  const userId = "c602e0b8-464c-431e-a5aa-f6098d27defb";
  
  return (
    <UserProvider userId={userId}>
      <Router>
        <SidebarProvider className="flex h-screen w-full ">
          <AppSidebar />
          <main className="w-full h-screen">
            <Routes>
              <Route path="/" element={<AIPage />} />
              <Route path="/chats" element={<ConversationsPage />} />
              <Route path="/c/:conversationId" element={<ChatPage />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
        </SidebarProvider>
      </Router>
    </UserProvider>
  );
}

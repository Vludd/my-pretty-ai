import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { SidebarProvider, SidebarTrigger } from "../ui/sidebar";
import Dashboard from "@/pages/Dashboard";
import Settings from "@/pages/Settings";
import AppSidebar from "../AppSidebar";
import ChatPage from "@/pages/ChatPage";
import AIPage from "@/pages/Ai";

import { UserProvider } from "@/context/UserProvider";

export default function AppLayout() {
  const userId = "c602e0b8-464c-431e-a5aa-f6098d27defb";
  
  return (
    <UserProvider userId={userId}>
      <Router>
        <SidebarProvider className="flex h-screen w-full">
          <AppSidebar />
          <div className="w-full">
            <SidebarTrigger className="fixed m-2 p-4"/>
            <Routes>
              <Route path="/" element={<AIPage />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/chat/:conversationId" element={<ChatPage />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </SidebarProvider>
      </Router>
    </UserProvider>
  );
}

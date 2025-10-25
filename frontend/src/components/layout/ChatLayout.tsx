import { Header } from "./Header";
import { Footer } from "./Footer";
import { type ReactNode } from "react";

export const ChatLayout = ({ children }: { children: ReactNode }) => (
  <div className="flex flex-col h-screen">
    <Header />
    <main className="flex-1 p-4 overflow-y-auto">
      <div className="max-w-3xl mx-auto space-y-4">{children}</div>
    </main>
    <Footer  />
  </div>
);
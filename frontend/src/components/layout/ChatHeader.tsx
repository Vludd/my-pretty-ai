import type { ReactNode } from "react";

interface ChatHeaderProps {
  children?: ReactNode;
}

export const ChatHeader = ({ children }: ChatHeaderProps) => (
  <header className={`${children && "flex items-center justify-center px-4 py-2 border-b"}`}>
    {children}
  </header>
);

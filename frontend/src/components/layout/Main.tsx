import type { ReactNode } from "react";

interface MainProps {
  className?: string;
  children?: ReactNode;
}

export const Main = ({ className, children }: MainProps) => (
  <main className={`${children && ""} ${className}`}>
    {children}
  </main>
);

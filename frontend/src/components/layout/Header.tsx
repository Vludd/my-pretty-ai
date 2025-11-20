import { cn } from "@/lib/utils";
import type { ReactNode, HTMLAttributes } from "react";

interface HeaderProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
  separator?: boolean;
}

export const Header = ({ className, children, separator, ...props }: HeaderProps) => {
  return (
    <div
      className={cn(
        "flex items-center w-full justify-between p-2 shadow-md z-1 bg-background",
        className, 
        separator ? "border-b" : ""
        )}
      {...props}
    >
      {children}
    </div>
  );
};

import { cn } from "@/lib/utils";
import type { ReactNode, HTMLAttributes } from "react";

interface FooterProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
  separator?: boolean;
}

export const Footer = ({ className, children, separator, ...props }: FooterProps) => {
  return (
    <div
      className={cn("mt-auto", className, separator ? "border-t": "")}
      {...props}
    >
      {children}
    </div>
  );
};

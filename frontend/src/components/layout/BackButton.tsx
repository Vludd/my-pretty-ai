import type { HTMLAttributes } from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

import { ChevronLeft } from "lucide-react";

interface BackButtonProps extends HTMLAttributes<HTMLDivElement> {
  text: string;
  to: string;
}

export const BackButton = ({ className, text, to, ...props }: BackButtonProps) => {
  return (
    <div
      className={cn("", className)}
      {...props}
    >
      <Link 
        to={to}
        className="text-sm text-muted-foreground flex items-center whitespace-nowrap"
      >
        <ChevronLeft className="w-5 h-5 shrink-0" strokeWidth={2.5} />
        <span className="">{text}</span>
      </Link>
    </div>
  );
};
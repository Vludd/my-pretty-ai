import type { NavItem } from "@/types/NavItem";

export function getNavLinkClass(item: NavItem, isActive: boolean) {
  const base =
    "flex items-center gap-2 px-2 py-1.5 rounded-md w-full " +
    "transition-all duration-300 ease-in-out";

  const aiActive =
    "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white animate-gradient-x";
  const aiInactive =
    "bg-gradient-to-r from-indigo-500/50 via-purple-500/50 to-pink-500/50 text-muted-foreground animate-gradient-x " +
    "hover:bg-gradient-to-r hover:from-indigo-500/50 hover:via-purple-500/50 hover:to-pink-500/50 hover:text-white";

  const defaultActive = "bg-secondary text-accent-foreground";
  const defaultInactive =
    "text-muted-foreground hover:text-accent-foreground hover:bg-secondary";

  if (isActive) return `${base} ${item.title === "AI" ? aiActive : defaultActive}`;
  return `${base} ${item.title === "AI" ? aiInactive : defaultInactive}`;
}
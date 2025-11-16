import type { SidebarGroup } from "@/types/SidebarGroup";
import { ChartPie, Settings, Wand2 } from "lucide-react";

export const sidebarItems: SidebarGroup[] = [
  {
    name: "",
    items: [
      { title: "AI", url: "/", icon: Wand2 },
    ]
  },
  {
    name: "General",
    items: [
      { title: "Dashboard", url: "/dashboard", icon: ChartPie },
    ]
  },
  {
    name: "System",
    items: [
      { title: "Settings", url: "/settings", icon: Settings },
    ]
  },
]
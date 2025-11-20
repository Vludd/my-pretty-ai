import type { NavGroup } from "@/types/NavGroup";
import { ChartPie, Settings, Wand2 } from "lucide-react";

export const navGroups: NavGroup[] = [
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
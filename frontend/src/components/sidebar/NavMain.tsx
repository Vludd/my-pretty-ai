import { 
  SidebarGroup, 
  SidebarGroupContent, 
  SidebarGroupLabel, 
  SidebarMenu, 
  SidebarMenuItem, 
  SidebarSeparator, 
} from "@/components/ui/sidebar";

import type { NavGroup } from "@/types/NavGroup";

import { getNavLinkClass } from "@/utils/getNavLinkClass";
import { NavLink } from "react-router-dom";

interface NavMainProps {
  navGroups: NavGroup[]
}

export default function NavMain({navGroups}: NavMainProps) {
  return (
    <div>
      {navGroups.map((group, idx) => (
          <SidebarGroup key={idx} >
            {group.name && (
              <div className="flex justify-between w-full items-center">
                <SidebarGroupLabel 
                  className="text-xs text-muted-foreground uppercase tracking-wide"
                >
                  {group.name}
                </SidebarGroupLabel>
              </div>
            )}
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <NavLink
                      to={item.url}
                      className={({ isActive }) => getNavLinkClass(item, isActive)}
                    >
                      {item.icon && <item.icon className="w-4 h-4 shrink-0" />}
                      <span>{item.title}</span>
                    </NavLink>

                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>

            {idx < navGroups.length - 1 && <SidebarSeparator className="mt-2" />}
          </SidebarGroup>
        ))}
    </div>
  )
}
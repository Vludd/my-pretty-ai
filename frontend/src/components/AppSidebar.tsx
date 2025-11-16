import { NavLink, Link } from "react-router-dom";

import { 
  Sidebar, 
  SidebarContent, 
  SidebarFooter, 
  SidebarGroup, 
  SidebarGroupContent, 
  SidebarGroupLabel, 
  SidebarHeader, 
  SidebarMenu, 
  SidebarMenuButton, 
  SidebarMenuItem, 
  SidebarSeparator, 
} from "@/components/ui/sidebar";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";

import { ChevronUp, Ellipsis } from "lucide-react";

import { sidebarItems } from "@/data/appSidebarItems";
import { getNavLinkClass } from "@/utils/getNavLinkClass";

export default function AppSidebar() {

  return (
    <Sidebar>
      <SidebarHeader className="flex flex-row items-center justify-between m-2">
        <Link to="/" className="font-bold cursor-pointer">MyPrettyAI</Link>
      </SidebarHeader>
      
      <SidebarContent>
        {sidebarItems.map((group, idx) => (
          <SidebarGroup key={idx} >
            {group.name && (
              <div className="flex justify-between w-full items-center">
                <SidebarGroupLabel 
                  className="text-xs text-muted-foreground uppercase tracking-wide"
                >
                  {group.name}
                </SidebarGroupLabel>
                <Button
                  variant="ghost"
                  className="w-6 h-6 rounded-full cursor-poiсnter"
                >
                  <Ellipsis />
                </Button>
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

            {idx < sidebarItems.length - 1 && <SidebarSeparator className="mt-2" />}
          </SidebarGroup>
        ))}
      </SidebarContent>
      
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton className="cursor-pointer">
                  <Avatar>
                    <AvatarImage 
                      src="https://avatars.githubusercontent.com/u/95350423?v=4&size=64" 
                      alt="@username"
                    />
                    <AvatarFallback>UN</AvatarFallback>
                  </Avatar> Username
                  <ChevronUp className="ml-auto" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                side="top"
                className="w-[--radix-popper-anchor-width]"
              >
                <DropdownMenuItem className="cursor-pointer">
                  <span>Account</span>
                </DropdownMenuItem>
                <DropdownMenuItem className="cursor-pointer">
                  <span>Billing</span>
                </DropdownMenuItem>
                <DropdownMenuItem className="cursor-pointer">
                  <span>Sign out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
